{% if "postgres" in cookiecutter.db_resource %}
{% set pg_version = 15 %}
{% endif %}

param name string
param location string = resourceGroup().location
param tags object = {}
param prefix string
{# Define the dbserverUser. in cosmos-postgres it is 'citus' and in postgres aca add-on it is predefined #}
{% if cookiecutter.db_resource == "cosmos-postgres" %}
// value is read-only in cosmos
var dbserverUser = 'citus'
{% elif cookiecutter.db_resource == "postgres-flexible" %}
var dbserverUser = 'admin${uniqueString(resourceGroup().id)}'
{% endif %}
{# Create the dbserverPassword this is only required for postgres instances #}
{% if "postgres" in cookiecutter.db_resource %}
param dbserverPassword string
{% endif %}
{% if cookiecutter.db_resource != "postgres-addon" %}
param dbserverDatabaseName string
{% endif %}
param keyVaultName string

{# Postgres ACA Add-on #}
{% if cookiecutter.db_resource == "postgres-addon" %}
module dbserver 'core/database/postgresql/aca-service.bicep' = {
  name: name
  params: {
    name: '${take(prefix, 29)}-pg' // max 32 characters
    location: location
    tags: tags
    containerAppsEnvironmentId: containerApps.outputs.environmentId
  }
}
{% endif %}
{# Postgres Flexible Server #}
{% if cookiecutter.db_resource == "postgres-flexible" %}
module dbserver 'core/database/postgresql/flexibleserver.bicep' = {
  name: name
  scope: scope
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
{# Cosmos PostgreSQL#}
{% if cookiecutter.db_resource == "cosmos-postgres" %}
module dbserver 'core/database/cosmos/cosmos-pg-adapter.bicep' = {
  name: name
  scope: scope
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
{# Cosmos MongoDB#}
{% if cookiecutter.db_resource == "cosmos-mongodb" %}
module dbserver 'core/database/cosmos/mongo/cosmos-mongo-db.bicep' = {
  name: name
  params: {
    accountName: '${prefix}-mongodb'
    location: location
    databaseName: dbserverDatabaseName
    tags: tags
    keyVaultName: keyVaultName
  }
}
{% endif %}
