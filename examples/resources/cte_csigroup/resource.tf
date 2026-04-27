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

resource "ciphertrust_cte_csigroup" "test_csi_group" {
  name                     = "TF_CSI_GROUP"
  kubernetes_namespace     = "default"
  kubernetes_storage_class = "standard"

  description    = "tf test csi group"


# Create CSI Group
  ############################################################
  # Operation type to perform on the CSI Group
  #
  # IMPORTANT:
  # - This field is ONLY used during UPDATE operations
  # - It is IGNORED during the initial `terraform apply`
  #
  # Supported values:
  # - update               : Update description / client_profile
  # - add-clients          : Add clients to CSI group
  # - remove-client        : Remove a client from CSI group
  # - add-guard-policies   : Add guard policies to CSI group
  # - update-guard-policy  : Enable/Disable guard policies
  # - remove-guard-policy  : Remove guard policies
  #
  # op_type = "add-clients/remove-client/update/add-guard-policies/update-guard-policy/remove-guard-policy"

  # List of clients to operate on
  #
  # NOTE:
  # - Used ONLY for client-related operation: op_type = add-clients
  # - Ignored for other op_type values
  /*
  client_list = [
    "client1",   # Client name / hostname / UUID
    "client2"
  ]
  */

  #
  # NOTE:
  # - Used ONLY when:
  #     op_type = "remove-client"
  # - Provide SINGLE client_id

  # client_id = "client1"



  # NOTE:
  # - Used ONLY for policy-related operation: op_type = add-guard-policies
  # - Ignored for other op_type values

  /*
  policy_list = [
    "policy1",   # Policy name or ID
    "policy2"
  ]
  */

  # UPDATE OPERATIONS
  #
  # NOTE:
  # - Used ONLY when:
  #     op_type = "update"
  # - Only these fields are considered
  
  # description    = "updated description"
  # client_profile = "updated-profile"


  # GUARD POLICY UPDATE
  #
  # NOTE:
  # - Used ONLY when:
  #     op_type = "update-guard-policy"

  # guard_enabled = true


}

# Output the unique ID of the created CTE CSIGroup
output "cte_csigroup_id" {
    value = ciphertrust_cte_csigroup.csigroup.id
}