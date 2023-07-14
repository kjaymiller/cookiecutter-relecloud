import os
import pathlib
import re

import pytest
{% if cookiecutter.project_backend == "flask" %}
from flask import url_for
{% endif %}
{% if cookiecutter.project_backend == "django" %}
from django.core.management import call_command
{% endif %}
from playwright.sync_api import Page, expect

{% if cookiecutter.project_backend == "flask" %}
from flaskapp import create_app, db, seeder
{% endif %}

{% if cookiecutter.project_backend == "django" %}
@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", "seed_data.json")
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


@pytest.fixture(scope="session")
def mock_functions_env():
    {% if cookiecutter.project_backend == "django" %}
    os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = "true"
    {% else %}
    pass
    {% endif %}


def get_index_url(live_server):
    {% if cookiecutter.project_backend == "django" %}
    return live_server.url
    {% endif %}
    {% if cookiecutter.project_backend == "flask" %}
    return url_for('pages.index', _external=True)
    {% endif %}


def expect_header_url_test(page:Page, url:str, name: str, re_str: str) -> None:
    """Helper function to test that a link has a certain attribute"""


def test_home(mock_functions_env, page: Page, live_server):
    """Test that the home page loads"""
    page.goto(get_index_url(live_server))
    expect(page).to_have_title("ReleCloud - Expand your horizons")
    page.close()


@pytest.mark.parametrize(
    "page_title, page_url",
    (
        ("Request Information", "info"),
        ("Destinations", "destinations"),
        ("About", "about"),
    )
)
def test_header_has_request_info(mock_functions_env, page: Page, live_server, page_title, page_url):
    """Test that the header loads with links"""
    page.goto(get_index_url(live_server))
    header = page.locator("nav")

    # Request Info
    request_info = header.get_by_role("link", name=page_title)
    expect(request_info).to_have_attribute("href", re.compile(rf'.*{page_url}.*'))
    page.close()


def test_request_information(mock_functions_env, page: Page, live_server):
    """Test that the request info form page loads"""
    page.goto(get_index_url(live_server))
    page.get_by_role("link", name="Request Information").click()
    expect(page).to_have_title("ReleCloud - Request information")
    page.close()


def test_destinations(mock_functions_env, page: Page, live_server):
    page.goto(get_index_url(live_server))
    page.get_by_role("link", name="Destinations").click()
    expect(page).to_have_title("ReleCloud - Destinations")

destinations = (
    "The Sun",
    "Mercury",
    "Venus",
    "Earth",
    "Mars",
    "Jupyter",
    "Saturn",
    "Uranus",
    "Neptune",
    "Pluto",
)

cruises = (
    "The Sun Tour",
    "The Hot Tour",
    "The Cold Tour",
    "The Central Tour",
    "The Big Tour",
)

@pytest.mark.parametrize(
    "destination",
    destinations,
)
def test_destination_options(
    page: Page,
    mock_functions_env,
    live_server,
    destination,
    ):
    """Test that the destinations page loads with seeded data"""

    # Create a destination
    page.goto(get_index_url(live_server))

    page.get_by_role("link", name="Destinations").click()
    expect(page).to_have_title("ReleCloud - Destinations")
    expect(page.get_by_text(destination)).to_be_visible()

@pytest.mark.parametrize(
    "destination",
    destinations,
)
def test_destination_options_have_cruises(
    page: Page,
    mock_functions_env,
    live_server,
    destination
):
    page.goto(get_index_url(live_server))
    page.get_by_role("link", name="Destinations").click()
    page.get_by_role("link", name=destination).click()
    expect(page).to_have_url(re.compile(r".*destination/\d+", re.IGNORECASE))
    expect(page).to_have_title(f"ReleCloud - {destination}") 
    expect(page.locator("#page-title")).to_have_text(destination)
    page_cruises = page.locator(".list-group-item").all()

    for page_cruise in page_cruises:
        assert page_cruise.text_content() in cruises
    page.close()


def test_about(mock_functions_env, page: Page, live_server):
    """Test that the request info form page loads"""
    page.goto(get_index_url(live_server))
    page.get_by_role("link", name="About").click()
    expect(page.locator("#page-title")).to_have_text(re.compile(r".*about.*", re.IGNORECASE))
    page.close()
