param location string
param environment string
param projectPrefix string

var serverName = '${projectPrefix}-db-${environment}'
var dbName = '${projectPrefix}_${environment}'

resource postgresServer 'Microsoft.DBforPostgreSQL/flexibleServers@2023-12-01' = {
  name: serverName
  location: location
  properties: {
    version: '16'
    administratorLogin: 'adminuser'
    administratorLoginPassword: 'ChangeMe123!' // Will be rotated to Key Vault
    storage: {
      storageSizeGB: 32
    }
    sku: {
      name: 'Standard_D2ds_v5'
      tier: 'GeneralPurpose'
    }
    backup: {
      backupRetentionDays: 7
      geoRedundantBackup: 'Enabled'
    }
    highAvailability: {
      mode: 'ZoneRedundant'
    }
  }
}

resource postgresDatabase 'Microsoft.DBforPostgreSQL/flexibleServers/databases@2023-12-01' = {
  name: dbName
  parent: postgresServer
  properties: {}
}

resource postgresFirewall 'Microsoft.DBforPostgreSQL/flexibleServers/firewallRules@2023-12-01' = {
  name: 'allow-azure-services'
  parent: postgresServer
  properties: {
    startIpAddress: '0.0.0.0'
    endIpAddress: '0.0.0.0'
  }
}

output connectionString string = 'postgresql://${postgresServer.properties.administratorLogin}:${postgresServer.properties.administratorLoginPassword}@${postgresServer.properties.fullyQualifiedDomainName}:5432/${dbName}?sslmode=require'
output serverFqdn string = postgresServer.properties.fullyQualifiedDomainName
