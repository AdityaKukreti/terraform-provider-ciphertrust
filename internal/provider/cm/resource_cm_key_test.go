package cm

import (
	"encoding/json"
	"strings"
	"testing"
)

// TestCMKeyJSON_RevocationTagsMarshal asserts that the CMKeyJSON struct
// serializes RevocationReason and RevocationMessage under the correct
// CipherTrust Manager wire keys. Regression test for TFIN-286, where the
// JSON struct tags were swapped.
func TestCMKeyJSON_RevocationTagsMarshal(t *testing.T) {
	in := CMKeyJSON{
		RevocationReason:  "REASON_SENTINEL",
		RevocationMessage: "MESSAGE_SENTINEL",
	}

	out, err := json.Marshal(in)
	if err != nil {
		t.Fatalf("json.Marshal returned error: %v", err)
	}

	got := string(out)
	if !strings.Contains(got, `"revocationReason":"REASON_SENTINEL"`) {
		t.Errorf("expected revocationReason to carry the reason sentinel; got: %s", got)
	}
	if !strings.Contains(got, `"revocationMessage":"MESSAGE_SENTINEL"`) {
		t.Errorf("expected revocationMessage to carry the message sentinel; got: %s", got)
	}
}

// TestCMKeyJSON_RevocationTagsUnmarshal asserts the inverse: a CM payload using
// the correct wire keys decodes into the matching Go fields.
func TestCMKeyJSON_RevocationTagsUnmarshal(t *testing.T) {
	const payload = `{"revocationReason":"REASON_SENTINEL","revocationMessage":"MESSAGE_SENTINEL"}`

	var out CMKeyJSON
	if err := json.Unmarshal([]byte(payload), &out); err != nil {
		t.Fatalf("json.Unmarshal returned error: %v", err)
	}

	if out.RevocationReason != "REASON_SENTINEL" {
		t.Errorf("expected RevocationReason=%q, got %q", "REASON_SENTINEL", out.RevocationReason)
	}
	if out.RevocationMessage != "MESSAGE_SENTINEL" {
		t.Errorf("expected RevocationMessage=%q, got %q", "MESSAGE_SENTINEL", out.RevocationMessage)
	}
}
