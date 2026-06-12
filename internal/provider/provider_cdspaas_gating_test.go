package provider

import (
	"fmt"
	"io"
	"net/http"
	"net/http/httptest"
	"regexp"
	"testing"

	"github.com/hashicorp/terraform-plugin-testing/helper/resource"
)

// fakeCDSPaaSAuthServer returns an httptest server that mimics the CDSPaaS /
// CDSPaaS auth-token endpoint. It accepts any sign-in request and returns a
// fake JWT — enough for the provider to finish Configure and reach plan-time
// resource validation. The handler does not assert on the request body
// because the goal is to test plan-time gating, not the auth payload shape.
func fakeCDSPaaSAuthServer(t *testing.T) *httptest.Server {
	t.Helper()
	mux := http.NewServeMux()
	mux.HandleFunc("/api/v1/auth/tokens", func(w http.ResponseWriter, r *http.Request) {
		_, _ = io.Copy(io.Discard, r.Body)
		w.Header().Set("Content-Type", "application/json")
		_, _ = w.Write([]byte(`{"jwt":"fake-jwt-for-cdspaas-gating-test"}`))
	})
	return httptest.NewServer(mux)
}

// TestPlanTimeGating_CMOnlyResourceFailsOnCDSPaaS verifies that a CM-only
// resource (ciphertrust_ntp here) fails at terraform plan time when the
// provider is configured against a CDSPaaS deployment (i.e. tenant
// is set). It does not require TF_ACC because IsUnitTest is true and the
// auth endpoint is faked.
func TestPlanTimeGating_CMOnlyResourceFailsOnCDSPaaS(t *testing.T) {
	server := fakeCDSPaaSAuthServer(t)
	defer server.Close()

	config := fmt.Sprintf(`
provider "ciphertrust" {
  address  = %q
  username = "tenant-admin@acme.com"
  password = "ignored-by-fake-server"
  tenant   = "acme"
}

resource "ciphertrust_ntp" "x" {
  host = "time.google.com"
}
`, server.URL)

	resource.UnitTest(t, resource.TestCase{
		ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
		Steps: []resource.TestStep{{
			Config:      config,
			PlanOnly:    true,
			ExpectError: regexp.MustCompile(`Resource not supported on CDSPaaS`),
		}},
	})
}

// TestPlanTimeGating_CMOnlyResourcePassesOnCM is the negative control: the
// same gated resource MUST plan cleanly when tenant is unset (CM mode),
// confirming the gate fires only on CDSPaaS. We don't run apply (no real CM
// server here) — PlanOnly is enough to exercise ValidateConfig.
func TestPlanTimeGating_CMOnlyResourcePassesOnCM(t *testing.T) {
	server := fakeCDSPaaSAuthServer(t)
	defer server.Close()

	config := fmt.Sprintf(`
provider "ciphertrust" {
  address  = %q
  username = "admin"
  password = "ignored-by-fake-server"
}

resource "ciphertrust_ntp" "x" {
  host = "time.google.com"
}
`, server.URL)

	resource.UnitTest(t, resource.TestCase{
		ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
		Steps: []resource.TestStep{{
			Config: config,
			// PlanOnly + no ExpectError ⇒ plan must succeed without diagnostics.
			PlanOnly:           true,
			ExpectNonEmptyPlan: true,
		}},
	})
}
