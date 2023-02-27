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