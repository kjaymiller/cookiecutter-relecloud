# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import os
import pytest
from playwright.sync_api import expect, Page, expect


    # def setUpClass(cls):
    #     os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    #     super().setUpClass()
    #     cls.playwright = sync_playwright().start()
    #     cls.browser = cls.playwright.chromium.launch()

    # @classmethod
    # def tearDownClass(cls):
    #     super().tearDownClass()
    #     cls.browser.close()
    #     cls.playwright.stop()

@pytest.fixture(scope="session")
def mock_functions_env():
    os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = "true"
    
def test_request_info(page: Page, live_server):
    page.goto(live_server.url)
    page.get_by_role("link", name="Request Information").click()
    expect(page).to_have_title("ReleCloud - Request information")
    # page.get_by_label("Name*").click()
    # page.get_by_label("Name*").fill("pamela")
    # page.get_by_label("Name*").press("Tab")
    # page.get_by_label("Email*").fill("pammyla.fox@gmail.com")
    # page.get_by_label("Email*").press("Tab")
    # page.get_by_role("combobox", name="Cruise*").select_option("The Sun Tour")
    # page.get_by_label("Notes*").click()
    # page.get_by_label("Notes*").fill("more mars rovers pls")
    # page.get_by_role("button", name="Save").click()
    # page.get_by_role("alert").click()
    # expect(page.locator("[role=alert]")).to_contain_text(
    #     "Thank you, pamela! We will email you when we have more information about The Sun"
    # )
    page.close()

    # def test_destinations(self):
    #     page = self.browser.new_page()
    #     page.goto(self.live_server_url)
    #     page.get_by_role("link", name="Destinations").click()
    #     expect(page.get_by_role("heading", name="Cruise destinations")).to_be_visible()
    #     page.get_by_role("link", name="Mars").click()
    #     expect(page.get_by_role("heading", name="Mars")).to_be_visible()
    #     expect(page.get_by_text("It's red")).to_be_visible()
    #     page.get_by_role("link", name="The Hot Tour").click()
    #     expect(page.get_by_role("heading", name="The Hot Tour")).to_be_visible()
    #     page.get_by_role("link", name="Mercury").click()
    #     expect(page.get_by_role("heading", name="Mercury")).to_be_visible()

    # def test_about(self):
    #     page = self.browser.new_page()
    #     page.goto(self.live_server_url)
    #     page.get_by_role("link", name="About").click()
    #     expect(page.get_by_role("heading", name="About ReleCloud")).to_be_visible()

    # def test_admin_login_not_allowed(self):
    #     page = self.browser.new_page()
    #     page.goto(f"{self.live_server_url}/admin/")
    #     page.wait_for_selector("text=Django administration")
    #     page.fill("[name=username]", "myuser")
    #     page.fill("[name=password]", "secret")
    #     page.click("text=Log in")
    #     assert len(page.eval_on_selector(".errornote", "el => el.innerText")) > 0
    #     page.close()
