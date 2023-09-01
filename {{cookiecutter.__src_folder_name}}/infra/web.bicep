param name string
param location string = resourceGroup().location
param tags object = {}

param applicationInsightsName string
param containerAppsEnvironmentName string
param containerRegistryName string
param exists bool
param identityName string
param serviceName string = 'web'
param keyVaultUrl string
{# The dbserver values do not exist in the postgres aca add-on #}
{% if cookiecutter.db_resource in ("postgres-flexible", "cosmos-postgres") %}
param dbserverDomainName string
param dbserverDatabaseName string
param dbserverUser string

@secure()
param dbserverPassword string
{% endif %}
{% if cookiecutter.project_backend in ("django", "flask") %}
@secure()
param secretKey string
{% endif %}
{% if cookiecutter.db_resource == "postgres-addon" %}
param postgresServiceId string
{% endif %}

resource webIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: identityName
  location: location
}

{% if cookiecutter.project_host == "aca" %}
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
      {% if 'postgres' in cookiecutter.db_resource %}
      {% if cookiecutter.db_resource in ("postgres-flexible", "cosmos-postgres") %}
      {
        name: 'POSTGRES_HOST'
        value: dbserverDomainName
      }
      {
        name: 'POSTGRES_USERNAME'
        value: dbserverUser
      }
      {
        name: 'POSTGRES_DATABASE'
        value: dbserverDatabaseName
      }
      {
        name: 'POSTGRES_PASSWORD'
        secretRef: 'dbserver-password'
      }
      {% endif %}
      {% endif %}
      {
        name: 'RUNNING_IN_PRODUCTION'
        value: 'true'
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
      ]
    secrets: [
        {% if cookiecutter.db_resource in ("postgres-flexible", "cosmos-postgres") %}
        {
          name: 'dbserver-password'
          value: dbserverPassword
        }
        {% endif %}
        {% if cookiecutter.project_backend in ("django", "flask") %}
        {
          name: 'secret-key'
          value: secretKey
        }
        {% endif %}
        {% if "mongodb" in cookiecutter.project_backend%}
        {
          name: 'azure-cosmos-connection-string'
          keyVaultUrl: '${keyVaultURI}/secrets/azure-cosmos-connection-string'
          identity: 
        }
        {% endif %}
      ]
    {% if cookiecutter.db_resource == "postgres-addon" %}
    postgresServiceId: postgresServiceId
    {% endif %}
    targetPort: {{cookiecutter.web_port}} 
  }
}
{% endif %}

resource applicationInsights 'Microsoft.Insights/components@2020-02-02' existing = {
  name: applicationInsightsName

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
  output SERVICE_WEB_IDENTITY_PRINCIPAL_ID string = webIdentity.properties.principalId
output SERVICE_WEB_NAME string = app.outputs.name
output SERVICE_WEB_URI string = app.outputs.uri
output SERVICE_WEB_IMAGE_NAME string = app.outputs.imageName
