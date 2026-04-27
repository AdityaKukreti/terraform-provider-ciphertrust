terraform {
  required_providers {
    ciphertrust = {
      source  = "ThalesGroup/CipherTrust"
      version = "1.0.0-pre3"
    }
  }
}

provider "ciphertrust" {
  address  = "https://10.10.10.10"
  username = "admin"
  password = "ChangeMe101!"
}


# Create CSI Group
resource "ciphertrust_cte_csigroup" "test_csi_group" {
  name                     = "TF_CSI_GROUP"
  kubernetes_namespace     = "default"
  kubernetes_storage_class = "standard"

  description    = "tf test csi group"


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