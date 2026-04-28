package cckm

import "encoding/json"

// redactOCIResponse returns a version of a CipherTrust Manager OCI API response
// JSON that is safe to write to debug logs. Sensitive fields are replaced with
// the string "redacted". The original response string is never modified; all
// changes are made on an in-memory copy produced by JSON round-tripping.
//
// Fields redacted at the top level:
//
//	vault_id       -- the OCI vault OCID; identifies the customer's vault in OCI
//	tenancy        -- the OCI tenancy name; identifies the customer's tenancy
//	wrappingkey_id -- OCID of the vault's wrapping key (vault responses only)
//	compartment_id -- OCID of the OCI compartment (vault responses carry this at the top level;
//	                  key responses carry it inside oci_params)
//	freeform_tags  -- user-defined key:value pairs (vault responses carry this at the top level;
//	                  key responses carry it inside oci_params)
//	defined_tags   -- namespace-scoped tags (vault responses carry this at the top level;
//	                  key responses carry it inside oci_params)
//
// Fields redacted inside oci_params:
//
//	compartment_id      -- OCID of the OCI compartment
//	current_key_version -- OCID of the key's current version
//	key_id              -- OCID of the key itself
//	freeform_tags       -- user-defined key:value pairs; may contain sensitive info
//	defined_tags        -- namespace-scoped tags; may contain sensitive info
//
// Fields redacted inside oci_key_version_params:
//
//	compartment_id -- OCID of the OCI compartment
//	key_id         -- OCID of the parent key
//	vault_id       -- OCID of the vault containing the key version
//	version_id     -- OCID of the key version itself
//	freeform_tags  -- user-defined key:value pairs; may contain sensitive info
//	defined_tags   -- namespace-scoped tags; may contain sensitive info
func redactOCIResponse(response string) string {
	var data map[string]interface{}
	if err := json.Unmarshal([]byte(response), &data); err != nil {
		// If we cannot parse the response, return it as-is - a malformed response
		// is itself useful diagnostic information.
		return response
	}

	for _, field := range []string{
		"vault_id", "tenancy",
		// vault responses carry these at the top level (not nested in oci_params)
		"wrappingkey_id", "compartment_id", "freeform_tags", "defined_tags",
	} {
		if _, ok := data[field]; ok {
			data[field] = "redacted"
		}
	}

	if ociParams, ok := data["oci_params"].(map[string]interface{}); ok {
		for _, field := range []string{
			"compartment_id", "current_key_version", "key_id",
			"freeform_tags", "defined_tags",
		} {
			if _, ok := ociParams[field]; ok {
				ociParams[field] = "redacted"
			}
		}
	}

	if ociVersionParams, ok := data["oci_key_version_params"].(map[string]interface{}); ok {
		for _, field := range []string{
			"compartment_id", "key_id", "vault_id", "version_id",
			"freeform_tags", "defined_tags",
		} {
			if _, ok := ociVersionParams[field]; ok {
				ociVersionParams[field] = "redacted"
			}
		}
	}

	b, err := json.Marshal(data)
	if err != nil {
		return response
	}
	return string(b)
}
