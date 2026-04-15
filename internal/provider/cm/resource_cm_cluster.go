package cm

import (
	"context"
	"encoding/json"
	"fmt"
	"net"
	"net/url"
	"strings"

	"github.com/google/uuid"
	"github.com/tidwall/gjson"

	common "github.com/ThalesGroup/terraform-provider-ciphertrust/internal/provider/common"
	"github.com/hashicorp/terraform-plugin-framework/resource"
	"github.com/hashicorp/terraform-plugin-framework/resource/schema"
	"github.com/hashicorp/terraform-plugin-framework/resource/schema/int64default"
	"github.com/hashicorp/terraform-plugin-framework/resource/schema/planmodifier"
	"github.com/hashicorp/terraform-plugin-framework/resource/schema/stringplanmodifier"
	"github.com/hashicorp/terraform-plugin-framework/types"
	"github.com/hashicorp/terraform-plugin-log/tflog"
)

var (
	_ resource.Resource              = &resourceCMCluster{}
	_ resource.ResourceWithConfigure = &resourceCMCluster{}
)

func NewResourceCMCluster() resource.Resource {
	return &resourceCMCluster{}
}

type resourceCMCluster struct {
	client *common.Client
}

func (r *resourceCMCluster) Metadata(_ context.Context, req resource.MetadataRequest, resp *resource.MetadataResponse) {
	resp.TypeName = req.ProviderTypeName + "_cluster"
}

// Schema defines the schema for the resource.
func (r *resourceCMCluster) Schema(_ context.Context, _ resource.SchemaRequest, resp *resource.SchemaResponse) {
	resp.Schema = schema.Schema{
		Description: "Initializes a new CipherTrust Manager cluster with this node as the initial member. Additional nodes can be added using ciphertrust_cluster_node resources.",
		Attributes: map[string]schema.Attribute{
			"id": schema.StringAttribute{
				Computed:    true,
				Description: "The cluster node ID.",
				PlanModifiers: []planmodifier.String{
					stringplanmodifier.UseStateForUnknown(),
				},
			},
			"local_node_host": schema.StringAttribute{
				Required:    true,
				Description: "The hostname or IP of this node. Must be reachable by all nodes in the cluster, including this one.",
				PlanModifiers: []planmodifier.String{
					stringplanmodifier.RequiresReplace(),
				},
			},
			"local_node_port": schema.Int64Attribute{
				Optional:    true,
				Computed:    true,
				Default:     int64default.StaticInt64(5432),
				Description: "The port of this node. Defaults to 5432.",
			},
			"public_address": schema.StringAttribute{
				Optional:    true,
				Description: "The fully qualified domain name (FQDN) or public IP of this node. This attribute is used by CipherTrust Manager connectors to learn how to access this particular node of the cluster remotely. Can be updated.",
			},
			"node_id": schema.StringAttribute{
				Computed:    true,
				Description: "CipherTrust Manager node ID assigned to this cluster node.",
				PlanModifiers: []planmodifier.String{
					stringplanmodifier.UseStateForUnknown(),
				},
			},
			"node_count": schema.Int64Attribute{
				Computed:    true,
				Description: "Total number of nodes in the cluster.",
			},
			"status_code": schema.StringAttribute{
				Computed:    true,
				Description: "Short cluster status code (e.g., 'r' = ready).",
			},
			"status_description": schema.StringAttribute{
				Computed:    true,
				Description: "Human-readable cluster status description.",
			},
		},
	}
}

// Create creates the resource and sets the initial Terraform state.
func (r *resourceCMCluster) Create(ctx context.Context, req resource.CreateRequest, resp *resource.CreateResponse) {
	id := uuid.New().String()
	tflog.Trace(ctx, common.MSG_METHOD_START+"[resource_cm_cluster.go -> Create]["+id+"]")

	// Retrieve values from plan
	var plan CMClusterTFSDK
	diags := req.Plan.Get(ctx, &plan)
	resp.Diagnostics.Append(diags...)
	if resp.Diagnostics.HasError() {
		return
	}

	// Build payload for POST /v1/cluster/new
	payload := NewCMClusterNodeJSON{
		LocalNodeHost: plan.LocalNodeHost.ValueString(),
		LocalNodePort: plan.LocalNodePort.ValueInt64(),
	}
	if !plan.PublicAddress.IsNull() && !plan.PublicAddress.IsUnknown() {
		payload.PublicAddress = plan.PublicAddress.ValueString()
	}

	payloadJSON, err := json.Marshal(payload)
	if err != nil {
		tflog.Debug(ctx, common.ERR_METHOD_END+err.Error()+" [resource_cm_cluster.go -> Create]["+id+"]")
		resp.Diagnostics.AddError(
			"Invalid payload for cluster creation",
			err.Error(),
		)
		return
	}

	// POST /v1/cluster/new
	response, err := r.client.PostDataV2(ctx, id, common.URL_NEW_CLUSTER, payloadJSON)
	if err != nil {
		tflog.Debug(ctx, common.ERR_METHOD_END+err.Error()+" [resource_cm_cluster.go -> Create]["+id+"]")
		resp.Diagnostics.AddError(
			"Error creating cluster on CipherTrust Manager",
			"Could not create cluster, unexpected error: "+err.Error(),
		)
		return
	}

	// Update state with response data
	nodeID := gjson.Get(response, "nodeID").String()
	plan.ID = types.StringValue(nodeID)
	plan.NodeId = types.StringValue(nodeID)
	plan.NodeCount = types.Int64Value(gjson.Get(response, "nodeCount").Int())
	plan.StatusCode = types.StringValue(gjson.Get(response, "status.code").String())
	plan.StatusDescription = types.StringValue(gjson.Get(response, "status.description").String())

	tflog.Trace(ctx, common.MSG_METHOD_END+"[resource_cm_cluster.go -> Create]["+id+"]")
	diags = resp.State.Set(ctx, plan)
	resp.Diagnostics.Append(diags...)
}

// Read refreshes the Terraform state with the latest data.
func (r *resourceCMCluster) Read(ctx context.Context, req resource.ReadRequest, resp *resource.ReadResponse) {
	var state CMClusterTFSDK
	id := uuid.New().String()

	diags := req.State.Get(ctx, &state)
	resp.Diagnostics.Append(diags...)
	if resp.Diagnostics.HasError() {
		return
	}

	// GET /v1/cluster
	response, err := r.client.ReadDataByParam(ctx, id, "", common.URL_CLUSTER_INFO)
	if err != nil {
		tflog.Debug(ctx, common.ERR_METHOD_END+err.Error()+" [resource_cm_cluster.go -> Read]["+id+"]")
		resp.Diagnostics.AddError(
			"Error reading cluster information from CipherTrust Manager",
			"Could not read cluster info, unexpected error: "+err.Error(),
		)
		return
	}

	// Update computed fields from API response
	state.NodeId = types.StringValue(gjson.Get(response, "nodeID").String())
	state.NodeCount = types.Int64Value(gjson.Get(response, "nodeCount").Int())
	state.StatusCode = types.StringValue(gjson.Get(response, "status.code").String())
	state.StatusDescription = types.StringValue(gjson.Get(response, "status.description").String())

	tflog.Trace(ctx, common.MSG_METHOD_END+"[resource_cm_cluster.go -> Read]["+id+"]")
	diags = resp.State.Set(ctx, &state)
	resp.Diagnostics.Append(diags...)
}

// Update updates the resource and sets the updated Terraform state on success.
func (r *resourceCMCluster) Update(ctx context.Context, req resource.UpdateRequest, resp *resource.UpdateResponse) {
	id := uuid.New().String()
	tflog.Trace(ctx, common.MSG_METHOD_START+"[resource_cm_cluster.go -> Update]["+id+"]")

	var plan, state CMClusterTFSDK
	resp.Diagnostics.Append(req.Plan.Get(ctx, &plan)...)
	resp.Diagnostics.Append(req.State.Get(ctx, &state)...)
	if resp.Diagnostics.HasError() {
		return
	}

	// Only public_address is updatable
	if !plan.PublicAddress.Equal(state.PublicAddress) {
		nodeID := state.NodeId.ValueString()

		// Build PATCH payload
		updatePayload := map[string]interface{}{}
		if !plan.PublicAddress.IsNull() && !plan.PublicAddress.IsUnknown() {
			updatePayload["publicAddress"] = plan.PublicAddress.ValueString()
		} else {
			// Empty string clears the public address
			updatePayload["publicAddress"] = ""
		}

		payloadJSON, err := json.Marshal(updatePayload)
		if err != nil {
			tflog.Debug(ctx, common.ERR_METHOD_END+err.Error()+" [resource_cm_cluster.go -> Update]["+id+"]")
			resp.Diagnostics.AddError("Invalid update payload", err.Error())
			return
		}

		// PATCH /v1/nodes/{id}
		_, err = r.client.UpdateDataV2(ctx, nodeID, common.URL_NODES, payloadJSON)
		if err != nil {
			tflog.Debug(ctx, common.ERR_METHOD_END+err.Error()+" [resource_cm_cluster.go -> Update]["+id+"]")
			resp.Diagnostics.AddError(
				"Error updating public_address",
				"Could not update public_address for node "+nodeID+": "+err.Error(),
			)
			return
		}

		tflog.Debug(ctx, "[resource_cm_cluster.go -> Update] Successfully updated public_address for node "+nodeID)
	}

	// Copy plan to state
	state.PublicAddress = plan.PublicAddress

	tflog.Trace(ctx, common.MSG_METHOD_END+"[resource_cm_cluster.go -> Update]["+id+"]")
	resp.Diagnostics.Append(resp.State.Set(ctx, state)...)
}

// Delete deletes the resource and removes the Terraform state on success.
func (r *resourceCMCluster) Delete(ctx context.Context, req resource.DeleteRequest, resp *resource.DeleteResponse) {
	var state CMClusterTFSDK
	diags := req.State.Get(ctx, &state)
	resp.Diagnostics.Append(diags...)
	if resp.Diagnostics.HasError() {
		return
	}

	// DELETE /v1/cluster
	// Note: This only works if this is the last/only node in the cluster
	output, err := r.client.DeleteByURL(ctx, state.NodeId.ValueString(), common.URL_CLUSTER_INFO)
	tflog.Trace(ctx, common.MSG_METHOD_END+"[resource_cm_cluster.go -> Delete]["+state.ID.ValueString()+"]["+output+"]")
	if err != nil {
		resp.Diagnostics.AddError(
			"Error deleting cluster",
			"Could not delete cluster. Ensure all additional nodes have been removed first and this is the last node in the cluster. Error: "+err.Error(),
		)
		return
	}
}

func (d *resourceCMCluster) Configure(_ context.Context, req resource.ConfigureRequest, resp *resource.ConfigureResponse) {
	if req.ProviderData == nil {
		return
	}

	client, ok := req.ProviderData.(*common.Client)
	if !ok {
		resp.Diagnostics.AddError(
			"Error in fetching client from provider",
			fmt.Sprintf("Expected *provider.Client, got: %T. Please report this issue to the provider developers.", req.ProviderData),
		)
		return
	}

	d.client = client
}

// extractHost extracts the bare hostname or IP from either a plain hostname/IP
// string or a URL string (e.g. "https://1.2.3.4/" or "https://cm.example.com").
// Both IP addresses and FQDNs are accepted as bare values.
func extractHost(input string) (string, error) {
	if strings.Contains(input, "://") {
		u, err := url.Parse(input)
		if err != nil {
			return "", fmt.Errorf("invalid URL %q: %w", input, err)
		}
		return u.Hostname(), nil
	}
	// Bare IP address.
	if net.ParseIP(input) != nil {
		return input, nil
	}
	// Bare hostname — non-empty is sufficient; the API will reject invalid values.
	if input != "" {
		return input, nil
	}
	return "", fmt.Errorf("host must not be empty")
}
