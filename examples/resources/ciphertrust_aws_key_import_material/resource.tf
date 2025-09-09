
# Create a CipherTrust AES key
resource "ciphertrust_cm_key" "new_key_material" {
  name      = "new-material"
  algorithm = "AES"
}

# Import new material to the AWS key
resource "ciphertrust_aws_key_import_material" "import_new_material" {
  key_id = "aws-key-id"
  import_key_material {
    import_type           = "NEW_KEY_MATERIAL"
    source_key_identifier = ciphertrust_cm_key.new_key_material.id
    source_key_tier       = "local"
  }
}

# The key material is now in PENDING_ROTATION state and can be made to be the CURRENT key material using a ciphertrust_aws_key_rotation resource.
resource "ciphertrust_aws_key_rotation" "rotate_imported_material" {
  key_id = ciphertrust_aws_key_import_material.import_new_material.key_id
}
