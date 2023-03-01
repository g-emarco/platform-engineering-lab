variable "bucket_name_set" {
  description = "A set of GCS bucket names..."
  type        = list(string)
}


variable services {
  type        = list(string)
  default     = [
    "artifactregistry.googleapis.com",
    "run.googleapis.com",
    "cloudbuild.googleapis.com"
  ]
}
variable "project_id" {
  type = string
}

variable "project_number" {
  type = string
}