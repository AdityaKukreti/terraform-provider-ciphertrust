package provider

import (
	"fmt"
	"os"
	"strings"
	"testing"

	"github.com/hashicorp/terraform-plugin-testing/helper/resource"
	"github.com/hashicorp/terraform-plugin-testing/terraform"
)

type clusterNode struct {
	host, addr, public, password string
}

// checkStep wraps check functions with step-level logging so it is always
// clear which logical stage is being verified and whether it passed or failed.
func checkStep(t *testing.T, label string, checks ...resource.TestCheckFunc) resource.TestCheckFunc {
	t.Helper()
	return func(s *terraform.State) error {
		fmt.Printf("\n======== CHECK: %s ========\n", label)
		err := resource.ComposeAggregateTestCheckFunc(checks...)(s)
		if err != nil {
			fmt.Printf("======== FAILED: %s ========\n%v\n", label, err)
		} else {
			fmt.Printf("======== PASSED: %s ========\n", label)
		}
		return err
	}
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
// Each step is a single framework apply; checks run against state set by
// Create/Update, which already polls until the cluster is stable (status="r").
// Explicit RefreshState steps are omitted: the framework's pre-plan refresh
// calls Read on all existing resources before every apply, so existing resource
// state is already current when checks run against Create-set values.
//
//  1. Create 1-node cluster                          → count = 1
//  2. Add node2                                      → count = 2
//  3. Add node3                                      → count = 3
//  4. Remove node3                                   → count = 2
//  5. Swap node2 → node3 (add + remove in one apply) → count = 2
//  6. Update public_address of node3 (IP → DNS)      → count = 2
//  7. Re-add node2 (3-node state)                    → count = 3
//  8. Destroy full 3-node cluster
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

	// node2ID is captured in step 4 and compared in step 5 to confirm the
	// swap produced a genuinely new node rather than reusing the old one.
	var node2ID string

	resource.Test(t, resource.TestCase{
		ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
		Steps: []resource.TestStep{

			// Step 1: Create 1-node cluster
			{
				Config: cfgPrimary(n1Host),
				Check: checkStep(t, "Step 1: 1-node cluster created",
					resource.TestCheckResourceAttrSet("ciphertrust_cluster.primary", "id"),
					resource.TestCheckResourceAttrSet("ciphertrust_cluster.primary", "node_id"),
					resource.TestCheckResourceAttr("ciphertrust_cluster.primary", "local_node_host", n1Host),
					resource.TestCheckResourceAttr("ciphertrust_cluster.primary", "local_node_port", "5432"),
					resource.TestCheckResourceAttr("ciphertrust_cluster.primary", "status_code", "r"),
					resource.TestCheckResourceAttrSet("ciphertrust_cluster.primary", "status_description"),
				),
			},

			// Step 2: Add node2 (1 → 2)
			{
				Config: cfg2Node(n1Host, n1Public, n2, username),
				Check: checkStep(t, "Step 2: node2 joined (2-node)",
					resource.TestCheckResourceAttrSet("ciphertrust_cluster_node.node2", "id"),
					resource.TestCheckResourceAttrSet("ciphertrust_cluster_node.node2", "node_id"),
					resource.TestCheckResourceAttr("ciphertrust_cluster_node.node2", "host", n2.host),
					resource.TestCheckResourceAttr("ciphertrust_cluster_node.node2", "status_code", "r"),
				),
			},

			// Step 3: Add node3 (2 → 3)
			{
				Config: cfg3Node(n1Host, n1Public, n2, n3, username),
				Check: checkStep(t, "Step 3: node3 joined (3-node)",
					resource.TestCheckResourceAttr("ciphertrust_cluster_node.node2", "status_code", "r"),
					resource.TestCheckResourceAttrSet("ciphertrust_cluster_node.node3", "id"),
					resource.TestCheckResourceAttr("ciphertrust_cluster_node.node3", "status_code", "r"),
				),
			},

			// Step 4: Remove node3 (3 → 2)
			{
				Config: cfg2Node(n1Host, n1Public, n2, username),
				Check: checkStep(t, "Step 4: node3 removed (2-node)",
					resource.TestCheckResourceAttrSet("ciphertrust_cluster_node.node2", "id"),
					resource.TestCheckResourceAttr("ciphertrust_cluster_node.node2", "status_code", "r"),
					resource.TestCheckResourceAttrWith("ciphertrust_cluster_node.node2", "id", func(v string) error {
						node2ID = v
						return nil
					}),
				),
			},

			// Step 5: Swap node2 → node3 (simultaneous add + remove, 2 → 2)
			{
				Config: cfgPrimaryPublic(n1Host, n1Public) +
					cfgNodeBlock("node3", n3.host, n3.public, n1Host, n3.addr, username, n3.password),
				Check: checkStep(t, "Step 5: swap produced new node (2-node)",
					resource.TestCheckResourceAttrSet("ciphertrust_cluster_node.node3", "id"),
					resource.TestCheckResourceAttr("ciphertrust_cluster_node.node3", "status_code", "r"),
					resource.TestCheckResourceAttrWith("ciphertrust_cluster_node.node3", "id", func(v string) error {
						if node2ID != "" && v == node2ID {
							return fmt.Errorf("node3 ID %s matches removed node2 ID — swap did not produce a new node", v)
						}
						return nil
					}),
				),
			},

			// Step 6: Update public_address of node3 (IP → DNS)
			{
				Config: cfgPrimaryPublic(n1Host, n1Public) +
					cfgNodeBlock("node3", n3DNS.host, n3DNS.public, n1Host, n3DNS.addr, username, n3DNS.password),
				Check: checkStep(t, "Step 6: node3 public_address updated",
					resource.TestCheckResourceAttr("ciphertrust_cluster_node.node3", "public_address", n3.addr),
					resource.TestCheckResourceAttr("ciphertrust_cluster_node.node3", "status_code", "r"),
				),
			},

			// Step 7: Re-add node2 — 3-node state before teardown
			{
				Config: cfgPrimaryPublic(n1Host, n1Public) +
					cfgNodeBlock("node2", n2.host, n2.public, n1Host, n2.addr, username, n2.password) +
					cfgNodeBlock("node3", n3DNS.host, n3DNS.public, n1Host, n3DNS.addr, username, n3DNS.password),
				Check: checkStep(t, "Step 7: 3-node cluster before teardown",
					resource.TestCheckResourceAttrSet("ciphertrust_cluster_node.node2", "id"),
					resource.TestCheckResourceAttr("ciphertrust_cluster_node.node2", "status_code", "r"),
					resource.TestCheckResourceAttrSet("ciphertrust_cluster_node.node3", "id"),
					resource.TestCheckResourceAttr("ciphertrust_cluster_node.node3", "status_code", "r"),
				),
			},

			// Step 8: Destroy full 3-node cluster.
			// Applying provider-only config removes all three resources in dependency order.
			{Config: providerConfig},
		},
	})
}
