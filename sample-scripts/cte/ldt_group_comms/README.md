# Configure a CipherTrust Transparent Encryption LDT Communication Group on CipherTrust Manager

This example shows how to:
- Create a CipherTrust Transparent Encryption LDT Communication Group on CipherTrust Manager

These steps explain how to:
- Configure CipherTrust Manager Provider parameters required to run the examples
- Configure CTE LDT Communication Group parameters required to create a CTE LDT Communication Group
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

## Configure CTE LDT Communication Group Parameters
Edit the CTE LDT Communication Group resource in main.tf with actual values:
```bash
resource "ciphertrust_cte_ldtgroupcomms" "lgs" {
  name        = "test_lgs"
  description = "Testing ldt comm group using Terraform"

  # Comma-separated list of clients to be part of the LDT communication group
  # NOTE: All clients listed here must already be registered with CipherTrust Manager
  client_list = ["client1,client2"]
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