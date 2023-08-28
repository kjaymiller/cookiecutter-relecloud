{% macro install_flask_deps() %}
{# Check for Databases #}
{% if cookiecutter.opencensus %}
python3 -m pip install -e .[opencensus]
{% endif %}
{% if 'postgres' in cookiecutter.db_resource %}
python3 -m pip install -e .[postgres]
{# postgres migrations need to happen #}
python3 -m flask --app flaskapp db upgrade --directory flaskapp/migrations
python3 -m flask --app flaskapp seed --filename seed_data.json
python3 -m gunicorn 'flaskapp:create_app()'
{% endif %}
{% if 'mongodb' in cookiecutter.db_resource %}
python3 -m pip install -e .[mongodb]
{% endif %}
{% endmacro %}