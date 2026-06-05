# Configure a CipherTrust Transparent Encryption Signature Set on CipherTrust Manager

This example shows how to:
- Create a CipherTrust Transparent Encryption Signature Set on CipherTrust Manager

These steps explain how to:
- Configure CipherTrust Manager Provider parameters required to run the examples
- Configure CTE Signature Set parameters required to create a CTE Signature Set
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

## Configure CTE Signature Set Parameters
Edit the CTE Signature Set resource in main.tf with actual values:
```bash
resource "ciphertrust_cte_signature_set" "signature_set" {
    name        = "signature_set_tf"
    description = "SignatureSet Terraform"

    labels = {
      key1 = "value1"
      key2 = "value2"
    }

    source_list = [
      "/usr/sbin/ls",
    ]

    type = "Application"
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