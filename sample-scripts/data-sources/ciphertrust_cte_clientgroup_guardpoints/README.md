# Google Cloud Connection Data Source

This example demonstrates how the ciphertrust_cte_clients_list data source can be used.


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

## Configure CTE client group guardpoints data source

### Edit the CTE client guardpoint data source in main.tf

```bash
# Data source for retrieving CTE client group guardpoints details
data "ciphertrust_cte_clientgroup_guardpoint" "example" {
    # The name filter to specify which CTE client group guardpoints to retrieve (replace with actual client names)
    clientgroup_name = ""
}

output "clientgroup_guardpoint" {
  # Output the list of CTE clientgroup guardpoints retrieved from the data source
  value = "${data.ciphertrust_cte_clientgroup_guardpoint.example.clientgroup_guardpoint}"
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