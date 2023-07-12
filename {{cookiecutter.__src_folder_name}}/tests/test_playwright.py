# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import re
import os
import pytest
from playwright.sync_api import expect, Page, expect


@pytest.fixture(scope="session")
def mock_functions_env():
    os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = "true"

def expect_header_url_test(page:Page, url:str, name: str, re_str: str) -> None:
    """Helper function to test that a link has a certain attribute"""
    page.goto(url)
    header = page.locator("nav")

    # Request Info
    request_info = header.get_by_role("link", name=name)
    expect(request_info).to_have_attribute("href", re.compile(re_str))


def test_home(mock_functions_env, page: Page, live_server):
    """Test that the home page loads"""
    page.goto(live_server.url)
    expect(page).to_have_title("ReleCloud - Expand your horizons")
    page.close()


def test_header_has_request_info(mock_functions_env, page: Page, live_server):
    """Test that the header loads with links"""

    header_links = (
        ("Request Information", ".*info.*"),
        ("Destinations", ".*destination.*"),
        ("About", ".*about.*"),
    )

    for title, re_str in header_links:
        expect_header_url_test(
            page,
            url=live_server.url,
            name=title,
            re_str=re_str,
        )
    page.close()


def test_request_information(mock_functions_env, page: Page, live_server):
    """Test that the request info form page loads"""
    page.goto(live_server.url)
    page.get_by_role("link", name="Request Information").click()
    expect(page).to_have_title("ReleCloud - Request information")
    page.close()


def test_destinations_(mock_functions_env, page: Page, live_server):
    """Test that the request info form page loads"""
    page.goto(live_server.url)
    page.get_by_role("link", name="Destinations").click()
    expect(page).to_have_title("ReleCloud - Destinations")
    page.close()


def test_about(mock_functions_env, page: Page, live_server):
    """Test that the request info form page loads"""
    page.goto(live_server.url)
    page.get_by_role("link", name="About").click()
    expect(page).to_have_title("ReleCloud - About")
    expect(page).to_have_text("About ReleCloud")
    page.close()