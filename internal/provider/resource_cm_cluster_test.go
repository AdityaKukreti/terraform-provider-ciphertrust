package provider

import (
	"fmt"
	"os"
	"strings"
	"testing"

	"github.com/hashicorp/terraform-plugin-testing/helper/resource"
)

type clusterNode struct {
	host, addr, public, password string
}

// printConfig prints the Terraform HCL config for a test step and returns it unchanged.
func printConfig(t *testing.T, label, cfg string) string {
	t.Helper()
	fmt.Printf("\n======== %s ========\n%s\n======== END %s ========\n", label, cfg, label)
	return cfg
}

// bareHost strips scheme and trailing slash: "https://1.2.3.4/" → "1.2.3.4".
func bareHost(address string) string {
	s := strings.TrimPrefix(address, "https://")
	s = strings.TrimPrefix(s, "http://")
	return strings.TrimSuffix(s, "/")
}

// node1Coords returns the primary node's host and public-address values.
// Skips t if CIPHERTRUST_ADDRESS is not set.
func node1Coords(t *testing.T) (host, public string) {
	t.Helper()
	address := os.Getenv("CIPHERTRUST_ADDRESS")
	if address == "" {
		t.Skip("CIPHERTRUST_ADDRESS not set; skipping cluster test")
	}
	host = os.Getenv("CLUSTER_NODE1_HOST")
	if host == "" {
		host = bareHost(address)
	}
	public = os.Getenv("CLUSTER_NODE1_PUBLIC")
	if public == "" {
		public = host
	}
	return
}

// node2Coords returns the second node's coordinates.
// Skips t if any CLUSTER_NODE2_* variable is unset.
func node2Coords(t *testing.T) clusterNode {
	t.Helper()
	n := clusterNode{
		host:     os.Getenv("CLUSTER_NODE2_HOST"),
		addr:     os.Getenv("CLUSTER_NODE2_ADDRESS"),
		public:   os.Getenv("CLUSTER_NODE2_PUBLIC"),
		password: os.Getenv("CLUSTER_NODE2_PASSWORD"),
	}
	for _, e := range []struct{ name, val string }{
		{"CLUSTER_NODE2_HOST", n.host},
		{"CLUSTER_NODE2_ADDRESS", n.addr},
		{"CLUSTER_NODE2_PUBLIC", n.public},
		{"CLUSTER_NODE2_PASSWORD", n.password},
	} {
		if e.val == "" {
			t.Skipf("%s not set; skipping test", e.name)
		}
	}
	return n
}

// node3Coords returns the third node's coordinates.
// Skips t if any CLUSTER_NODE3_* variable is unset.
func node3Coords(t *testing.T) clusterNode {
	t.Helper()
	n := clusterNode{
		host:     os.Getenv("CLUSTER_NODE3_HOST"),
		addr:     os.Getenv("CLUSTER_NODE3_ADDRESS"),
		public:   os.Getenv("CLUSTER_NODE3_PUBLIC"),
		password: os.Getenv("CLUSTER_NODE3_PASSWORD"),
	}
	for _, e := range []struct{ name, val string }{
		{"CLUSTER_NODE3_HOST", n.host},
		{"CLUSTER_NODE3_ADDRESS", n.addr},
		{"CLUSTER_NODE3_PUBLIC", n.public},
		{"CLUSTER_NODE3_PASSWORD", n.password},
	} {
		if e.val == "" {
			t.Skipf("%s not set; skipping test", e.name)
		}
	}
	return n
}

func clusterUsername() string {
	if u := os.Getenv("CIPHERTRUST_USERNAME"); u != "" {
		return u
	}
	return "admin"
}

// cfgPrimary — single-node cluster, no public_address.
func cfgPrimary(n1Host string) string {
	return providerConfig + fmt.Sprintf(`
resource "ciphertrust_cluster" "primary" {
  local_node_host = %q
  local_node_port = 5432
}
`, n1Host)
}

// cfgPrimaryPublic — single-node cluster with public_address set.
func cfgPrimaryPublic(n1Host, n1Public string) string {
	return providerConfig + fmt.Sprintf(`
resource "ciphertrust_cluster" "primary" {
  local_node_host = %q
  local_node_port = 5432
  public_address  = %q
}
`, n1Host, n1Public)
}

// cfgNodeBlock — HCL resource block for one cluster_node.
// memberHost is the primary node's internal IP (used in CM API payloads).
func cfgNodeBlock(resourceName, nodeHost, nodePublic, memberHost, nodeAddr, username, password string) string {
	return fmt.Sprintf(`
resource "ciphertrust_cluster_node" %q {
  depends_on = [ciphertrust_cluster.primary]

  host           = %q
  port           = 5432
  public_address = %q
  member_host    = %q
  member_port    = 5432

  credentials = {
    address  = %q
    username = %q
    password = %q
  }
}
`, resourceName, nodeHost, nodePublic, memberHost, nodeAddr, username, password)
}

// cfg2Node — primary + node2.
func cfg2Node(n1Host, n1Public string, n2 clusterNode, username string) string {
	return cfgPrimaryPublic(n1Host, n1Public) +
		cfgNodeBlock("node2", n2.host, n2.public, n1Host, n2.addr, username, n2.password)
}

// cfg3Node — primary + node2 + node3.
// node2 and node3 both depend_on the primary cluster but not on each other;
// the provider-level mutex (clusterJoinMu) serialises concurrent joins.
func cfg3Node(n1Host, n1Public string, n2, n3 clusterNode, username string) string {
	return cfgPrimaryPublic(n1Host, n1Public) +
		cfgNodeBlock("node2", n2.host, n2.public, n1Host, n2.addr, username, n2.password) +
		cfgNodeBlock("node3", n3.host, n3.public, n1Host, n3.addr, username, n3.password)
}

// TestResourceCMCluster runs the full cluster lifecycle as one sequential test.
// Each logical operation is two framework steps: an apply followed by a
// RefreshState that re-reads all resources from the API before assertions run.
// This ensures node_count and other async-updated attributes reflect actual
// CM state rather than the value returned by the Create/Update call.
//
//  1. Create 1-node cluster                          → count = 1
//  2. Add node2                                      → count = 2
//  3. Add node3                                      → count = 3
//  4. Remove node2 + node3 simultaneously            → count = 1
//  5. Add node2 + node3 simultaneously               → count = 3
//  6. Remove node3                                   → count = 2
//  7. Swap node2 → node3 (add + remove in one apply) → count = 2
//  8. Update public_address of node3 (IP → DNS)      → count = 2
//  9. Re-add node2 (3-node state for destroy)         → count = 3
//     framework destroys the full 3-node cluster
func TestResourceCMCluster(t *testing.T) {
	n1Host, n1Public := node1Coords(t)
	n2 := node2Coords(t)
	n3 := node3Coords(t)
	username := clusterUsername()

	// n3DNS — node3 with its DNS name used as public_address instead of its IP.
	n3DNS := clusterNode{
		host:     n3.host,
		addr:     n3.addr,
		public:   n3.addr,
		password: n3.password,
	}

	// node2ID is captured during the step-6 refresh and compared in step-7
	// refresh to confirm the swap produced a genuinely new node.
	var node2ID string

	resource.Test(t, resource.TestCase{
		ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
		Steps: []resource.TestStep{

			// ── Step 1: Create 1-node cluster ────────────────────────────────
			{Config: printConfig(t, "Step 1: Create 1-node cluster", cfgPrimary(n1Host))},
			{
				RefreshState: true,
				Check: resource.ComposeAggregateTestCheckFunc(
					resource.TestCheckResourceAttrSet("ciphertrust_cluster.primary", "id"),
					resource.TestCheckResourceAttrSet("ciphertrust_cluster.primary", "node_id"),
					resource.TestCheckResourceAttr("ciphertrust_cluster.primary", "local_node_host", n1Host),
					resource.TestCheckResourceAttr("ciphertrust_cluster.primary", "local_node_port", "5432"),
					resource.TestCheckResourceAttr("ciphertrust_cluster.primary", "node_count", "1"),
					resource.TestCheckResourceAttr("ciphertrust_cluster.primary", "status_code", "r"),
					resource.TestCheckResourceAttrSet("ciphertrust_cluster.primary", "status_description"),
				),
			},

			// ── Step 2: Add node2 (1 → 2) ────────────────────────────────────
			{Config: printConfig(t, "Step 2: Add node2 (1→2)", cfg2Node(n1Host, n1Public, n2, username))},
			{
				RefreshState: true,
				Check: resource.ComposeAggregateTestCheckFunc(
					resource.TestCheckResourceAttr("ciphertrust_cluster.primary", "node_count", "2"),
					resource.TestCheckResourceAttr("ciphertrust_cluster.primary", "status_code", "r"),
					resource.TestCheckResourceAttrSet("ciphertrust_cluster_node.node2", "id"),
					resource.TestCheckResourceAttrSet("ciphertrust_cluster_node.node2", "node_id"),
					resource.TestCheckResourceAttr("ciphertrust_cluster_node.node2", "host", n2.host),
					resource.TestCheckResourceAttr("ciphertrust_cluster_node.node2", "status_code", "r"),
					resource.TestCheckResourceAttr("ciphertrust_cluster_node.node2", "node_count", "2"),
				),
			},

			// ── Step 3: Add node3 (2 → 3) ────────────────────────────────────
			{Config: printConfig(t, "Step 3: Add node3 (2→3)", cfg3Node(n1Host, n1Public, n2, n3, username))},
			{
				RefreshState: true,
				Check: resource.ComposeAggregateTestCheckFunc(
					resource.TestCheckResourceAttr("ciphertrust_cluster.primary", "node_count", "3"),
					resource.TestCheckResourceAttr("ciphertrust_cluster.primary", "status_code", "r"),
					resource.TestCheckResourceAttrSet("ciphertrust_cluster_node.node2", "id"),
					resource.TestCheckResourceAttr("ciphertrust_cluster_node.node2", "status_code", "r"),
					resource.TestCheckResourceAttr("ciphertrust_cluster_node.node2", "node_count", "3"),
					resource.TestCheckResourceAttrSet("ciphertrust_cluster_node.node3", "id"),
					resource.TestCheckResourceAttr("ciphertrust_cluster_node.node3", "status_code", "r"),
					resource.TestCheckResourceAttr("ciphertrust_cluster_node.node3", "node_count", "3"),
				),
			},

			// ── Step 4: Remove node2 + node3 simultaneously (3 → 1) ──────────
			{Config: printConfig(t, "Step 4: Remove node2+node3 (3→1)", cfgPrimaryPublic(n1Host, n1Public))},
			{
				RefreshState: true,
				Check: resource.ComposeAggregateTestCheckFunc(
					resource.TestCheckResourceAttr("ciphertrust_cluster.primary", "node_count", "1"),
					resource.TestCheckResourceAttr("ciphertrust_cluster.primary", "status_code", "r"),
				),
			},

			// ── Step 5: Add node2 + node3 simultaneously (1 → 3) ─────────────
			{Config: printConfig(t, "Step 5: Add node2+node3 (1→3)", cfg3Node(n1Host, n1Public, n2, n3, username))},
			{
				RefreshState: true,
				Check: resource.ComposeAggregateTestCheckFunc(
					resource.TestCheckResourceAttr("ciphertrust_cluster.primary", "node_count", "3"),
					resource.TestCheckResourceAttr("ciphertrust_cluster.primary", "status_code", "r"),
					resource.TestCheckResourceAttr("ciphertrust_cluster_node.node2", "status_code", "r"),
					resource.TestCheckResourceAttr("ciphertrust_cluster_node.node3", "status_code", "r"),
				),
			},

			// ── Step 6: Remove node3 (3 → 2) ─────────────────────────────────
			{Config: printConfig(t, "Step 6: Remove node3 (3→2)", cfg2Node(n1Host, n1Public, n2, username))},
			{
				RefreshState: true,
				Check: resource.ComposeAggregateTestCheckFunc(
					resource.TestCheckResourceAttr("ciphertrust_cluster.primary", "node_count", "2"),
					resource.TestCheckResourceAttr("ciphertrust_cluster.primary", "status_code", "r"),
					resource.TestCheckResourceAttrSet("ciphertrust_cluster_node.node2", "id"),
					resource.TestCheckResourceAttr("ciphertrust_cluster_node.node2", "status_code", "r"),
					resource.TestCheckResourceAttr("ciphertrust_cluster_node.node2", "node_count", "2"),
					resource.TestCheckResourceAttrWith("ciphertrust_cluster_node.node2", "id", func(v string) error {
						node2ID = v
						return nil
					}),
				),
			},

			// ── Step 7: Swap node2 → node3 (simultaneous add + remove, 2 → 2) ─
			{
				Config: printConfig(t, "Step 7: Swap node2→node3 (2→2)",
					cfgPrimaryPublic(n1Host, n1Public)+
						cfgNodeBlock("node3", n3.host, n3.public, n1Host, n3.addr, username, n3.password)),
			},
			{
				RefreshState: true,
				Check: resource.ComposeAggregateTestCheckFunc(
					resource.TestCheckResourceAttr("ciphertrust_cluster.primary", "node_count", "2"),
					resource.TestCheckResourceAttr("ciphertrust_cluster.primary", "status_code", "r"),
					resource.TestCheckResourceAttrSet("ciphertrust_cluster_node.node3", "id"),
					resource.TestCheckResourceAttr("ciphertrust_cluster_node.node3", "status_code", "r"),
					resource.TestCheckResourceAttr("ciphertrust_cluster_node.node3", "node_count", "2"),
					resource.TestCheckResourceAttrWith("ciphertrust_cluster_node.node3", "id", func(v string) error {
						if node2ID != "" && v == node2ID {
							return fmt.Errorf("node3 ID %s matches removed node2 ID — swap did not produce a new node", v)
						}
						return nil
					}),
				),
			},

			// ── Step 8: Update public_address of node3 (IP → DNS) ────────────
			{
				Config: printConfig(t, "Step 8: Update node3 public_address (IP→DNS)",
					cfgPrimaryPublic(n1Host, n1Public)+
						cfgNodeBlock("node3", n3DNS.host, n3DNS.public, n1Host, n3DNS.addr, username, n3DNS.password)),
			},
			{
				RefreshState: true,
				Check: resource.ComposeAggregateTestCheckFunc(
					resource.TestCheckResourceAttr("ciphertrust_cluster.primary", "public_address", n1Public),
					resource.TestCheckResourceAttr("ciphertrust_cluster.primary", "status_code", "r"),
					resource.TestCheckResourceAttr("ciphertrust_cluster_node.node3", "public_address", n3.addr),
					resource.TestCheckResourceAttr("ciphertrust_cluster_node.node3", "status_code", "r"),
				),
			},

			// ── Step 9: Re-add node2 — 3-node state for full-cluster destroy ──
			{
				Config: printConfig(t, "Step 9: Re-add node2 (3-node for destroy)",
					cfgPrimaryPublic(n1Host, n1Public)+
						cfgNodeBlock("node2", n2.host, n2.public, n1Host, n2.addr, username, n2.password)+
						cfgNodeBlock("node3", n3DNS.host, n3DNS.public, n1Host, n3DNS.addr, username, n3DNS.password)),
			},
			{
				RefreshState: true,
				Check: resource.ComposeAggregateTestCheckFunc(
					resource.TestCheckResourceAttrSet("ciphertrust_cluster.primary", "id"),
					resource.TestCheckResourceAttr("ciphertrust_cluster.primary", "node_count", "3"),
					resource.TestCheckResourceAttr("ciphertrust_cluster.primary", "status_code", "r"),
					resource.TestCheckResourceAttrSet("ciphertrust_cluster_node.node2", "id"),
					resource.TestCheckResourceAttr("ciphertrust_cluster_node.node2", "status_code", "r"),
					resource.TestCheckResourceAttrSet("ciphertrust_cluster_node.node3", "id"),
					resource.TestCheckResourceAttr("ciphertrust_cluster_node.node3", "status_code", "r"),
				),
			},
			// framework destroys the 3-node cluster after the last step
		},
	})
}
