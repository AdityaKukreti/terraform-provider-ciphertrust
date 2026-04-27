# Configure a CipherTrust Transparent Encryption Process Set on CipherTrust Manager

This example shows how to:
- Create a CipherTrust Transparent Encryption Process Set on CipherTrust Manager

These steps explain how to:
- Configure CipherTrust Manager Provider parameters required to run the examples
- Configure CTE Process Set parameters required to create a CTE Process Set
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

## Configure CTE Process Set Parameters
Edit the CTE Process Set resource in main.tf with actual values:
```bash
resource "ciphertrust_cte_process_set" "process_set" {
    name        = "process_set_tf"
    description = "Process set test"

    processes = [
      {
        directory       = "/usr/bin"
        file            = "ls"
        resource_set_id = "cm-test"
        signature       = "demo"
        labels = {
          key1 = "value1"
        }
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