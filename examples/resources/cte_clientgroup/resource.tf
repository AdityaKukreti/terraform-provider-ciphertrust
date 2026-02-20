# Terraform Configuration for CipherTrust Provider

# This configuration demonstrates the creation of a CTE guardpoint resource
# with the CipherTrust provider, including setting up guardpoint details.

terraform {
  # Define the required providers for the configuration
  required_providers {
    # CipherTrust provider for managing CipherTrust resources
    ciphertrust = {
      # The source of the provider
      source = "ThalesGroup/CipherTrust"
      # Version of the provider to use
      version = "1.0.0-pre3"
    }
  }
}

# Configure the CipherTrust provider for authentication
provider "ciphertrust" {
	# The address of the CipherTrust appliance (replace with the actual address)
  address = "https://10.10.10.10"

  # Username for authenticating with the CipherTrust appliance
  username = "admin"

  # Password for authenticating with the CipherTrust appliance
  password = "ChangeMe101!"
}

# Add a resource of type CTE  Client Group
resource "ciphertrust_cte_client_group" "test_cg_group_test1" {
  name = "test_cgp_1"
  cluster_type = "NON-CLUSTER"
}

# Output the unique ID of the created CTE Client Group
output "cte_client_group_id" {
    value = ciphertrust_cte_client_group.test_cg_group_test1.id
}