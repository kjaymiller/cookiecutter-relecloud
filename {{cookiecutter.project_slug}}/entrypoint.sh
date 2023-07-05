#!/bin/bash

set -e

{% if cookiecutter.project_backend == "flask" %}
python3 -m flask --app flaskapp db upgrade --directory flaskapp/migrations
python3 -m flask --app flaskapp seed --filename seed_data.json
python3 -m gunicorn 'flaskapp:create_app()'
{% endif %}
{% if cookiecutter.project_backend in ("fastapi", "flask") %}
python3 -m gunicorn app:app
{% endif %}
{% if cookiecutter.project_backend == "django" %}
echo "${0}: running migrations."
python manage.py migrate
python manage.py loaddata seed_data.json
python manage.py collectstatic
python3 -m gunicorn project.wsgi:application \
    --name relecloud
{% endif %}