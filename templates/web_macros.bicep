{% macro env_db_resources %}
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
{
  name: 'POSTGRES_SSL'
  value: 'require'
}
{% endif %}
{% endmacro %}


{% if cookiecutter.db_resource == "cosmos-mongodb" %}
module dbserver 'core/database/cosmos/mongo/cosmos-mongo-db.bicep' = {
  name: 'dbserver'
  scope: resourceGroup
  params: {
    accountName: 'mongodb'
    location: location
    databaseName: 'db'
    tags: tags
    keyVaultName: keyVault.name
  }
}
{% endif %}
