{# This is the appservice version of `web.bicep` selected by post_gen_project.py #}
param name string
param location string = resourceGroup().location
param tags object = {}
param identityName string
param pythonVersion string
param appCommandLine string
param keyVaultName string

resource applicationInsights 'Microsoft.Insights/components@2020-02-02' existing = {
  name: applicationInsightsName
}

module appServicePlan 'core/host/appserviceplan.bicep' = {
  name: 'serviceplan'
  params: {
    name: '${name}-serviceplan'
    location: location
    tags: tags
    sku: {
      name: 'B1'
    }
    reserved: true
  }
}

resource webIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: identityName
  location: location
}
// Give the app access to KeyVault
module webKeyVaultAccess './core/security/keyvault-access.bicep' = {
  name: 'web-keyvault-access'
  scope: resourceGroup
  params: {
    keyVaultName: keyVaultName
    principalId: web.outputs.identityPrincipalId
  }
}

module web 'core/host/appservice.bicep' = {
    name: 'appservice'
    params: {
      name: '${name}-web'
      location: location
      tags: union(tags, {'azd-service-name': 'web'})
      appCommandLine: appCommandLine
      appServicePlanId: appServicePlan.outputs.id
      keyVaultName: keyVaultName
      runtimeName: 'python'
      runtimeVersion: pythonVersion
      scmDoBuildDuringDeployment: true
      ftpsState: 'Disabled'
      managedIdentity: true
      appSettings: {
        APPLICATIONINSIGHTS_CONNECTION_STRING: applicationInsights.properties.ConnectionString
        RUNNING_IN_PRODUCTION: 'true'
        {% if "postgres" in cookiecutter.db_resource %}
        POSTGRES_HOST: dbserver.outputs.DOMAIN_NAME
        POSTGRES_USERNAME: dbserverUser
        POSTGRES_DATABASE: dbserverDatabaseName
        POSTGRES_PASSWORD: '@Microsoft.KeyVault(VaultName=${keyVault.outputs.name};SecretName=DBSERVERPASSWORD)'
        {% endif %}
        {% if cookiecutter.project_backend in ("django", "flask") %}
        SECRET_KEY: '@Microsoft.KeyVault(VaultName=${keyVaultName};SecretName=SECRETKEY)'
        {% endif %}
        {% if 'mongodb' in cookiecutter.db_resource %}
        AZURE_COSMOS_CONNECTION_STRING: '@Microsoft.KeyVault(VaultName=${keyVaultName};SecretName=AZURE-COSMOS-CONNECTION-STRING)'
        {% endif %}
      }
    }
    dependsOn: [
      webKeyVaultAccess
    ]
  }


  output SERVICE_WEB_IDENTITY_PRINCIPAL_ID string = web.outputs.identityPrincipalId
