# Create a Google service account key
# Note: Add a keepers block if periodic rotation is required
resource "google_service_account_key" "sa_key" {
  service_account_id = google_service_account.connection.name
}

# Create a connection to Google Cloud.
# key_file must point to the service account JSON file path.
# IMPORTANT: The description field must never contain key_file contents
# or any credential material. This was a provider bug (issue #23) where
# key_file contents were incorrectly written to the description field.
# Ensure you are using a provider version that includes the fix for issue #23.
#
# The private_key value from google_service_account_key is base64-encoded.
# Decode it and write to a temp file that ciphertrust_gcp_connection can reference.
# Alternatively, if the provider supports passing key content directly, prefer that.
resource "local_sensitive_file" "sa_key_file" {
  content         = base64decode(google_service_account_key.sa_key.private_key)
  filename        = "${path.module}/.tmp-gcp-key.json"
  file_permission = "0600"
}

resource "ciphertrust_gcp_connection" "gcp_connection" {
  name        = "connection-name"
  key_file    = local_sensitive_file.sa_key_file.filename
  description = "GCP connection for CipherTrust key management"
}

resource "ciphertrust_gcp_keyring" "gcp_keyring" {
  gcp_connection = ciphertrust_gcp_connection.gcp_connection.name
  name           = "keyring-name"
  project_id     = "project-id"
}

resource "ciphertrust_gcp_key" "gcp_key" {
  algorithm = "RSA_DECRYPT_OAEP_4096_SHA512"
  key_ring  = ciphertrust_gcp_keyring.gcp_keyring.id
  name      = "key-name"
}