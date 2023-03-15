cd platform_api
gcloud run deploy platform-api --region=europe-west3 --set-env-vars=FLASK_APP=main.py --service-account=bucket-accessor-sa@${TF_VAR_project_id}.iam.gserviceaccount.com --no-allow-unauthenticated --source .
cd ..