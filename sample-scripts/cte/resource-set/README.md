# Configure a CipherTrust Transparent Encryption Resource Set on CipherTrust Manager

This example shows how to:
- Create a CipherTrust Transparent Encryption Resource Set on CipherTrust Manager

These steps explain how to:
- Configure CipherTrust Manager Provider parameters required to run the examples
- Configure CTE Resource Set parameters required to create a CTE Resource Set
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

## Configure CTE Resource Set Parameters
Edit the CTE Resource Set resource in main.tf with actual values:
```bash
resource "ciphertrust_cte_resource_set" "resource_set" {
    name        = "resource_set_tf"
    description = "ResourceSet Terraform"

    labels = {
      key1 = "value1"
      key2 = "value2"
    }

    resources = [
      {
        directory          = "/opt/temp1"
        file               = "file1.txt"
        include_subfolders = true
        hdfs               = false
      }
    ]
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