{# standard library imports #}
{% if cookiecutter.project_backend == "fastapi" %}
from multiprocessing import Process
{% endif %}
{% if cookiecutter.project_backend == "flask" %}
import os
import pathlib
{% endif %}

{# third-party library imports #}
{% if cookiecutter.project_backend == "django" %}
from django.core.management import call_command
{% endif %}
import pytest
{% if cookiecutter.project_backend == "flask" %}
from flask import url_for
{% endif %}
{% if cookiecutter.project_backend == "fastapi" %}
import uvicorn
{% endif %}

{# Local imports #}
{% if cookiecutter.project_backend == "fastapi" %}
import seed_data
from app import app
{% endif %}
{% if cookiecutter.project_backend == "flask" %}
from flaskapp import create_app, db, seeder
{% endif %}

{% if cookiecutter.project_backend == "fastapi" %}
def run_server():
    uvicorn.run(app)

@pytest.fixture(scope="session")
def live_server():
    seed_data.load_from_json()
    proc = Process(target=run_server, daemon=True)
    proc.start()
    yield
    proc.kill()
    seed_data.drop_all()
{% endif %}

{% if cookiecutter.project_backend == "flask" %}
@pytest.fixture(scope="session")
def app():
    """Session-wide test `Flask` application."""
    config_override = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get(
            "TEST_DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres"
        ),
    }
    app = create_app(config_override)

    with app.app_context():
        engines = db.engines
        db.create_all()
        seeder.seed_data(db, pathlib.Path(__file__).parent.parent / "seed_data.json")

    engine_cleanup = []

    for key, engine in engines.items():
        connection = engine.connect()
        transaction = connection.begin()
        engines[key] = connection
        engine_cleanup.append((key, engine, connection, transaction))

    yield app

    for key, engine, connection, transaction in engine_cleanup:
        transaction.rollback()
        connection.close()
        engines[key] = engine
{% endif %}
{% if cookiecutter.project_backend == "django" %}
@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", "seed_data.json")
{% endif %}


@pytest.fixture(scope="session")
def mock_functions_env():
    {% if cookiecutter.project_backend == "django" %}
    os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = "true"
    {% else %}
    pass
    {% endif %}


{% if cookiecutter.project_backend == "django" %}
@pytest.fixture(scope="session")
def live_server_url(live_server):
    """Returns the url of the live server"""
    return live_server.url
{% endif %}
{% if cookiecutter.project_backend == "fastapi" %}
@pytest.fixture(scope="session")
def live_server_url(live_server):
    """Returns the url of the live server"""
    return "http://localhost:8000"
{% endif %}
{% if cookiecutter.project_backend == "flask" %}
@pytest.fixture(scope="function")
def live_server_url(app, live_server):
    """Returns the url of the live server"""
    return url_for("pages.index", _external=True)
{% endif %}
