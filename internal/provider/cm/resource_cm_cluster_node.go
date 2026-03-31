package cm

import (
	"context"
	"encoding/json"
	"fmt"
	"strings"
	"time"

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
	_ resource.Resource              = &resourceCMClusterNode{}
	_ resource.ResourceWithConfigure = &resourceCMClusterNode{}
)

func NewResourceCMClusterNode() resource.Resource {
	return &resourceCMClusterNode{}
}

type resourceCMClusterNode struct {
	client *common.Client
}

func (r *resourceCMClusterNode) Metadata(_ context.Context, req resource.MetadataRequest, resp *resource.MetadataResponse) {
	resp.TypeName = req.ProviderTypeName + "_cluster_node"
}

func (r *resourceCMClusterNode) Schema(_ context.Context, _ resource.SchemaRequest, resp *resource.SchemaResponse) {
	resp.Schema = schema.Schema{
		Description: "Adds a single node to an existing CipherTrust Manager cluster. The provider's configured address is used as the existing cluster member for signing the join request.",
		Attributes: map[string]schema.Attribute{
			"id": schema.StringAttribute{
				Computed: true,
				PlanModifiers: []planmodifier.String{
					stringplanmodifier.UseStateForUnknown(),
				},
			},
			"host": schema.StringAttribute{
				Required:    true,
				Description: "Hostname or IP address of the node to add to the cluster.",
			},
			"port": schema.Int64Attribute{
				Required:    true,
				Description: "Port of the node to add, typically 5432.",
			},
			"public_address": schema.StringAttribute{
				Required:    true,
				Description: "FQDN or public IP of the new node. Used by CipherTrust Manager connectors to reach this node remotely.",
			},
			"credentials": schema.SingleNestedAttribute{
				Optional:    true,
				Description: "Credentials for the new node. If omitted, the provider's configured credentials are used.",
				Attributes: map[string]schema.Attribute{
					"username": schema.StringAttribute{
						Optional:    true,
						Description: "Username for the new node.",
					},
					"password": schema.StringAttribute{
						Optional:    true,
						Sensitive:   true,
						Description: "Password for the new node.",
					},
					"domain": schema.StringAttribute{
						Optional:    true,
						Description: "CipherTrust domain to log in to on the new node. Default is the root domain.",
					},
					"auth_domain": schema.StringAttribute{
						Optional:    true,
						Description: "CipherTrust authentication domain of the user on the new node.",
					},
					"no_ssl_verify": schema.BoolAttribute{
						Optional:    true,
						Description: "Set to false to verify the server's certificate chain and host name.",
					},
				},
			},
			"member_host": schema.StringAttribute{
				Optional:    true,
				Description: "Hostname or FQDN of the existing cluster member. If omitted, the provider's configured address is used. Use an FQDN (e.g. ec2-1-2-3-4.compute-1.amazonaws.com) to match the member node's TLS certificate.",
			},
			"member_port": schema.Int64Attribute{
				Optional:    true,
				Computed:    true,
				Default:     int64default.StaticInt64(5432),
				Description: "Port of the existing cluster member (the provider's configured node). Defaults to 5432.",
			},
			"node_id": schema.StringAttribute{
				Computed:    true,
				Description: "CipherTrust Manager node ID assigned to the new node after joining the cluster.",
				PlanModifiers: []planmodifier.String{
					stringplanmodifier.UseStateForUnknown(),
				},
			},
			"node_count": schema.Int64Attribute{
				Computed:    true,
				Description: "Total number of nodes in the cluster after this node has joined.",
			},
			"status_code": schema.StringAttribute{
				Computed:    true,
				Description: "Short cluster status code (e.g. 'r' = ready).",
			},
			"status_description": schema.StringAttribute{
				Computed:    true,
				Description: "Human-readable cluster status description.",
			},
		},
	}
}

// Create joins a new node to the existing cluster using the three-step CSR workflow.
func (r *resourceCMClusterNode) Create(ctx context.Context, req resource.CreateRequest, resp *resource.CreateResponse) {
	id := uuid.New().String()
	tflog.Trace(ctx, common.MSG_METHOD_START+"[resource_cm_cluster_node.go -> Create]["+id+"]")

	var plan CMAddClusterNodeTFSDK
	diags := req.Plan.Get(ctx, &plan)
	resp.Diagnostics.Append(diags...)
	if resp.Diagnostics.HasError() {
		return
	}

	joiningNodeHost, err := extractHost(plan.Host.ValueString())
	if err != nil {
		resp.Diagnostics.AddError("Invalid host for joining node", err.Error())
		return
	}
	joiningNodePubAddress, err := extractHost(plan.PublicAddress.ValueString())
	if err != nil {
		resp.Diagnostics.AddError("Invalid public_address for joining node", err.Error())
		return
	}

	// Use node-specific credentials if provided, otherwise fall back to the provider's credentials.
	nodeUsername := r.client.AuthData.Username
	nodePassword := r.client.AuthData.Password
	nodeDomain := r.client.AuthData.Domain
	nodeAuthDomain := r.client.AuthData.AuthDomain
	if plan.Creds != nil {
		if !plan.Creds.Username.IsNull() && !plan.Creds.Username.IsUnknown() {
			nodeUsername = plan.Creds.Username.ValueString()
		}
		if !plan.Creds.Password.IsNull() && !plan.Creds.Password.IsUnknown() {
			nodePassword = plan.Creds.Password.ValueString()
		}
		if !plan.Creds.Domain.IsNull() && !plan.Creds.Domain.IsUnknown() {
			nodeDomain = plan.Creds.Domain.ValueString()
		}
		if !plan.Creds.AuthDomain.IsNull() && !plan.Creds.AuthDomain.IsUnknown() {
			nodeAuthDomain = plan.Creds.AuthDomain.ValueString()
		}
	}

	nodeURL := "https://" + joiningNodeHost
	nodeClient, err := common.NewClient(ctx, id, &nodeURL, &nodeAuthDomain, &nodeDomain, &nodeUsername, &nodePassword, true, 180)
	if err != nil {
		tflog.Debug(ctx, common.ERR_METHOD_END+err.Error()+" [resource_cm_cluster_node.go -> Create]["+id+"]")
		resp.Diagnostics.AddError("Unable to create HTTPS client for the joining node.", err.Error())
		return
	}

	// Step 1: Generate a CSR on the joining node.
	payloadCSR := NewCSRJSON{
		LocalNodeHost: joiningNodeHost,
		PublicAddress: joiningNodePubAddress,
	}
	payloadCSRJSON, err := json.Marshal(payloadCSR)
	if err != nil {
		resp.Diagnostics.AddError("Invalid payload: Create CSR", err.Error())
		return
	}
	responseCSR, err := nodeClient.PostDataV2(ctx, id, common.URL_CREATE_CSR, payloadCSRJSON)
	if err != nil {
		tflog.Debug(ctx, common.ERR_METHOD_END+err.Error()+" [resource_cm_cluster_node.go -> Create]["+id+"]")
		resp.Diagnostics.AddError("Error creating CSR on the joining node: ", err.Error())
		return
	}

	// Step 2: Sign the CSR on the existing cluster member (provider's configured node).
	// Retry when consensus is temporarily unavailable after a recent node join.
	payloadSignCSR := SignRequestJSON{
		CSR:                gjson.Get(responseCSR, "csr").String(),
		NewNodeHost:        joiningNodeHost,
		PublicAddress:      joiningNodePubAddress,
		SharedHSMPartition: false,
	}
	payloadSignCSRJSON, err := json.Marshal(payloadSignCSR)
	if err != nil {
		resp.Diagnostics.AddError("Invalid payload: Sign CSR", err.Error())
		return
	}

	maxSignRetries := 30
	signRetryInterval := 10 * time.Second
	var responseSignCSR string
	for attempt := 1; attempt <= maxSignRetries; attempt++ {
		responseSignCSR, err = r.client.PostDataV2(ctx, id, common.URL_SIGN_CERT, payloadSignCSRJSON)
		if err == nil {
			break
		}
		if strings.Contains(err.Error(), "consensus is down") && attempt < maxSignRetries {
			tflog.Debug(ctx, fmt.Sprintf("[resource_cm_cluster_node.go -> Create][%s] Consensus not ready, retrying sign CSR (attempt %d/%d)...", id, attempt, maxSignRetries))
			time.Sleep(signRetryInterval)
			continue
		}
		tflog.Debug(ctx, common.ERR_METHOD_END+err.Error()+" [resource_cm_cluster_node.go -> Create]["+id+"]")
		resp.Diagnostics.AddError("Error signing CSR on the existing cluster member: ", err.Error())
		return
	}
	if err != nil {
		resp.Diagnostics.AddError("Error signing CSR on the existing cluster member after retries: ", err.Error())
		return
	}

	// Step 3: Send the join request to the new node with the signed certificate and CA chain.
	// Use the explicit member_host if provided, otherwise fall back to the provider's address.
	memberHostInput := r.client.CipherTrustURL
	if !plan.MemberHost.IsNull() && !plan.MemberHost.IsUnknown() && plan.MemberHost.ValueString() != "" {
		memberHostInput = plan.MemberHost.ValueString()
	}
	memberHost, err := extractHost(memberHostInput)
	if err != nil {
		resp.Diagnostics.AddError("Invalid member_host for cluster member", err.Error())
		return
	}
	payloadJoinNode := JoinClusterJSON{
		CAChain:                gjson.Get(responseSignCSR, "cachain").String(),
		Cert:                   gjson.Get(responseSignCSR, "cert").String(),
		MKEKBlob:               gjson.Get(responseSignCSR, "mkek_blob").String(),
		LocalNodeHost:          joiningNodeHost,
		MemberNodeHost:         memberHost,
		MemberNodePort:         plan.MemberPort.ValueInt64(),
		LocalNodePort:          plan.Port.ValueInt64(),
		LocalNodePublicAddress: joiningNodePubAddress,
	}
	payloadJoinNodeJSON, err := json.Marshal(payloadJoinNode)
	if err != nil {
		resp.Diagnostics.AddError("Invalid payload: Join Node", err.Error())
		return
	}
	responseJoinNode, err := nodeClient.PostDataV2(ctx, id, common.URL_CLUSTER_JOIN, payloadJoinNodeJSON)
	if err != nil {
		tflog.Debug(ctx, common.ERR_METHOD_END+err.Error()+" [resource_cm_cluster_node.go -> Create]["+id+"]")
		resp.Diagnostics.AddError("Error joining cluster: ", err.Error())
		return
	}

	plan.ID = types.StringValue(gjson.Get(responseJoinNode, "nodeID").String())
	plan.NodeId = types.StringValue(gjson.Get(responseJoinNode, "nodeID").String())
	plan.NodeCount = types.Int64Value(gjson.Get(responseJoinNode, "nodeCount").Int())
	plan.StatusCode = types.StringValue(gjson.Get(responseJoinNode, "status.code").String())
	plan.StatusDescription = types.StringValue(gjson.Get(responseJoinNode, "status.description").String())

	tflog.Trace(ctx, common.MSG_METHOD_END+"[resource_cm_cluster_node.go -> Create]["+id+"]")
	diags = resp.State.Set(ctx, plan)
	resp.Diagnostics.Append(diags...)
}

// Read refreshes the Terraform state by calling /v1/cluster on the joining node.
// This keeps node_id and other computed fields in sync after each apply.
func (r *resourceCMClusterNode) Read(ctx context.Context, req resource.ReadRequest, resp *resource.ReadResponse) {
	var state CMAddClusterNodeTFSDK
	id := uuid.New().String()

	diags := req.State.Get(ctx, &state)
	resp.Diagnostics.Append(diags...)
	if resp.Diagnostics.HasError() {
		return
	}

	joiningNodeHost, err := extractHost(state.Host.ValueString())
	if err != nil {
		resp.Diagnostics.AddError("Invalid host for joining node", err.Error())
		return
	}
	nodeUsername := r.client.AuthData.Username
	nodePassword := r.client.AuthData.Password
	nodeDomain := r.client.AuthData.Domain
	nodeAuthDomain := r.client.AuthData.AuthDomain
	if state.Creds != nil {
		if !state.Creds.Username.IsNull() && !state.Creds.Username.IsUnknown() {
			nodeUsername = state.Creds.Username.ValueString()
		}
		if !state.Creds.Password.IsNull() && !state.Creds.Password.IsUnknown() {
			nodePassword = state.Creds.Password.ValueString()
		}
		if !state.Creds.Domain.IsNull() && !state.Creds.Domain.IsUnknown() {
			nodeDomain = state.Creds.Domain.ValueString()
		}
		if !state.Creds.AuthDomain.IsNull() && !state.Creds.AuthDomain.IsUnknown() {
			nodeAuthDomain = state.Creds.AuthDomain.ValueString()
		}
	}
	nodeURL := "https://" + joiningNodeHost
	nodeClient, err := common.NewClient(ctx, id, &nodeURL, &nodeAuthDomain, &nodeDomain, &nodeUsername, &nodePassword, true, 180)
	if err != nil {
		tflog.Debug(ctx, common.ERR_METHOD_END+err.Error()+" [resource_cm_cluster_node.go -> Read]["+id+"]")
		resp.Diagnostics.AddError("Unable to create HTTPS client for the joining node", err.Error())
		return
	}

	response, err := nodeClient.ReadDataByParam(ctx, id, "all", common.URL_CLUSTER_INFO)
	if err != nil {
		tflog.Debug(ctx, common.ERR_METHOD_END+err.Error()+" [resource_cm_cluster_node.go -> Read]["+id+"]")
		resp.Diagnostics.AddError("Error reading cluster info from joining node", err.Error())
		return
	}

	nodeID := gjson.Get(response, "nodeID").String()
	state.ID = types.StringValue(nodeID)
	state.NodeId = types.StringValue(nodeID)
	state.NodeCount = types.Int64Value(gjson.Get(response, "nodeCount").Int())
	state.StatusCode = types.StringValue(gjson.Get(response, "status.code").String())
	state.StatusDescription = types.StringValue(gjson.Get(response, "status.description").String())

	tflog.Trace(ctx, common.MSG_METHOD_END+"[resource_cm_cluster_node.go -> Read]["+id+"]")
	diags = resp.State.Set(ctx, &state)
	resp.Diagnostics.Append(diags...)
}

// Update is not implemented; node properties cannot be changed after joining.
func (r *resourceCMClusterNode) Update(ctx context.Context, req resource.UpdateRequest, resp *resource.UpdateResponse) {
}

// Delete removes the node from the cluster and clears the cluster config on the node itself.
func (r *resourceCMClusterNode) Delete(ctx context.Context, req resource.DeleteRequest, resp *resource.DeleteResponse) {
	id := uuid.New().String()
	var state CMAddClusterNodeTFSDK
	diags := req.State.Get(ctx, &state)
	resp.Diagnostics.Append(diags...)
	if resp.Diagnostics.HasError() {
		return
	}

	joiningNodeHost, err := extractHost(state.Host.ValueString())
	if err != nil {
		resp.Diagnostics.AddError("Invalid host for removed node", err.Error())
		return
	}
	nodeUsername := r.client.AuthData.Username
	nodePassword := r.client.AuthData.Password
	nodeDomain := r.client.AuthData.Domain
	nodeAuthDomain := r.client.AuthData.AuthDomain
	if state.Creds != nil {
		if !state.Creds.Username.IsNull() && !state.Creds.Username.IsUnknown() {
			nodeUsername = state.Creds.Username.ValueString()
		}
		if !state.Creds.Password.IsNull() && !state.Creds.Password.IsUnknown() {
			nodePassword = state.Creds.Password.ValueString()
		}
		if !state.Creds.Domain.IsNull() && !state.Creds.Domain.IsUnknown() {
			nodeDomain = state.Creds.Domain.ValueString()
		}
		if !state.Creds.AuthDomain.IsNull() && !state.Creds.AuthDomain.IsUnknown() {
			nodeAuthDomain = state.Creds.AuthDomain.ValueString()
		}
	}
	nodeURL := "https://" + joiningNodeHost
	nodeClient, err := common.NewClient(ctx, id, &nodeURL, &nodeAuthDomain, &nodeDomain, &nodeUsername, &nodePassword, true, 180)
	if err != nil {
		tflog.Debug(ctx, common.ERR_METHOD_END+err.Error()+" [resource_cm_cluster_node.go -> Delete]["+id+"]")
		resp.Diagnostics.AddError("Unable to create HTTPS client for the removed node", err.Error())
		return
	}

	// Recover node ID from the joining node if missing from state (e.g. after a failed apply).
	nodeID := state.NodeId.ValueString()
	if nodeID == "" {
		response, err := nodeClient.ReadDataByParam(ctx, id, "all", common.URL_CLUSTER_INFO)
		if err == nil {
			nodeID = gjson.Get(response, "nodeID").String()
		}
	}

	// Step 1: Remove the node from the cluster member list (called on the existing cluster member).
	// Skip if nodeID is still unknown — the node may never have fully joined.
	if nodeID != "" {
		endpoint := fmt.Sprintf("%s/%s", common.URL_NODES, nodeID)
		output, err := r.client.DeleteByURL(ctx, nodeID, endpoint)
		tflog.Trace(ctx, common.MSG_METHOD_END+"[resource_cm_cluster_node.go -> Delete]["+nodeID+"]["+output+"]")
		if err != nil {
			resp.Diagnostics.AddError(
				"Error removing node from cluster",
				"Could not remove node "+nodeID+" from cluster, unexpected error: "+err.Error(),
			)
			return
		}
	} else {
		tflog.Debug(ctx, "[resource_cm_cluster_node.go -> Delete]["+id+"] node ID unknown, skipping cluster member removal")
	}

	// Step 2: Delete the cluster configuration from the removed node itself.
	output, err := nodeClient.DeleteByURL(ctx, id, common.URL_CLUSTER_INFO)
	tflog.Trace(ctx, common.MSG_METHOD_END+"[resource_cm_cluster_node.go -> Delete]["+id+"]["+output+"]")
	if err != nil {
		tflog.Debug(ctx, common.ERR_METHOD_END+err.Error()+" [resource_cm_cluster_node.go -> Delete]["+id+"]")
		resp.Diagnostics.AddError(
			"Error deleting cluster config from removed node",
			"Node was removed from the cluster but its local cluster config could not be cleared: "+err.Error(),
		)
	}
}

func (r *resourceCMClusterNode) Configure(_ context.Context, req resource.ConfigureRequest, resp *resource.ConfigureResponse) {
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

	r.client = client
}
