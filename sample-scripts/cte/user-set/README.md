# Configure a CipherTrust Transparent Encryption User Set on CipherTrust Manager

This example shows how to:
- Create a CipherTrust Transparent Encryption User Set on CipherTrust Manager

These steps explain how to:
- Configure CipherTrust Manager Provider parameters required to run the examples
- Configure CTE User Set parameters required to create a CTE User Set
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

## Configure CTE User Set Parameters
Edit the CTE User Set resource in main.tf with actual values:
```bash
resource "ciphertrust_cte_user_set" "user_set" {
    name        = "User_set_tf"
    description = "UserSet Terraform"

    labels = {
      key1 = "value1"
      key2 = "value2"
    }

    users = [
      {
        uname = "john.doe"
        uid   = 1000
        gname = "sudo"
        gid   = 0
      },
      {
        uname = "test.user"
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