# Terraform Configuration for adding a node to an existing CipherTrust Manager cluster.
#
# Workflow:
#   1. Use ciphertrust_cluster to create the initial n-node cluster.
#   2. Use ciphertrust_cluster_node to add an additional node to that cluster at any time.

terraform {
  required_providers {
    ciphertrust = {
      source  = "ThalesGroup/CipherTrust"
      version = "1.0.0-pre3"
    }
  }
}

# Configure the provider against the primary (original) CipherTrust Manager node.
provider "ciphertrust" {
  address  = "https://10.10.10.11"
  username = "admin"
  password = "ChangeMe101!"
}

# Step 1: Create the initial 2-node cluster.
resource "ciphertrust_cluster" "cluster" {
  nodes = [
    {
      host           = "10.10.10.11"
      port           = 5432
      original       = true
      public_address = "10.10.10.11"
      credentials = {
        username = "admin"
        password = "ChangeMe101!"
      }
    },
    {
      host           = "10.10.10.12"
      port           = 5432
      original       = false
      public_address = "10.10.10.12"
      credentials = {
        username = "admin"
        password = "ChangeMe102!"
      }
    },
  ]
}

# Step 2: Add a third node to the existing cluster.
# This can be applied in the same plan as Step 1, or later in a separate apply.
# depends_on is only needed when the cluster was created in the same Terraform
# configuration (as in Step 1 above).
# If the cluster already exists and was created outside this configuration, omit depends_on entirely.
resource "ciphertrust_cluster_node" "node3" {
  depends_on = [ciphertrust_cluster.cluster]

  host           = "10.10.10.13"
  port           = 5432
  public_address = "10.10.10.13"

  # member_host is the hostname or FQDN of the existing cluster member (the
  # provider's configured node). When omitted, the provider's address is used.
  member_host = "10.10.10.11"

  # member_port is the port on the existing cluster member. Defaults to 5432.
  member_port = 5432

  credentials = {
    username = "admin"
    password = "ChangeMe103!"
  }
}

output "cluster_node_count" {
  value = ciphertrust_cluster_node.node3.node_count
}

