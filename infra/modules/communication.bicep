param location string
param environment string
param projectPrefix string

var acsName = '${projectPrefix}-acs-${environment}'

resource communicationService 'Microsoft.Communication/communicationServices@2023-10-01' = {
  name: acsName
  location: 'global'
  properties: {
    dataLocation: 'United States'
  }
}

output name string = communicationService.name
output connectionString string = communicationService.listKeys().primaryConnectionString
output emailDomain string = 'noreply@${communicationService.name}.com'
