# Terraform Configuration for CipherTrust Provider

# This configuration demonstrates the creation of a CTE CSIGroup resource
# with the CipherTrust provider, including setting up CTE CSIGroup details.

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

# Create CSI Group
resource "ciphertrust_cte_csigroup" "test_csi_group" {
  name                     = "TF_CSI_GROUP"

  kubernetes_namespace     = "default"

  kubernetes_storage_class = "standard"

  description    = "tf test csi group.."
 
  guard_policies = {
        test-csi1 = {},
        test-csi2 = {},
        test-csi3 = {},
  }


  ############################################################
  # Operation type to perform on the CSI Group
  #
  # IMPORTANT:
  # - This field is ONLY used during UPDATE operations
  # - It is IGNORED during the initial `terraform apply`
  #
  # Supported values:
  # - update                : Update description / client_profile
  # - add-clients           : Add clients to CSI group
  # - remove-clients        : Remove clients from CSI group
  # - update-guard-policies : Add/remove/Enable/Disable guard policies
 
  # op_type = "add-clients/remove-clients/update/update-guard-policies"

  # List of clients to operate on
  #
  # NOTE:
  # - Used ONLY for client-related operations: op_type = add-clients/remove-clients
  # - Ignored for other op_type values
  /*
  client_list = [
    "client1",   # Client name / hostname / UUID
    "client2"
  ]
  */

  # NOTE:
  # - when op_type = "update-guard-policies" (Using this op_type, we can add new policies or enable/disable/remove existing ones)
/*
 guard_policies = {
	test-csi1 = {},
	test-csi2 = {guard_enabled = false},
	test-csi3 = {},
}
*/

  # UPDATE OPERATIONS
  #
  # NOTE:
  # - Used ONLY when:
  #     op_type = "update"
  # - Only these fields are considered

/*  
  description    = "updated description"
  client_profile = "updated-profile"
*/

}

# Output the unique ID of the created CTE CSIGroup
output "cte_csigroup_id" {
    value = ciphertrust_cte_csigroup.csigroup.id
}