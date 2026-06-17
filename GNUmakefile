
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
	go test -v -count=1 -cover -timeout=120s -parallel=10 ./...

testacc:
	rm -rf /work/ctp.log
	rm -rf /work/terraform-provider-ciphertrust-v1/*.log
	rm -rf /work/terraform-provider-ciphertrust-v1-101/*.log

#	TF_ACC=1 go test -v -count=1 -timeout 120m ./...


# START OF SMOKE
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmOCIKeyVaultDeletedOOB

#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSXksUnlinkedKey
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSDataSourceXksKey

##	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSKms
##	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSPolicyTemplate
##	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSAcl
##	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSKeyNative$
##	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSKeyNativeImport
##	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSKeyKmsDeleteRecovery
##	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSKeyMultiRegionNativeAndMakePrimary
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSKeyRotationNative
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSByokKeyAESCreateWithSourceKey
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSByokKeyUpdates
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSByokKeyKmsDeleteRecovery
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSByokKeyMultiRegionAndMakePrimary
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSKeyMaterialCreateAndUpdate
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSKeyMaterialRepairPendingImport
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSKeyMaterialMultiRegionOOBDeleteMaterial
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSCustomKeyStoreUnlinked
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSCloudHSMUnlinkedKey
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSXksUnlinkedKey
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSDataSourceKms
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSDataSourceKey
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSDataSourceCustomKeyStore
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSDataSourceXksKey
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSDataSourceAccountDetails


# END OF SMOKE

#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWS

#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSKeyRotationNative
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWS
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSXks
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSNativeKeyMinimalConfig

#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSByokKeyMultiRegionAndPrimaryRegion
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSByokKeyMultiRegionAndMakePrimary
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSKeyMultiRegionNativeAndPrimaryRegion
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSKeyMultiRegionNativeAndMakePrimary


#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSDataSourceXksKey
#TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSByokKeyRSACreateWithSourceKey
#TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSKeyRotationNative
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSKeyNative
#TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSKeyMultiRegionNative
#TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSKeyNativeImport
#TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSKeyKmsDeleteRecovery
#TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSKeyMinimalConfig
#TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSXKSUnlinkedKey

#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSKeyMaterial
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSKeyMaterialCreate
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSKeyMaterialRepairPendingImport
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSKeyMaterialRepairPendingRotation
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSKeyMaterialRepairCombined
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSKeyMaterialCreateAndUpdate
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSKeyMaterialMultiRegionOOBDeleteMaterial
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSKeyMaterialRepairMultiRegionPendingImportAndRotation
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSKeyMaterialAdoptPendingRotation
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSKeyMaterialAdoptPendingMRRotation
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSKeyMaterialMRPendingImportFirstMaterial
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSKeyMaterialPlanValidation
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWSKeyMaterialCombinedUpdates

#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmAWS
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run  TestCckmAWSAcl
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run  TestCckmAWSByokKeyUpdates
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run  TestCckmAWSByokKeyPolicyUpdates
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run  TestCckmAWSByokKeyRepairMaterial
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run  TestCckmAWSByokKeyRepairMultiRegionPendingImportAndRotation
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run  TestCckmAWSByokKeyKmsDeleteRecovery
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run  TestCckmAWSByokKeyMultiRegion
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run  TestCckmAWSByokKeyCreatePendingImport
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run  TestCckmAWSByokKeyUploadOnCreate
##	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run  TestCckmAWSCloudHSMUnlinkedKey
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run  TestCckmAWSCustomKeyStoreEmptyAwsParams
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run  TestCckmAWSCustomKeyStoreEmptyLocalHostedParams
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run  TestCckmAWSCustomKeyStoreUnlinked
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run  TestCckmAwsImportMaterial$
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run  TestCckmAwsImportMaterialMultiRegion
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run  TestCckmAWSKeyRotationNative
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run  TestCckmAWSKeyRotationByokKey

# WE ARE UP TO HERE ON INDIVIDUAL TESTS - PRE
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run  TestCckmAWSKeyKmsDeleteRecovery
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run  TestCckmAWSKeyMinimalConfig
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run  TestCckmAWSKeyMultiRegionNative
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run  TestCckmAWSKeyNative$
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run  TestCckmAWSKeyNativeImport
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run  TestCckmAWSKeyRotationNative
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run  TestCckmAWSKms
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run  TestCckmAWSPolicyTemplate
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run  TestCckmAWSXKSUnlinkedKey

#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run  TestCckmAWSDataSourceAccountDetails
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run  TestCckmAWSDataSourceCustomKeyStore
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run  TestCckmAWSDataSourceKey
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run  TestCckmAWSDataSourceKms
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run  TestCckmAWSDataSourceXksKey

#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmOCI
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmOCIAcl
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmOCIDataSourceConnection
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmOCIDatasourceVault
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmOCIKeysAndVersionsBYOK
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmOCIKeysAndVersionsNative
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmOCIMinimalConfig
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmOCIVault
#	TF_ACC=1 go test -v -count=1 -timeout 120m ./internal/provider/ -run TestCckmOCIVault

me:
	rm -rf /work/ctf.log
	rm -rf /work/terraform-provider-ciphertrust-v1/*.log
	rm -rf /work/terraform-provider-ciphertrust-v1-101/*.log
	go build -o ./terraform-provider-ciphertrust
	cp terraform-provider-ciphertrust ~/.terraform.d/plugins/thales.com/terraform/ciphertrust/1.0.1/linux_amd64/


.PHONY: fmt lint test testacc build install generate


