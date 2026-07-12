param location string
param environment string
param projectPrefix string

var namespaceName = '${projectPrefix}-nh-${environment}'
var hubName = '${projectPrefix}-hub-${environment}'

resource namespace 'Microsoft.NotificationHubs/namespaces@2023-09-01' = {
  name: namespaceName
  location: location
  sku: {
    name: 'Free'
    tier: 'Free'
  }
  properties: {
    enabled: true
  }
}

resource hub 'Microsoft.NotificationHubs/namespaces/notificationHubs@2023-09-01' = {
  name: hubName
  parent: namespace
  properties: {}
}

output namespaceName string = namespace.name
output hubName string = hub.name
output connectionString string = 'Endpoint=sb://${namespace.name}.servicebus.windows.net/;SharedAccessKeyName=DefaultListenSharedAccessSignature;SharedAccessKey=${namespace.listKeys().primaryConnectionString}'
