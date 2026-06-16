package cckm

import (
	"context"
	"encoding/json"
	"strings"

	"github.com/ThalesGroup/terraform-provider-ciphertrust/internal/provider/cckm/utils"
	"github.com/hashicorp/terraform-plugin-framework/attr"
	"github.com/hashicorp/terraform-plugin-framework/diag"
	"github.com/hashicorp/terraform-plugin-framework/types"
	"github.com/hashicorp/terraform-plugin-log/tflog"
	"github.com/tidwall/gjson"
)

// setCommonKeyState populates the all the common read-only AWS key fields in Terraform state from an
// API response JSON string.
func setCommonKeyState(ctx context.Context, response string, state *AWSKeyCommonTFSDK, diags *diag.Diagnostics) {
	state.ARN = types.StringValue(gjson.Get(response, "aws_param.Arn").String())
	state.AWSAccountID = types.StringValue(gjson.Get(response, "aws_param.AWSAccountId").String())
	state.AWSKeyID = types.StringValue(gjson.Get(response, "aws_param.KeyID").String())
	state.CloudName = types.StringValue(gjson.Get(response, "cloud_name").String())
	state.CreatedAt = types.StringValue(gjson.Get(response, "createdAt").String())
	state.DeletionDate = types.StringValue(gjson.Get(response, "deletion_date").String())
	state.Enabled = types.BoolValue(gjson.Get(response, "aws_param.Enabled").Bool())
	state.EnableKey = types.BoolValue(gjson.Get(response, "aws_param.Enabled").Bool())
	state.EncryptionAlgorithms = utils.StringSliceJSONToListValue(gjson.Get(response, "aws_param.EncryptionAlgorithms").Array(), diags)
	state.ExpirationModel = types.StringValue(gjson.Get(response, "aws_param.ExpirationModel").String())
	state.MacAlgorithms = utils.StringSliceJSONToListValue(gjson.Get(response, "aws_param.MacAlgorithmSpec").Array(), diags)
	state.ExternalAccounts = utils.StringSliceJSONToSetValue(gjson.Get(response, "external_accounts").Array(), diags)
	state.KeyAdmins = utils.StringSliceJSONToSetValue(gjson.Get(response, "key_admins").Array(), diags)
	state.KeyAdminsRoles = utils.StringSliceJSONToSetValue(gjson.Get(response, "key_admins_roles").Array(), diags)
	state.KeyManager = types.StringValue(gjson.Get(response, "aws_param.KeyManager").String())
	state.KeyMaterialOrigin = types.StringValue(gjson.Get(response, "key_material_origin").String())
	state.KeyRotationEnabled = types.BoolValue(gjson.Get(response, "aws_param.KeyRotationEnabled").Bool())
	state.KeySource = types.StringValue(gjson.Get(response, "key_source").String())
	state.KeyState = types.StringValue(gjson.Get(response, "aws_param.KeyState").String())
	state.KeyType = types.StringValue(gjson.Get(response, "key_type").String())
	state.KeyUsers = utils.StringSliceJSONToSetValue(gjson.Get(response, "key_users").Array(), diags)
	state.KeyUsersRoles = utils.StringSliceJSONToSetValue(gjson.Get(response, "key_users_roles").Array(), diags)
	state.KMSID = types.StringValue(gjson.Get(response, "kms_id").String())
	state.KMSName = types.StringValue(gjson.Get(response, "kms").String())
	setKeyLabels(ctx, response, state.ID.ValueString(), &state.Labels, diags)
	state.Origin = types.StringValue(gjson.Get(response, "aws_param.Origin").String())
	state.Region = types.StringValue(gjson.Get(response, "region").String())
	state.RotatedAt = types.StringValue(gjson.Get(response, "rotated_at").String())
	state.RotatedFrom = types.StringValue(gjson.Get(response, "rotated_from").String())
	state.RotationStatus = types.StringValue(gjson.Get(response, "rotation_status").String())
	state.RotatedTo = types.StringValue(gjson.Get(response, "rotated_to").String())
	state.SyncedAt = types.StringValue(gjson.Get(response, "synced_at").String())
	state.UpdatedAt = types.StringValue(gjson.Get(response, "updatedAt").String())
}

// setNativeAndByokKeyCommonState populates the top-level Terraform state fields shared by
// the aws_key and aws_byok_key resources. It writes into AWSNativeAndByokKeyCommonTFSDK,
// which excludes the 12 fields that have moved into the aws_param nested block
// (arn, aws_account_id, aws_key_id, deletion_date, enabled, encryption_algorithms,
// expiration_model, key_manager, key_rotation_enabled, key_state, mac_algorithms, origin).
// The top-level policy field is also omitted; policy lives inside aws_param.
// XKS and CloudHSM keys continue to use setCommonKeyState unchanged.
func setNativeAndByokKeyCommonState(ctx context.Context, response string, state *AWSNativeAndByokKeyCommonTFSDK, diags *diag.Diagnostics) {
	keyID := gjson.Get(response, "id").String()
	state.EnableKey = types.BoolValue(gjson.Get(response, "aws_param.Enabled").Bool())
	state.CloudName = types.StringValue(gjson.Get(response, "cloud_name").String())
	state.CreatedAt = types.StringValue(gjson.Get(response, "createdAt").String())
	state.ExternalAccounts = utils.StringSliceJSONToSetValue(gjson.Get(response, "external_accounts").Array(), diags)
	state.KeyAdmins = utils.StringSliceJSONToSetValue(gjson.Get(response, "key_admins").Array(), diags)
	state.KeyAdminsRoles = utils.StringSliceJSONToSetValue(gjson.Get(response, "key_admins_roles").Array(), diags)
	state.KeyMaterialOrigin = types.StringValue(gjson.Get(response, "key_material_origin").String())
	state.KeySource = types.StringValue(gjson.Get(response, "key_source").String())
	state.KeyType = types.StringValue(gjson.Get(response, "key_type").String())
	state.KeyUsers = utils.StringSliceJSONToSetValue(gjson.Get(response, "key_users").Array(), diags)
	state.KeyUsersRoles = utils.StringSliceJSONToSetValue(gjson.Get(response, "key_users_roles").Array(), diags)
	state.KMSID = types.StringValue(gjson.Get(response, "kms_id").String())
	state.KMSName = types.StringValue(gjson.Get(response, "kms").String())
	setKeyLabels(ctx, response, keyID, &state.Labels, diags)
	state.Region = types.StringValue(gjson.Get(response, "region").String())
	state.RotatedAt = types.StringValue(gjson.Get(response, "rotated_at").String())
	state.RotatedFrom = types.StringValue(gjson.Get(response, "rotated_from").String())
	state.RotationStatus = types.StringValue(gjson.Get(response, "rotation_status").String())
	state.RotatedTo = types.StringValue(gjson.Get(response, "rotated_to").String())
	state.SyncedAt = types.StringValue(gjson.Get(response, "synced_at").String())
	state.UpdatedAt = types.StringValue(gjson.Get(response, "updatedAt").String())
}

// setCommonKeyStoreKeyState populates the common key store key fields shared by the XKS and CloudHSM key
// resources. For linked keys (linked_state = true), all AWS-facing attributes including aliases, tags,
// description, policy, and policy-template tag are refreshed from the API response. For unlinked keys,
// aliases and tags retain their prior state values, and policy_template_tag is set to null.
// Used by resourceAWSXKSKey (via setXKSKeyState) and resourceAWSCloudHSMKey.
func setCommonKeyStoreKeyState(ctx context.Context, response string, state *AWSKeyStoreKeyCommonTFSDK, diags *diag.Diagnostics) {
	linked := gjson.Get(response, "linked_state").Bool()
	// Save enable_key before setCommonKeyState overwrites it from the API.
	// For unlinked keys we restore it afterward: the API may return Enabled=true
	// for a CipherTrust-local key that has not yet been linked to AWS, which
	// would cause an "inconsistent result after apply" error when the config
	// sets enable_key = false.
	savedEnableKey := state.EnableKey
	setCommonKeyState(ctx, response, &state.AWSKeyCommonTFSDK, diags)
	if diags.HasError() {
		return
	}
	if !linked {
		state.EnableKey = savedEnableKey
	}
	// Keystore-specific input/computed fields not in AWSKeyCommonTFSDK
	state.CustomerMasterKeySpec = types.StringValue(gjson.Get(response, "aws_param.CustomerMasterKeySpec").String())
	state.KeyUsage = types.StringValue(gjson.Get(response, "aws_param.KeyUsage").String())
	state.ValidTo = types.StringValue(gjson.Get(response, "aws_param.ValidTo").String())
	// Keystore-specific fields
	state.Blocked = types.BoolValue(gjson.Get(response, "blocked").Bool())
	state.AWSCustomKeyStoreID = types.StringValue(gjson.Get(response, "aws_param.CustomKeyStoreId").String())
	state.CustomKeyStoreID = types.StringValue(gjson.Get(response, "custom_key_store_id").String())
	state.KeySourceContainerID = types.StringValue(gjson.Get(response, "key_source_container_id").String())
	state.KeySourceContainerName = types.StringValue(gjson.Get(response, "key_source_container_name").String())
	state.LocalKeyID = types.StringValue(gjson.Get(response, "local_key_id").String())
	state.LocalKeyName = types.StringValue(gjson.Get(response, "local_key_name").String())
	state.Linked = types.BoolValue(linked)

	// Extract any existing aws_param values (preserves caller-set values such as
	// alias on unlinked keys), update the relevant fields, then pack back to Object.
	p := extractAWSKeyStoreAwsParam(ctx, state.AWSParam, diags)
	if diags.HasError() {
		return
	}
	if linked {
		setAliases(response, &p.Alias, diags)
		setKeyTags(ctx, response, &p.Tags, diags)
		p.Description = types.StringValue(gjson.Get(response, "aws_param.Description").String())
		state.EnableKey = types.BoolValue(gjson.Get(response, "aws_param.Enabled").Bool())
		state.Enabled = types.BoolValue(gjson.Get(response, "aws_param.Enabled").Bool())
		policy := gjson.Get(response, "aws_param.Policy").String()
		if state.Policy.IsUnknown() || !getPoliciesAreEqual(ctx, policy, state.Policy.ValueString(), diags) {
			state.Policy = types.StringValue(policy)
		}
		p.Policy = types.StringValue(gjson.Get(response, "aws_param.Policy").String())
		setPolicyTemplateTag(ctx, response, &state.PolicyTemplateTag, diags)
	} else {
		var d diag.Diagnostics
		p.Description = types.StringValue(gjson.Get(response, "aws_param.Description").String())
		state.Enabled = types.BoolValue(gjson.Get(response, "aws_param.Enabled").Bool())
		state.PolicyTemplateTag = types.MapNull(types.StringType)
		policy := gjson.Get(response, "aws_param.Policy").String()
		state.Policy = types.StringValue(policy)
		p.Policy = types.StringValue(policy)
		if len(p.Alias.Elements()) == 0 {
			p.Alias, d = types.SetValue(types.StringType, []attr.Value{})
			if d.HasError() {
				diags.Append(d...)
			}
		}
		if len(p.Tags.Elements()) == 0 {
			tags := make(map[string]string)
			p.Tags, d = types.MapValueFrom(ctx, types.StringType, tags)
			if d.HasError() {
				diags.Append(d...)
			}
		}
	}
	state.AWSParam = packAWSKeyStoreAwsParam(ctx, p, diags)
}

// setKeyLabels parses the CipherTrust Manager labels from the API response and stores them in Terraform state.
func setKeyLabels(ctx context.Context, response string, keyID string, stateLabels *types.Map, diags *diag.Diagnostics) {
	labels := make(map[string]string)
	if gjson.Get(response, "labels").Exists() {
		labelsJSON := gjson.Get(response, "labels").Raw
		if err := json.Unmarshal([]byte(labelsJSON), &labels); err != nil {
			msg := "Error setting state for key labels, invalid data input."
			details := utils.ApiError(msg, map[string]interface{}{"error": err.Error(), "key_id": keyID})
			tflog.Error(ctx, details)
			diags.AddError(details, "")
			return
		}
	}
	labelMap, d := types.MapValueFrom(ctx, types.StringType, labels)
	if d.HasError() {
		diags.Append(d...)
		return
	}
	*stateLabels = labelMap
}

// multiRegionKeyAttrTypes defines the attr types for a single ARN/region entry
// used in multi_region_configuration.primary_key and multi_region_configuration.replica_keys.
var multiRegionKeyAttrTypes = map[string]attr.Type{
	"arn":    types.StringType,
	"region": types.StringType,
}

// multiRegionConfigAttrTypes defines the attr types for the multi_region_configuration object.
// All callers that need to construct a null or unknown object must use this map so that
// the Framework type system is satisfied.
var multiRegionConfigAttrTypes = map[string]attr.Type{
	"multi_region_key_type": types.StringType,
	"primary_key":           types.ObjectType{AttrTypes: multiRegionKeyAttrTypes},
	"replica_keys":          types.SetType{ElemType: types.ObjectType{AttrTypes: multiRegionKeyAttrTypes}},
}

// setMultiRegionConfig builds a types.Object representing multi_region_configuration
// from the API response JSON. Returns a null Object when the key is not a multi-region key.
// Any type-construction errors are appended to diags so callers can surface them.
// Used by resourceAWSKey, resourceAWSByokKey, resourceAWSKeyForImportMaterial, and the aws_key data source.
func setMultiRegionConfig(keyJSON string, diags *diag.Diagnostics) types.Object {
	if !gjson.Get(keyJSON, "aws_param.MultiRegion").Bool() {
		return types.ObjectNull(multiRegionConfigAttrTypes)
	}

	// Build primary_key object.
	primaryKeyObj, d := types.ObjectValue(multiRegionKeyAttrTypes, map[string]attr.Value{
		"arn":    types.StringValue(gjson.Get(keyJSON, "aws_param.MultiRegionConfiguration.PrimaryKey.Arn").String()),
		"region": types.StringValue(gjson.Get(keyJSON, "aws_param.MultiRegionConfiguration.PrimaryKey.Region").String()),
	})
	if d.HasError() {
		diags.Append(d...)
		return types.ObjectNull(multiRegionConfigAttrTypes)
	}

	// Build replica_keys list.
	replicaElemType := types.ObjectType{AttrTypes: multiRegionKeyAttrTypes}
	replicaElems := make([]attr.Value, 0)
	for _, r := range gjson.Get(keyJSON, "aws_param.MultiRegionConfiguration.ReplicaKeys").Array() {
		replicaObj, rd := types.ObjectValue(multiRegionKeyAttrTypes, map[string]attr.Value{
			"arn":    types.StringValue(r.Get("Arn").String()),
			"region": types.StringValue(r.Get("Region").String()),
		})
		if rd.HasError() {
			diags.Append(rd...)
			return types.ObjectNull(multiRegionConfigAttrTypes)
		}
		replicaElems = append(replicaElems, replicaObj)
	}
	replicaList, d := types.SetValue(replicaElemType, replicaElems)
	if d.HasError() {
		diags.Append(d...)
		return types.ObjectNull(multiRegionConfigAttrTypes)
	}

	cfgObj, d := types.ObjectValue(multiRegionConfigAttrTypes, map[string]attr.Value{
		"multi_region_key_type": types.StringValue(gjson.Get(keyJSON, "aws_param.MultiRegionConfiguration.MultiRegionKeyType").String()),
		"primary_key":           primaryKeyObj,
		"replica_keys":          replicaList,
	})
	if d.HasError() {
		diags.Append(d...)
		return types.ObjectNull(multiRegionConfigAttrTypes)
	}
	return cfgObj
}

// setKeyTags populates the user-managed tags in state from the AWS response.
// If stateTags already contains a known set of keys (from the plan or prior state), only response
// tags whose keys are present in stateTags are stored. This prevents AWS-policy-added tags (e.g.
// an organisation-wide "owner" tag) from causing "inconsistent result after apply" errors when
// those tags are not in the Terraform config. On first use (null or unknown state, e.g. import),
// all response tags are stored as-is.
func setKeyTags(ctx context.Context, response string, stateTags *types.Map, diags *diag.Diagnostics) {
	// Read all user-visible tags from the response (exclude internal policy-template tag).
	allTags := make(map[string]string)
	for _, tag := range gjson.Get(response, "aws_param.Tags").Array() {
		tagKey := gjson.Get(tag.Raw, "TagKey").String()
		tagValue := gjson.Get(tag.Raw, "TagValue").String()
		if tagKey != policyTemplateTagKey {
			allTags[tagKey] = tagValue
		}
	}

	// When stateTags is already a known map (plan value or prior state), filter to only those keys.
	// An empty but known map (user set tags = {}) results in an empty filtered map - correct behaviour.
	filteredTags := allTags
	if !stateTags.IsNull() && !stateTags.IsUnknown() {
		priorKeys := stateTags.Elements()
		filteredTags = make(map[string]string, len(priorKeys))
		for k := range priorKeys {
			if v, ok := allTags[k]; ok {
				filteredTags[k] = v
			}
		}
	}

	tagMap, d := types.MapValueFrom(ctx, types.StringType, filteredTags)
	if d.HasError() {
		diags.Append(d...)
		return
	}
	*stateTags = tagMap
}

// setAliases parses alias values from the API response JSON and stores them in the Terraform state set.
func setAliases(response string, stateAlias *types.Set, diags *diag.Diagnostics) {
	var aliases []attr.Value
	aliasesJSON := gjson.Get(response, "aws_param.Alias").Array()
	for _, item := range aliasesJSON {
		alias := item.String()
		if strings.Contains(alias, "alias/") {
			alias = alias[len("alias/"):]
		}
		aliases = append(aliases, types.StringValue(alias))
	}
	aliasSet, d := types.SetValue(types.StringType, aliases)
	if d.HasError() {
		diags.Append(d...)
		return
	}
	*stateAlias = aliasSet
}
