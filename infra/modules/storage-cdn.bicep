param location string
param environment string
param projectPrefix string

var storageAccountName = '${projectPrefix}storage${environment}'
var containerName = 'images'
var cdnProfileName = '${projectPrefix}-cdn-${environment}'
var cdnEndpointName = '${projectPrefix}-images-${environment}'

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: storageAccountName
  location: location
  kind: 'StorageV2'
  sku: {
    name: 'Standard_LRS'
  }
  properties: {
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
    accessTier: 'Hot'
  }
}

resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2023-01-01' = {
  name: 'default'
  parent: storageAccount
  properties: {
    cors: {
      corsRules: [
        {
          allowedOrigins: ['*']
          allowedMethods: ['GET']
          allowedHeaders: ['*']
          exposedHeaders: ['*']
          maxAgeInSeconds: 3600
        }
      ]
    }
  }
}

resource container 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  name: containerName
  parent: blobService
  properties: {
    publicAccess: 'None'
  }
}

resource cdnProfile 'Microsoft.Cdn/profiles@2024-02-01' = {
  name: cdnProfileName
  location: location
  sku: {
    name: 'Standard_Microsoft'
  }
}

resource cdnEndpoint 'Microsoft.Cdn/profiles/endpoints@2024-02-01' = {
  name: cdnEndpointName
  parent: cdnProfile
  location: location
  properties: {
    origins: [
      {
        name: 'storageOrigin'
        properties: {
          hostName: storageAccount.properties.primaryEndpoints.blob
          httpPort: 80
          httpsPort: 443
        }
      }
    ]
    isHttpAllowed: false
    isHttpsAllowed: true
    queryStringCachingBehavior: 'BypassCaching'
  }
}

output accountName string = storageAccount.name
output accountKey string = storageAccount.listKeys().keys[0].value
output blobEndpoint string = storageAccount.properties.primaryEndpoints.blob
output cdnEndpoint string = 'https://${cdnEndpointName}.azureedge.net'
output containerName string = container.name
