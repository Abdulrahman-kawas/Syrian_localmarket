param location string
param environment string
param projectPrefix string

var signalRName = '${projectPrefix}-signalr-${environment}'

resource signalR 'Microsoft.SignalRService/signalR@2024-03-01' = {
  name: signalRName
  location: location
  sku: {
    name: 'Free_F1'
    tier: 'Free'
  }
  properties: {
    features: [
      {
        flag: 'ServiceMode'
        value: 'Serverless'
      }
    ]
    cors: {
      allowedOrigins: ['*']
    }
  }
}

output name string = signalR.name
output primaryConnectionString string = 'Endpoint=https://${signalR.properties.hostName};AccessKey=${signalR.listKeys().primaryKey};Version=1.0'
output hubName string = 'localmarket'
