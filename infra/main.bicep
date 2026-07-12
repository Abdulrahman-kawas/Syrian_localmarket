param location string = resourceGroup().location
param environment string = 'dev'
param projectPrefix string = 'lm'

// Module references
module containerApp './modules/container-app.bicep' = {
  name: 'containerApp'
  params: {
    location: location
    environment: environment
    projectPrefix: projectPrefix
  }
}

module postgres './modules/postgres.bicep' = {
  name: 'postgres'
  params: {
    location: location
    environment: environment
    projectPrefix: projectPrefix
  }
}

module storageCdn './modules/storage-cdn.bicep' = {
  name: 'storageCdn'
  params: {
    location: location
    environment: environment
    projectPrefix: projectPrefix
  }
}

module keyvault './modules/keyvault.bicep' = {
  name: 'keyvault'
  params: {
    location: location
    environment: environment
    projectPrefix: projectPrefix
    managedIdentityPrincipalId: containerApp.outputs.managedIdentityPrincipalId
  }
}

module notificationHubs './modules/notification-hubs.bicep' = {
  name: 'notificationHubs'
  params: {
    location: location
    environment: environment
    projectPrefix: projectPrefix
  }
}

module signalr './modules/signalr.bicep' = {
  name: 'signalr'
  params: {
    location: location
    environment: environment
    projectPrefix: projectPrefix
  }
}

module communication './modules/communication.bicep' = {
  name: 'communication'
  params: {
    location: location
    environment: environment
    projectPrefix: projectPrefix
  }
}

module monitoring './modules/monitoring.bicep' = {
  name: 'monitoring'
  params: {
    location: location
    environment: environment
    projectPrefix: projectPrefix
  }
}

output containerAppFqdn string = containerApp.outputs.fqdn
output postgresConnectionString string = postgres.outputs.connectionString
output storageAccountName string = storageCdn.outputs.accountName
output keyvaultUrl string = keyvault.outputs.vaultUri
output signalrConnectionString string = signalr.outputs.primaryConnectionString
output notificationHubsConnectionString string = notificationHubs.outputs.connectionString
output appInsightsConnectionString string = monitoring.outputs.connectionString
