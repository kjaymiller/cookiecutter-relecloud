{# This is the appservice version of `web.bicep` selected by post_gen_project.py #}
param scope object
param prefix string
param location string = resourceGroup().location
param tags object = {}
param applicationInsightsConnectionString
param pythonVersion string 
param appCommandLine string

{% if cookiecutter.project_host == "appservice" %}
module appServicePlan 'core/host/appserviceplan.bicep' = {
  name: 'serviceplan'
  scope: scope
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


module web 'core/host/appservice.bicep' = {
    name: 'appservice'
    scope: resourceGroup
    params: {
      name: '${prefix}-web'
      location: location
      tags: union(tags, {'azd-service-name': 'web'})
      appServicePlanId: appServicePlan.outputs.id
      runtimeName: 'python'
      runtimeVersion: pythonVersion
      scmDoBuildDuringDeployment: true
      ftpsState: 'Disabled'
      appCommandLine: appCommandLine
      managedIdentity: true
      appSettings: {
        APPLICATIONINSIGHTS_CONNECTION_STRING: applicationInsightsConnectionString
        RUNNING_IN_PRODUCTION: 'true'
        {% if "postgres" in cookiecutter.db_resource %}
        POSTGRES_HOST: dbserver.outputs.DOMAIN_NAME
        POSTGRES_USERNAME: dbserverUser
        POSTGRES_DATABASE: dbserverDatabaseName
        POSTGRES_PASSWORD: '@Microsoft.KeyVault(VaultName=${keyVault.outputs.name};SecretName=DBSERVERPASSWORD)'
        {% endif %}
        {% if cookiecutter.project_backend in ("django", "flask") %}
        SECRET_KEY: '@Microsoft.KeyVault(VaultName=${keyVault.outputs.name};SecretName=SECRETKEY)'
        {% endif %}
        {% if 'mongodb' in cookiecutter.db_resource %}
        AZURE_COSMOS_CONNECTION_STRING: '@Micrsoft.KeyVault(VaultName=${keyVault.outputs.name};SecretName=AZURE-COSMOS-CONNECTION-STRING)'
        {% endif %}
      }
    }
  }
