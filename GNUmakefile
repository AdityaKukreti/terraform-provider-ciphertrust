
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
#TF_ACC=1 go test -v -timeout 120m ./...
#TF_ACC=1 go test -v -timeout 120m ./internal/provider/ -run TestCckmOCI
	TF_ACC=1 go test -v -timeout 120m ./internal/provider/ -run TestOciConnection


me:
	rm -rf /work/ctf.log
	rm -rf /work/terraform-provider-ciphertrust-v1/*.log
	rm -rf /work/terraform-provider-ciphertrust-v1-101/*.log
	go build -o ./terraform-provider-ciphertrust
	cp terraform-provider-ciphertrust ~/.terraform.d/plugins/thales.com/terraform/ciphertrust/1.0.1/linux_amd64/


.PHONY: fmt lint test testacc build install generate


