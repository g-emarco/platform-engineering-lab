import argparse
import os
import requests


def get_auth_token():
    command = "gcloud auth print-identity-token"
    result = os.popen(command).read().strip()
    return result


def get_objects(bucket_name):
    cloud_run_url = f"https://www.cool-bucket.com/buckets/"
    url = f"{cloud_run_url}/{bucket_name}"
    headers = {"Authorization": f"Bearer {get_auth_token()}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(response.json())
    else:
        print(
            f"Failed to get objects from {bucket_name}. Status code: {response.status_code}"
        )


def main():
    parser = argparse.ArgumentParser(
        description="List objects in a Google Cloud Storage bucket"
    )
    parser.add_argument(
        "--bucket-name", help="Name of the bucket to list objects from", required=True
    )
    args = parser.parse_args()

    get_objects(args.bucket_name)


if __name__ == "__main__":
    main()
