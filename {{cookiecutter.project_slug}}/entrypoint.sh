#!/bin/bash

set -e

{% if cookiecutter.project_backend in ("fastapi", "flask") %}
gunicorn app:app
{% endif %}
{% if cookiecutter.project_backend == "django" %}
echo "${0}: running migrations."
python manage.py migrate
python manage.py loaddata seed_data.json
python manage.py collectstatic
gunicorn project.wsgi:application \
    --name relecloud \
    --bind 0.0.0.0:8000 \
    --timeout 600 \
    --workers 4 \
    --log-level=info
{% endif %}