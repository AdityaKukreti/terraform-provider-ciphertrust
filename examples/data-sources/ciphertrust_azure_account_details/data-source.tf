# Sensitive credentials — supply via TF_VAR_* environment variables or a secrets manager.
# Never hardcode real values in .tf files or commit them to source control.
#
# Example (Linux/macOS):
#   export TF_VAR_client_id="your-client-id"
#   export TF_VAR_client_secret="your-client-secret"
#   export TF_VAR_tenant_id="your-tenant-id"

variable "client_id" {
  description = "Azure service principal client ID."
  type        = string
}

variable "client_secret" {
  description = "Azure service principal client secret. Supply via TF_VAR_client_secret or a secrets manager — never as a literal value in source-controlled files."
  type        = string
  sensitive   = true
}

variable "tenant_id" {
  description = "Azure Active Directory tenant ID."
  type        = string
}

# Create an Azure connection
resource "ciphertrust_azure_connection" "azure_connection" {
  name          = "connection-name"
  client_id     = var.client_id
  client_secret = var.client_secret
  tenant_id     = var.tenant_id
}

data "ciphertrust_azure_account_details" "subscriptions" {
  azure_connection = ciphertrust_azure_connection.azure_connection.name
}

resource "ciphertrust_azure_vault" "azure_vault" {
  azure_connection = ciphertrust_azure_connection.azure_connection.name
  subscription_id  = data.ciphertrust_azure_account_details.subscriptions.subscription_id
  name             = "azure-vault"
}