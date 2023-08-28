targetScope = 'subscription'

@minLength(1)
@maxLength(64)
@description('Name which is used to generate a short unique hash for each resource')
param name string

@minLength(1)
@description('Primary location for all resources')
param location string

{% if cookiecutter.db_resource in ("postgres-flexible", "cosmos-postgres") %}
@secure()
@description('DBServer administrator password')
param dbserverPassword string
{% endif %}

{% if cookiecutter.project_backend in ("django", "flask") %}
@secure()
@description('Secret Key')
param secretKey string
{% endif %}
{% if cookiecutter.project_host == "aca" %}
param webAppExists bool = false
{% endif %}


@description('Id of the user or app to assign application roles')
param principalId string = ''

var resourceToken = toLower(uniqueString(subscription().id, name, location))
var tags = { 'azd-env-name': name }

resource resourceGroup 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: '${name}-rg'
  location: location
  tags: tags
}

var prefix = '${name}-${resourceToken}'
{% set pg_name = "dbserver" %}
{% set pg_version = 15 %}
{% if cookiecutter.db_resource == "cosmos-postgres" %}
// value is read-only in cosmos
var dbserverUser = 'citus'
{% elif cookiecutter.db_resource == "postgres-flexible" %}
var dbserverUser = 'admin${uniqueString(resourceGroup.id)}'
{% endif %}
{% if cookiecutter.db_resource in ("postgres-flexible", "cosmos-postgres") %}
var dbserverDatabaseName = 'relecloud'
{% endif %}

// Store secrets in a keyvault
module keyVault './core/security/keyvault.bicep' = {
  name: 'keyvault'
  scope: resourceGroup
  params: {
    name: '${take(replace(prefix, '-', ''), 17)}-vault'
    location: location
    tags: tags
    principalId: principalId
  }
}

{% if cookiecutter.db_resource == "cosmos-postgres" %}
module dbserver 'core/database/cosmos/cosmos-pg-adapter.bicep' = {
  name: '{{pg_name}}'
  scope: resourceGroup
  params: {
    name: '${prefix}-postgresql'
    location: location
    tags: tags
    postgresqlVersion: '{{pg_version}}'
    administratorLogin: dbserverUser
    administratorLoginPassword: dbserverPassword
    databaseName: dbserverDatabaseName
    allowAzureIPsFirewall: true
    coordinatorServerEdition: 'BurstableMemoryOptimized'
    coordinatorStorageQuotainMb: 131072
    coordinatorVCores: 1
    nodeCount: 0
    nodeVCores: 4
  }
}
{% endif %}

{% if cookiecutter.db_resource == "postgres-flexible" %}
module dbserver 'core/database/postgresql/flexibleserver.bicep' = {
  name: '{{pg_name}}'
  scope: resourceGroup
  params: {
    name: '${prefix}-postgresql'
    location: location
    tags: tags
    sku: {
      name: 'Standard_B1ms'
      tier: 'Burstable'
    }
    storage: {
      storageSizeGB: 32
    }
    version: '{{pg_version}}'
    administratorLogin: dbserverUser
    administratorLoginPassword: dbserverPassword
    databaseNames: [dbserverDatabaseName]
    allowAzureIPsFirewall: true
  }
}
{% endif %}

{% if cookiecutter.db_resource == "postgres-addon" %}
module dbserver 'core/database/postgresql/aca-service.bicep' = {
  name: '{{pg_name}}'
  scope: resourceGroup
  params: {
    name: '${take(prefix, 29)}-pg' // max 32 characters
    location: location
    tags: tags
    containerAppsEnvironmentId: containerApps.outputs.environmentId
  }
}
{% endif %}

// Monitor application with Azure Monitor
module monitoring 'core/monitor/monitoring.bicep' = {
  name: 'monitoring'
  scope: resourceGroup
  params: {
    location: location
    tags: tags
    applicationInsightsDashboardName: '${prefix}-appinsights-dashboard'
    applicationInsightsName: '${prefix}-appinsights'
    logAnalyticsName: '${prefix}-loganalytics'
  }
}

{% if cookiecutter.project_host == "appservice" %}

module web 'core/host/appservice.bicep' = {
  name: 'appservice'
  scope: resourceGroup
  params: {
    name: '${prefix}-web'
    location: location
    tags: union(tags, {'azd-service-name': 'web'})
    appServicePlanId: appServicePlan.outputs.id
    runtimeName: 'python'
    runtimeVersion: '3.11'
    scmDoBuildDuringDeployment: true
    ftpsState: 'Disabled'
    appCommandLine: 'entrypoint.sh'
    managedIdentity: true
    appSettings: {
      APPLICATIONINSIGHTS_CONNECTION_STRING: monitoring.outputs.applicationInsightsConnectionString
      RUNNING_IN_PRODUCTION: 'true'
      POSTGRES_HOST: dbserver.outputs.DOMAIN_NAME
      POSTGRES_USERNAME: dbserverUser
      POSTGRES_DATABASE: dbserverDatabaseName
      POSTGRES_PASSWORD: '@Microsoft.KeyVault(VaultName=${keyVault.outputs.name};SecretName=DBSERVERPASSWORD)'
      {% if cookiecutter.project_backend in ("django", "flask") %}
      SECRET_KEY: '@Microsoft.KeyVault(VaultName=${keyVault.outputs.name};SecretName=SECRETKEY)'
      {% endif %}
    }
  }
}

module appServicePlan 'core/host/appserviceplan.bicep' = {
  name: 'serviceplan'
  scope: resourceGroup
  params: {
    name: '${prefix}-serviceplan'
    location: location
    tags: tags
    sku: {
      name: 'B1'
    }
    reserved: true
  }
}
{% endif %}

{% if cookiecutter.project_host == "aca" %}
// Container apps host (including container registry)
module containerApps 'core/host/container-apps.bicep' = {
  name: 'container-apps'
  scope: resourceGroup
  params: {
    name: 'app'
    location: location
    containerAppsEnvironmentName: '${prefix}-containerapps-env'
    containerRegistryName: '${replace(prefix, '-', '')}registry'
    logAnalyticsWorkspaceName: monitoring.outputs.logAnalyticsWorkspaceName
  }
}

// Web frontend
module web 'web.bicep' = {
  name: 'web'
  scope: resourceGroup
  params: {
    name: replace('${take(prefix,19)}-ca', '--', '-')
    location: location
    tags: tags
    identityName: '${prefix}-id-web'
    applicationInsightsName: monitoring.outputs.applicationInsightsName
    containerAppsEnvironmentName: containerApps.outputs.environmentName
    containerRegistryName: containerApps.outputs.registryName
    {% if cookiecutter.db_resource in ("postgres-flexible", "cosmos-postgres") %}
    dbserverDomainName: dbserver.outputs.DOMAIN_NAME
    dbserverUser: dbserverUser
    dbserverDatabaseName: dbserverDatabaseName
    dbserverPassword: dbserverPassword
    {% endif %}
    {% if cookiecutter.db_resource == "postgres-addon" %}
    postgresServiceId: dbserver.outputs.id
    {% endif %}
    {% if cookiecutter.project_backend in ("django", "flask") %}
    secretKey: secretKey
    {% endif %}
    exists: webAppExists
  }
}
{% endif %}


// Give the app access to KeyVault
module webKeyVaultAccess './core/security/keyvault-access.bicep' = {
  name: 'web-keyvault-access'
  scope: resourceGroup
  params: {
    keyVaultName: keyVault.outputs.name
    {% if cookiecutter.project_host == "aca" %}
    principalId: web.outputs.SERVICE_WEB_IDENTITY_PRINCIPAL_ID
    {% endif %}
    {% if cookiecutter.project_host == "appservice" %}
    principalId: web.outputs.identityPrincipalId
    {% endif %}
  }
}


var secrets = [
  {% if cookiecutter.db_resource in ("postgres-flexible", "cosmos-postgres") %}
  {
    name: 'DBSERVERPASSWORD'
    value: dbserverPassword
  }
  {% endif %}
  {% if cookiecutter.project_backend in ("django", "flask") %}
  {
    name: 'SECRETKEY'
    value: secretKey
  }
  {% endif %}
]

@batchSize(1)
module keyVaultSecrets './core/security/keyvault-secret.bicep' = [for secret in secrets: {
  name: 'keyvault-secret-${secret.name}'
  scope: resourceGroup
  params: {
    keyVaultName: keyVault.outputs.name
    name: secret.name
    secretValue: secret.value
  }
}]

output AZURE_LOCATION string = location
{% if cookiecutter.project_host == "aca" %}
output AZURE_CONTAINER_ENVIRONMENT_NAME string = containerApps.outputs.environmentName
output AZURE_CONTAINER_REGISTRY_ENDPOINT string = containerApps.outputs.registryLoginServer
output AZURE_CONTAINER_REGISTRY_NAME string = containerApps.outputs.registryName
output SERVICE_WEB_IDENTITY_PRINCIPAL_ID string = web.outputs.SERVICE_WEB_IDENTITY_PRINCIPAL_ID
output SERVICE_WEB_NAME string = web.outputs.SERVICE_WEB_NAME
output SERVICE_WEB_URI string = web.outputs.SERVICE_WEB_URI
output SERVICE_WEB_IMAGE_NAME string = web.outputs.SERVICE_WEB_IMAGE_NAME
{% endif %}
output AZURE_KEY_VAULT_ENDPOINT string = keyVault.outputs.endpoint
output AZURE_KEY_VAULT_NAME string = keyVault.outputs.name
output APPLICATIONINSIGHTS_NAME string = monitoring.outputs.applicationInsightsName
