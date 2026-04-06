package provider

import (
	"context"
	"fmt"
	"github.com/ThalesGroup/terraform-provider-ciphertrust/internal/provider/common"
	"github.com/google/uuid"
	"github.com/hashicorp/terraform-plugin-framework/providerserver"
	"github.com/hashicorp/terraform-plugin-go/tfprotov6"
	"github.com/tidwall/gjson"
	"os"
	"strconv"
	"strings"
)

const (
	providerConfig = `
provider "ciphertrust" {
	address = "https://192.168.2.135"
	username = "admin"
	password = "ChangeIt01!"
	bootstrap = "no"
}
`
)

var (
	testAccProtoV6ProviderFactories = map[string]func() (tfprotov6.ProviderServer, error){
		"ciphertrust": providerserver.NewProtocol6WithError(New("ciphertrust")()),
	}
)

var cipherTrustVersion int

const devCMVersionValue = 9999

// getCipherTrustVersion will return the major and minor versions converted to an int
// For example 2.24.0-beta7+51895 returns 224. 2.21.2 returns 221.
// Development builds will return 9999 as we don't know.
func getCipherTrustVersion() int {
	if cipherTrustVersion != 0 {
		fmt.Printf("Test System Version: %d\n", cipherTrustVersion)
		return cipherTrustVersion
	}
	var (
		err      error
		client   *common.Client
		response string
	)
	address := os.Getenv("CIPHERTRUST_ADDRESS")
	username := os.Getenv("CIPHERTRUST_USERNAME")
	password := os.Getenv("CIPHERTRUST_PASSWORD")
	domain := "root"
	if address == "" || username == "" || password == "" {
		fmt.Printf("CIPHERTRUST_ADDRESS, CIPHERTRUST_USERNAME and CIPHERTRUST_PASSWORD enviornment variables must be set to get the system version, returning %d\n", devCMVersionValue)
		return devCMVersionValue
	}
	client, err = common.NewClient(context.Background(), uuid.NewString(), &address, &domain, &domain, &username, &password, true, 180)
	if err != nil {
		fmt.Printf("** Failed to create client, returning 0. err: %s\n", err.Error())
		return 0
	}
	response, err = client.GetById(context.Background(), "", "", common.URL_SYSTEMINFO)
	if err != nil {
		fmt.Printf("** Failed get system info, returning 0.  err: %s\n", err.Error())
		return 0
	}

	version := gjson.Get(response, "version").String()
	fmt.Printf("SysInfo Version: %v\n", version)
	if version == "" {
		fmt.Println("** System version is empty, returning 0")
		return 0
	}
	if version == "Development" {
		fmt.Printf("** System version is Development, returning %d\n", devCMVersionValue)
		return devCMVersionValue
	}
	versions := strings.Split(version, ".")
	if len(versions) < 2 {
		fmt.Printf("** Unable to determine system version from '%s', returning 0\n", version)
		return 0
	}
	cipherTrustVersion, err = strconv.Atoi(versions[0] + versions[1])
	if err != nil {
		fmt.Printf("** Failed to convert %s to int, returning 0. Error: %s\n", versions[0]+versions[1], err.Error())
		return 0
	}
	fmt.Printf("Test System Version: %d\n", cipherTrustVersion)
	return cipherTrustVersion
}
