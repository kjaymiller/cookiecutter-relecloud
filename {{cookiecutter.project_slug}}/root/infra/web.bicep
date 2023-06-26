param name string
param location string = resourceGroup().location
param tags object = {}

param applicationInsightsName string
param containerAppsEnvironmentName string
param containerRegistryName string
param exists bool
param identityName string
param keyVaultName string
param serviceName string = 'web'
param dbserverDomainName string
param dbserverDatabaseName string
param dbserverUser string
@secure()
param dbserverPassword string
{% if cookiecutter.project_backend in ("django", "flask") %}
@secure()
param secretKey string
{% endif %}

resource webIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: identityName
  location: location
}

module app 'core/host/container-app-upsert.bicep' = {
  name: '${serviceName}-container-app-module'
  params: {
    name: name
    location: location
    tags: union(tags, { 'azd-service-name': serviceName })
    identityName: webIdentity.name
    exists: exists
    containerAppsEnvironmentName: containerAppsEnvironmentName
    containerRegistryName: containerRegistryName
    env: [
      {
        name: 'DBSERVER_HOST'
        value: dbserverDomainName
      }
      {
        name: 'DBSERVER_USER'
        value: dbserverUser
      }
      {
        name: 'DBSERVER_DB'
        value: dbserverDatabaseName
      }
      {
        name: 'KEYVAULT'
        value: keyVault.name
      }
      {
        name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
        value: applicationInsights.properties.ConnectionString
      }
      {% if cookiecutter.project_backend in ("django", "flask") %}
      {
        name: 'SECRET_KEY'
        secretRef: 'secret-key'
      }
      {% endif %}
      {
        name: 'DBSERVER_PASSWORD'
        secretRef: 'dbserver-password'
      }
      ]
    secrets: [
        {
          name: 'dbserver-password'
          value: dbserverPassword
        }
        {% if cookiecutter.project_backend in ("django", "flask") %}
        {
          name: 'secret-key'
          value: secretKey
        }
        {% endif %}
      ]
    targetPort: {{cookiecutter.web_port}} 
  }
}

resource keyVault 'Microsoft.KeyVault/vaults@2022-07-01' existing = {
  name: keyVaultName
}

resource applicationInsights 'Microsoft.Insights/components@2020-02-02' existing = {
  name: applicationInsightsName
}

output SERVICE_WEB_IDENTITY_PRINCIPAL_ID string = webIdentity.properties.principalId
output SERVICE_WEB_NAME string = app.outputs.name
output SERVICE_WEB_URI string = app.outputs.uri
output SERVICE_WEB_IMAGE_NAME string = app.outputs.imageName
