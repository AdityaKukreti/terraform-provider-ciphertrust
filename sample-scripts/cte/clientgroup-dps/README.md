# Configure a CipherTrust Transparent Encryption Client Group Designated Primary Set on CipherTrust Manager

This example shows how to:
- Create a CipherTrust Transparent Encryption Client Group Designated Primary Set (DPS) on CipherTrust Manager

These steps explain how to:
- Configure CipherTrust Manager Provider parameters required to run the examples
- Configure CTE Client Group Designated Primary Set parameters required to create a DPS
- Run the example

## Configure CipherTrust Manager

### Edit the provider block in main.tf

```bash
provider "ciphertrust" {
  address  = "https://cm-address"
  username = "cm-username"
  password = "cm-password"
  domain   = "cm-domain"
  bootstrap = "no"
}
```

## Configure CTE Client Group Designated Primary Set Parameters
Edit the CTE Client Group Designated Primary Set resource in main.tf with actual values:
```bash
resource "ciphertrust_cte_clientgroup_designatedprimaryset" "dps1" {

  # ID of the client group where this designated primary set will be configured
  client_group_id = "cm-client-group-id"

  # Name of the designated primary set
  name = "cm-dps-name"

  # Comma-separated list of clients to be part of the designated primary set
  # NOTE: Must be provided as a single string and all clients MUST already
  # be part of the specified client_group_id
  client_list = "client1,client2"

  # ID/Name of LDT communication group service
  ldt_comm_group_service_id = "cm-ldt-comm-group-service-id"

}
```

## Run the Example

```bash
terraform init
terraform apply
```

## Destroy Resources
Resources must be destroyed before another sample script using the same cloud is run.

```bash
terraform destroy
```

Run this step even if the apply step fails.