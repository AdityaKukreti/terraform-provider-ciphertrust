# Example: Create a custom keystore and retrieve its details via data source

resource "ciphertrust_aws_connection" "aws_connection" {
  name = "aws-connection-example"
}

resource "ciphertrust_aws_kms" "kms" {
  aws_connection = ciphertrust_aws_connection.aws_connection.id
  name           = "aws-kms-example"
}

resource "ciphertrust_aws_custom_keystore" "custom_keystore" {
  aws_kms_id         = ciphertrust_aws_kms.kms.id
  name               = "example-custom-keystore"
  region             = "us-east-1"
  custom_key_store_type = "EXTERNAL_KEY_STORE"
}

# Retrieve details of the custom keystore using its Terraform resource ID
data "ciphertrust_aws_custom_keystore" "by_resource_id" {
  id = ciphertrust_aws_custom_keystore.custom_keystore.id

  depends_on = [ciphertrust_aws_custom_keystore.custom_keystore]
}