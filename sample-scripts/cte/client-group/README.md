# Configure a set of GuardPaths for a CipherTrust Transparent Encryption client on CipherTrust Manager

This example shows how to:
- Create a CTE ClientGroup on CM

These steps explain how to:
- Configure CipherTrust Manager Provider parameters required to run the examples
- Configure ClientGroup name and cluster type
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

## Configure CTE Client, a security policy and the corresponding guard points
Edit the configuration resource in main.tf
```bash
 resource "ciphertrust_cte_client_group" "test_cg_group_test1" {
  name = "test_cgp_1"
  cluster_type = "NON-CLUSTER"
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
