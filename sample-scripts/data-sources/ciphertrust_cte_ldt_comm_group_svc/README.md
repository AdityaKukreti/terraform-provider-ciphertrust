# Google Cloud Connection Data Source

This example demonstrates how the ciphertrust_ldt_comm_group_svc_list data source can be used.


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

## Configure CTE LDT comm group data source

### Edit the CTE LDT comm group data source in main.tf

```bash
# Data source for retrieving LDT CommGroup  details
data "ciphertrust_ldt_comm_group_svc_list" "example" {
  #To filter for only one LDTcomm group provide its name, this is optional
  group_name = ""
}

output "ldt_comm_groups" {
  # Output the list of LDTcomm group  retrieved from the data source
  value = "${data.ciphertrust_ldt_comm_group_svc_list.example.ldt_comm_groups}"
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