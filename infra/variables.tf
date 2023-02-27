variable "bucket_name_set" {
  description = "A set of GCS bucket names..."
  type        = list(string)
}

variable "project_id" {
  type = string
}