
default: fmt  install


build:
	go build -v ./...

install: build
	go install -v ./...

lint:
	golangci-lint run

generate:
	cd tools; go generate ./...

fmt:
	gofmt -s -w -e .

test:
	go test -v -cover -timeout=120s -parallel=10 ./...

testacc:
	rm -rf /work/ctp.log
	rm -rf /work/terraform-provider-ciphertrust-v1/*.log
	rm -rf /work/terraform-provider-ciphertrust-v1-101/*.log
#TF_ACC=1 go test -v -timeout 120m ./...
#TF_ACC=1 go test -v -timeout 120m ./internal/provider/ -run TestCckmOCI
#	TF_ACC=1 go test -v -timeout 120m ./internal/provider/ -run TestOciConnection
#	TF_ACC=1 go test -v -timeout 120m ./internal/provider/ -run TestResourceGCPConnection
	TF_ACC=1 go test -v -timeout 120m ./internal/provider/ -run TestCckmSchedulersRotationDataSource
	TF_ACC=1 go test -v -timeout 120m ./internal/provider/ -run TestCckmSchedulersRotationResource
	TF_ACC=1 go test -v -timeout 120m ./internal/provider/ -run TestCckmAWS
#	TF_ACC=1 go test -v -timeout 120m ./internal/provider/ -run TestCckmAWSKey
#	TF_ACC=1 go test -v -timeout 120m ./internal/provider/ -run TestCckmAWSKeyNative
#	TF_ACC=1 go test -v -timeout 120m ./internal/provider/ -run TestCckmAWSKeyNativeImport
#	TF_ACC=1 go test -v -timeout 120m ./internal/provider/ -run TestCckmAWSKeyRotation
#	TF_ACC=1 go test -v -timeout 120m ./internal/provider/ -run TestCckmSchedulersRotationDataSource
#	TF_ACC=1 go test -v -timeout 120m ./internal/provider/ -run TestCckmAWSDataSourceKey
#	TF_ACC=1 go test -v -timeout 120m ./internal/provider/ -run TestCckmAWSKeyImportKeyMaterial
#	TF_ACC=1 go test -v -timeout 120m ./internal/provider/ -run TestCckmAWSXKSUnlinkedKey
#	TF_ACC=1 go test -v -timeout 120m ./internal/provider/ -run TestCckmAWSDataSourceKey
#	TF_ACC=1 go test -v -timeout 120m ./internal/provider/ -run TestCckmAWSDataSourceXksKey
#	TF_ACC=1 go test -v -timeout 120m ./internal/provider/ -run TestCckmAWSXKSUnlinkedKey
#	TF_ACC=1 go test -v -timeout 120m ./internal/provider/ -run TestCckmSchedulersRotationDataSource
#	TF_ACC=1 go test -v -timeout 120m ./internal/provider/ -run TestCckmAWSDataSourceCustomKeyStore

me:
	rm -rf /work/ctf.log
	rm -rf /work/terraform-provider-ciphertrust-v1/*.log
	rm -rf /work/terraform-provider-ciphertrust-v1-101/*.log
	go build -o ./terraform-provider-ciphertrust
	cp terraform-provider-ciphertrust ~/.terraform.d/plugins/thales.com/terraform/ciphertrust/1.0.1/linux_amd64/


.PHONY: fmt lint test testacc build install generate


