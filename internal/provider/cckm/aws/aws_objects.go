package cckm

// aws_objects.go centralises all Framework attr.Type maps and typed Object
// conversion helpers (FromObject / ToObject / extract / pack) for the AWS key
// nested blocks.  Having them in one file makes it easy to grep for the
// definition of any type map or helper without hunting across multiple resource
// files.

import (
	"context"

	"github.com/hashicorp/terraform-plugin-framework/attr"
	"github.com/hashicorp/terraform-plugin-framework/diag"
	"github.com/hashicorp/terraform-plugin-framework/types"
	"github.com/hashicorp/terraform-plugin-framework/types/basetypes"
)

// ---------------------------------------------------------------------------
// XKS / CloudHSM key store aws_param
// ---------------------------------------------------------------------------

// keyStoreAwsParamAttrTypes defines the Framework attribute types for
// AWSKeyStoreAwsParamTFSDK. Used when constructing or extracting a types.Object
// for the aws_param nested block of aws_xks_key and aws_cloudhsm_key.
var keyStoreAwsParamAttrTypes = map[string]attr.Type{
	"alias":       types.SetType{ElemType: types.StringType},
	"description": types.StringType,
	"policy":      types.StringType,
	"tags":        types.MapType{ElemType: types.StringType},
}

// extractAWSKeyStoreAwsParam extracts an AWSKeyStoreAwsParamTFSDK from a
// types.Object. Returns a zero-value struct (with null fields) if the object
// is null or unknown.
func extractAWSKeyStoreAwsParam(ctx context.Context, obj types.Object, diags *diag.Diagnostics) AWSKeyStoreAwsParamTFSDK {
	var p AWSKeyStoreAwsParamTFSDK
	if obj.IsNull() || obj.IsUnknown() {
		return p
	}
	d := obj.As(ctx, &p, basetypes.ObjectAsOptions{UnhandledNullAsEmpty: true, UnhandledUnknownAsEmpty: true})
	if d.HasError() {
		diags.Append(d...)
	}
	return p
}

// packAWSKeyStoreAwsParam packs an AWSKeyStoreAwsParamTFSDK into a types.Object.
// On error, appends to diags and returns a null object.
func packAWSKeyStoreAwsParam(ctx context.Context, p AWSKeyStoreAwsParamTFSDK, diags *diag.Diagnostics) types.Object {
	obj, d := types.ObjectValueFrom(ctx, keyStoreAwsParamAttrTypes, p)
	if d.HasError() {
		diags.Append(d...)
		return types.ObjectNull(keyStoreAwsParamAttrTypes)
	}
	return obj
}

// ---------------------------------------------------------------------------
// Native (AWS_KMS) and BYOK (EXTERNAL) key aws_param - shared base type map
// ---------------------------------------------------------------------------

// commonAwsParamAttrTypes is the attr.Type map for the aws_param fields shared
// by both the aws_key and aws_byok_key resources. Use this as a base when
// building the full attr.Type map for each resource's aws_param block.
var commonAwsParamAttrTypes = map[string]attr.Type{
	"alias":                              types.SetType{ElemType: types.StringType},
	"arn":                                types.StringType,
	"aws_account_id":                     types.StringType,
	"aws_key_id":                         types.StringType,
	"bypass_policy_lockout_safety_check": types.BoolType,
	"current_key_material_id":            types.StringType,
	"customer_master_key_spec":           types.StringType,
	"deletion_date":                      types.StringType,
	"description":                        types.StringType,
	"enabled":                            types.BoolType,
	"encryption_algorithms":              types.ListType{ElemType: types.StringType},
	"expiration_model":                   types.StringType,
	"key_manager":                        types.StringType,
	"key_rotation_enabled":               types.BoolType,
	"key_state":                          types.StringType,
	"key_usage":                          types.StringType,
	"mac_algorithms":                     types.ListType{ElemType: types.StringType},
	"multi_region":                       types.BoolType,
	"origin":                             types.StringType,
	"policy":                             types.StringType,
	"replica_policy":                     types.StringType,
	"replica_tags":                       types.StringType,
	"tags":                               types.MapType{ElemType: types.StringType},
}

// ---------------------------------------------------------------------------
// Native key (aws_key) aws_param
// ---------------------------------------------------------------------------

// nativeKeyAwsParamAttrTypes is the attr.Type map for the aws_param block of
// the aws_key resource. It extends commonAwsParamAttrTypes with two
// additional fields that only apply to native (AWS_KMS) keys:
//   - auto_rotation_period_in_days: Optional/Computed rotation period in days
//   - next_rotation_date: Computed date of the next scheduled AWS auto-rotation
var nativeKeyAwsParamAttrTypes = func() map[string]attr.Type {
	m := make(map[string]attr.Type, len(commonAwsParamAttrTypes)+2)
	for k, v := range commonAwsParamAttrTypes {
		m[k] = v
	}
	m["auto_rotation_period_in_days"] = types.Int64Type
	m["next_rotation_date"] = types.StringType
	return m
}()

// nativeKeyAwsParamFromObject decodes a types.Object plan/state value into
// *AWSKeyAwsParamTFSDK. Returns nil when the object is null or unknown
// (aws_param was not set in config or not yet known).
func nativeKeyAwsParamFromObject(ctx context.Context, obj types.Object, diags *diag.Diagnostics) *AWSKeyAwsParamTFSDK {
	if obj.IsNull() || obj.IsUnknown() {
		return nil
	}
	var p AWSKeyAwsParamTFSDK
	diags.Append(obj.As(ctx, &p, basetypes.ObjectAsOptions{})...)
	return &p
}

// nativeKeyAwsParamToObject converts *AWSKeyAwsParamTFSDK to a types.Object
// for storage in state. Returns a typed null object when p is nil.
func nativeKeyAwsParamToObject(ctx context.Context, p *AWSKeyAwsParamTFSDK, diags *diag.Diagnostics) types.Object {
	if p == nil {
		return types.ObjectNull(nativeKeyAwsParamAttrTypes)
	}
	obj, d := types.ObjectValueFrom(ctx, nativeKeyAwsParamAttrTypes, p)
	diags.Append(d...)
	return obj
}

// ---------------------------------------------------------------------------
// BYOK key (aws_byok_key) aws_param
// ---------------------------------------------------------------------------

// byokAwsParamAttrTypes is the attr.Type map for the aws_param block of the
// aws_byok_key resource. It extends commonAwsParamAttrTypes with one
// additional field:
//   - valid_to: Optional/Computed expiry date for key material
//
// Note: auto_rotation_period_in_days and next_rotation_date are NOT included
// here because AWS cannot automatically rotate EXTERNAL-origin (BYOK) keys -
// they require customer-supplied key material and do not support on-demand
// AWS auto-rotation.
var byokAwsParamAttrTypes = func() map[string]attr.Type {
	m := make(map[string]attr.Type, len(commonAwsParamAttrTypes)+1)
	for k, v := range commonAwsParamAttrTypes {
		m[k] = v
	}
	m["valid_to"] = types.StringType
	return m
}()

// byokAwsParamFromObject decodes a types.Object plan/state value into
// *AWSByokAwsParamTFSDK. Returns nil when the object is null or unknown
// (aws_param was not set in config or not yet known).
func byokAwsParamFromObject(ctx context.Context, obj types.Object, diags *diag.Diagnostics) *AWSByokAwsParamTFSDK {
	if obj.IsNull() || obj.IsUnknown() {
		return nil
	}
	var p AWSByokAwsParamTFSDK
	diags.Append(obj.As(ctx, &p, basetypes.ObjectAsOptions{})...)
	return &p
}

// byokAwsParamToObject converts *AWSByokAwsParamTFSDK to a types.Object for
// storage in state. Returns a typed null object when p is nil.
func byokAwsParamToObject(ctx context.Context, p *AWSByokAwsParamTFSDK, diags *diag.Diagnostics) types.Object {
	if p == nil {
		return types.ObjectNull(byokAwsParamAttrTypes)
	}
	obj, d := types.ObjectValueFrom(ctx, byokAwsParamAttrTypes, p)
	diags.Append(d...)
	return obj
}
