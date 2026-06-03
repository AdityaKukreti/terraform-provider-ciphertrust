package cm

import (
	"encoding/json"
	"strings"
	"testing"
)

// TestCMKeyJSON_RevocationFieldSerialization guards against the TFIN-286
// regression where CMKeyJSON.RevocationReason and CMKeyJSON.RevocationMessage
// carried each other's JSON tags, causing Create/Update to store each value in
// the wrong CipherTrust Manager API field.
func TestCMKeyJSON_RevocationFieldSerialization(t *testing.T) {
	tests := []struct {
		name        string
		in          CMKeyJSON
		wantContain []string
		wantAbsent  []string
	}{
		{
			name: "both fields set serialize to matching keys",
			in: CMKeyJSON{
				RevocationReason:  "Unspecified",
				RevocationMessage: "audit note",
			},
			wantContain: []string{
				`"revocationReason":"Unspecified"`,
				`"revocationMessage":"audit note"`,
			},
			wantAbsent: []string{
				`"revocationMessage":"Unspecified"`,
				`"revocationReason":"audit note"`,
			},
		},
		{
			name: "zero value omits both revocation keys",
			in:   CMKeyJSON{},
			wantAbsent: []string{
				"revocationReason",
				"revocationMessage",
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			b, err := json.Marshal(tt.in)
			if err != nil {
				t.Fatalf("json.Marshal returned error: %v", err)
			}
			got := string(b)
			for _, want := range tt.wantContain {
				if !strings.Contains(got, want) {
					t.Errorf("expected output to contain %q, got %s", want, got)
				}
			}
			for _, absent := range tt.wantAbsent {
				if strings.Contains(got, absent) {
					t.Errorf("expected output NOT to contain %q, got %s", absent, got)
				}
			}
		})
	}
}
