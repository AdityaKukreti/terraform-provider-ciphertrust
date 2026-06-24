# Example: Create a custom keystore and retrieve its details via data source

resource "ciphertrust_aws_custom_keystore" "custom_keystore" {
  name           = "example-custom-keystore"
  region         = "us-east-1"
  # Add required attributes per your CipherTrust Manager configuration
}

# Retrieve details using the resource ID
data "ciphertrust_aws_custom_keystore" "by_resource_id" {
  id = ciphertrust_aws_custom_keystore.custom_keystore.id
}