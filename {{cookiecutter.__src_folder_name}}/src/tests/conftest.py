{# standard library imports #}
{% if cookiecutter.project_backend == "fastapi" %}
from multiprocessing import Process
import socket
import time
{% endif %}
{% if cookiecutter.project_backend == "flask" %}
import os
import pathlib
{% endif %}
{% if cookiecutter.project_backend == "django" %}
import os
{% endif %}

{# third-party library imports #}
import pytest
{% if cookiecutter.project_backend == "flask" %}
from flask import url_for
{% endif %}
{% if 'mongodb' in cookiecutter.db_resource %}
import mongoengine as engine
{% endif %}
{% if cookiecutter.project_backend == "fastapi" %}
import requests
import uvicorn
{% endif %}
{% if cookiecutter.project_backend == "django" %}
from django.core.management import call_command
{% endif %}

{# Local imports #}
{% if cookiecutter.project_backend == "fastapi" %}
from fastapi_app import seed_data
from fastapi_app.app import app

{% endif %}
{% if cookiecutter.project_backend == "flask" %}
from flaskapp import create_app, seeder
{% if 'postgres' in cookiecutter.db_resource %}
from flaskapp import db
{% endif %}
{% endif %}

{% if cookiecutter.project_backend == "fastapi" %}
def wait_for_server_ready(
    url: str, timeout: float = 10.0, check_interval: float = 0.5
) -> bool:
    """Make requests to provided url until it responds without error."""
    conn_error = None
    for _ in range(int(timeout / check_interval)):
        try:
            requests.get(url)
        except requests.ConnectionError as exc:
            time.sleep(check_interval)
            conn_error = str(exc)
        else:
            return True
    raise RuntimeError(conn_error)


@pytest.fixture(scope="session")
def free_port() -> int:
    """
    Return a free port on localhost
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        addr = s.getsockname()
        port = addr[1]
        return port


def run_server(port):
    uvicorn.run(app, port=port)
{% endif %}

{% if cookiecutter.project_backend == "flask" %}
{% if 'postgres' in cookiecutter.db_resource %}
{% from 'conftest_flask_postgres.py' import app with context %}
{% endif %}
{% if 'mongodb' in cookiecutter.db_resource %}
{% from 'conftest_flask_mongodb.py' import app with context %}
{% endif %}
{{app()}}
{% endif %}

{% if cookiecutter.project_backend == "django" %}
@pytest.fixture(scope="function")
def django_db_setup(django_db_setup, django_db_blocker):
    """ Overrides the default django_db_setup fixture to load the seed data
    https://pytest-django.readthedocs.io/en/latest/database.html#populate-the-test-database-if-you-use-transactional-or-live-server
    """
    with django_db_blocker.unblock():
        call_command("loaddata", "src/seed_data.json")


@pytest.fixture(scope="session", autouse=True)
def mock_functions_env():
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


@pytest.fixture(scope="session")
def live_server_url(live_server):
    """Returns the url of the live server"""
    return live_server.url
{% endif %}
{% if cookiecutter.project_backend == "fastapi" %}
@pytest.fixture(scope="session")
def live_server_url(free_port: int):
    """Returns the url of the live server"""
    seed_data.load_from_json()
    proc = Process(target=run_server, args=(free_port,), daemon=True)
    proc.start()
    url = f"http://localhost:{free_port}"
    wait_for_server_ready(url, timeout=10.0, check_interval=0.5)
    yield url
    proc.kill()
    seed_data.drop_all()
{% endif %}
{% if cookiecutter.project_backend == "flask" %}
@pytest.fixture(scope="function")
def live_server_url(app, live_server):
    """Returns the url of the live server"""
    return url_for("pages.index", _external=True)
{% endif %}
