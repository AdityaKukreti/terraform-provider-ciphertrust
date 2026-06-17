package cm

import (
	"context"
	"fmt"

	"github.com/hashicorp/terraform-plugin-framework/resource/schema/planmodifier"
)

// NameImmutableModifier is a plan modifier that prevents the 'name' field from
// being changed after resource creation. It produces a clear, actionable error
// at plan time so the user is informed before any API call is made.
type NameImmutableModifier struct{}

func (m NameImmutableModifier) Description(_ context.Context) string {
	return "Name is immutable after creation."
}

func (m NameImmutableModifier) MarkdownDescription(_ context.Context) string {
	return "Name is immutable after creation."
}

func (m NameImmutableModifier) PlanModifyString(_ context.Context, req planmodifier.StringRequest, resp *planmodifier.StringResponse) {
	if req.StateValue.IsNull() || req.PlanValue.Equal(req.StateValue) {
		return
	}
	resp.Diagnostics.AddError(
		"Name cannot be changed",
		fmt.Sprintf(
			"The 'name' field is immutable after creation. "+
				"Current name on CipherTrust Manager: %q. "+
				"To use a different name, remove this resource from Terraform state "+
				"(terraform state rm) and import or recreate it with the desired name.",
			req.StateValue.ValueString(),
		),
	)
}
