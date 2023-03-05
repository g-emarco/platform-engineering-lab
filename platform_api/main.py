import datetime
from functools import wraps
from google.auth import jwt
from flask import Flask, session, abort, redirect, request, render_template
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud import storage
from google.oauth2 import service_account


app = Flask("Dev Platform")

firebase_admin.initialize_app()
db = firestore.client()


def login_is_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        auth_token = request.headers["Authorization"].split(" ")[1]
        decoded = jwt.decode(auth_token, verify=False)
        email = decoded["email"]
        return function(email)

    return wrapper


def grant_user_access_to_bucket(email, bucket_id):
    client = storage.Client()
    bucket = client.bucket(bucket_id)
    policy = bucket.get_iam_policy()
    policy.bindings.append(
        {
            "role": "roles/storage.objectViewer",
            "members": {f"user:{email}"},
        }
    )
    bucket.set_iam_policy(policy)
    print(f"Granted {email} for {bucket_id} bucket.")


@app.route("/request_access_for_bucket")
@login_is_required
def grant_access(email):
    bucket = request.args.get("bucket")
    print(f"user {email} is trying to access bucket {bucket}")
    doc_ref = db.collection("users").document(str(email))
    doc = doc_ref.get()
    if doc.exists:
        print(f"user {email} exists, not writing in firestore")
        doc_ref = (
            db.collection("users")
            .document(email)
            .collection("allowed_buckets")
            .document(bucket)
        )
        doc = doc_ref.get()
        if doc.exists:
            time_added = doc.to_dict().get("time_added")
            if (
                time_added
                and datetime.datetime.utcnow()
                - datetime.datetime.fromtimestamp(time_added.timestamp())
                < datetime.timedelta(hours=2)
            ):
                grant_user_access_to_bucket(email=email, bucket_id=bucket)
                return {"message": "Granted 1 hour access for bucket"}

            else:
                print("1 hour passed since last grant, deleting document")
                doc_ref.delete()
                return {"message": "No Access to bucket"}, 403
        else:
            return {"message": "No Access to bucket, bucket not found"}, 403

    db.collection("users").document(email).set({})
    doc_ref = (
        db.collection("users")
        .document(email)
        .collection("allowed_buckets")
        .document("example_bucket")
    )
    doc_ref.set({"time_added": datetime.datetime.utcnow()})
    return {"message": "No Access to bucket"}, 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
