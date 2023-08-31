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
{% endif %}
{% endmacro %}