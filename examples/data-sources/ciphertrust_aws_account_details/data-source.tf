# Declare variables for AWS credentials to avoid hardcoding sensitive values.
# Supply values via environment variables (TF_VAR_access_key_id, TF_VAR_secret_access_key),
# a secrets manager, or a .tfvars file that is excluded from version control (.gitignore).
variable "access_key_id" {
  description = "AWS access key ID. Provide via TF_VAR_access_key_id or a .tfvars file excluded from version control."
  type        = string
}

variable "secret_access_key" {
  description = "AWS secret access key. Provide via TF_VAR_secret_access_key or a .tfvars file excluded from version control."
  type        = string
  sensitive   = true
}

# Create an AWS connection
resource "ciphertrust_aws_connection" "aws_connection" {
  name              = "connection-name"
  access_key_id     = var.access_key_id
  secret_access_key = var.secret_access_key
}

# Use the connection ID to retrieve account details
data "ciphertrust_aws_account_details" "account_details" {
  aws_connection = ciphertrust_aws_connection.aws_connection.id
}

# Use the account details datasource elements to create a KMS resource
resource "ciphertrust_aws_kms" "kms" {
  account_id     = data.ciphertrust_aws_account_details.account_details.account_id
  aws_connection = ciphertrust_aws_connection.aws_connection.id
  name           = "kms-name"
  regions        = data.ciphertrust_aws_account_details.account_details.regions
}