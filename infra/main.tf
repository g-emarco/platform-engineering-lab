resource "google_storage_bucket" "my_bucket_set" {
  for_each      = toset(var.bucket_name_set)
  name          = each.value
  location      = "EU"
  uniform_bucket_level_access = true
}

resource "google_storage_bucket_object" "txt_files" {
  for_each = google_storage_bucket.my_bucket_set
  name   = "some-file.txt"
  bucket = each.key
  content = "You successfully accessed a file in the bucket-${each.key}"
}

resource "google_project_service" "run_api" {
  service = "run.googleapis.com"
}


resource "google_project_service" "services" {
  for_each = toset(var.services)
  project                    = var.project_id
  service                    = each.key
}



##-----------------------------------------------------------------------

resource "google_service_account" "bucket_accessor_sa" {
  account_id   = "bucket-accessor-sa"
  display_name = "Bucket Accessor SA"
}

resource "google_project_iam_member" "token_creator_role" {
  project = var.project_id
  role = "roles/iam.serviceAccountTokenCreator"
  member = "serviceAccount:${google_service_account.bucket_accessor_sa.email}"
}

resource "google_project_iam_member" "firebase_service_agent_role" {
  project = var.project_id
  role = "roles/firebase.managementServiceAgent"
  member = "serviceAccount:${google_service_account.bucket_accessor_sa.email}"
}

resource "google_project_iam_member" "service_account_admin_role" {
  project = var.project_id
  role    = "roles/iam.serviceAccountAdmin"
  member  = "serviceAccount:${google_service_account.bucket_accessor_sa.email}"
}

resource "google_project_iam_member" "service_account_firebase_admin_role" {
  project = var.project_id
  role    = "roles/firebase.sdkAdminServiceAgent"
  member  = "serviceAccount:${google_service_account.bucket_accessor_sa.email}"
}

resource "google_project_iam_member" "cloud_build_sa_bucket_permission" {
  project = var.project_id
  role    = "roles/storage.admin"
  member  = "serviceAccount:${var.project_number}@cloudbuild.gserviceaccount.com"
}
