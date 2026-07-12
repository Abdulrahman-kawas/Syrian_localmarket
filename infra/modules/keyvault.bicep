param location string
param environment string
param projectPrefix string
param managedIdentityPrincipalId string

var keyVaultName = '${projectPrefix}-kv-${environment}'

resource keyVault 'Microsoft.KeyVault/vaults@2023-07.0' = {
  name: keyVaultName
  location: location
  properties: {
    tenantId: subscription().tenantId
    sku: {
      family: 'A'
      name: 'standard'
    }
    enableSoftDelete: true
    softDeleteRetentionInDays: 90
    enableRbacAuthorization: true
    networkAcls: {
      defaultAction: 'Deny'
      bypass: 'AzureServices'
    }
  }
}

resource accessPolicy 'Microsoft.KeyVault/vaults/accessPolicies@2023-07.0' = {
  name: 'add'
  parent: keyVault
  properties: {
    accessPolicies: [
      {
        tenantId: subscription().tenantId
        objectId: managedIdentityPrincipalId
        permissions: {
          secrets: ['get', 'list']
          keys: ['get', 'list']
        }
      }
    ]
  }
}

output vaultUri string = keyVault.properties.vaultUri
output vaultName string = keyVault.name
