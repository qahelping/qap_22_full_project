import allure
import pytest
from playwright.sync_api import Page


def pytest_addoption(parser):
    parser.addoption(
        "--br",
        action="store",
        default="chromium",
        help="Browser: chromium, firefox, webkit",
    )
    parser.addoption(
        "--app",
        default=None,
        help="Path to mobile app file (.apk for Android, .app/.ipa for iOS)",
    )
    parser.addoption(
        "--allure-print",
        action="store_true",
        default=True,
        help="Включить вывод шагов Allure в консоль.",
    )
    parser.addoption(
        "--locale",
        action="store",
        default="en",
        help="Locale to run tests in (e.g. en, ru).",
    )


@pytest.fixture(scope="session")
def locale(pytestconfig):
    return pytestconfig.getoption("--locale")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture()
def login(page: Page):
    """Залогинить пользователя и перейти на dashboard."""
    from config import BaseConfig

    url = f"{BaseConfig.ROOT_PATH}/login"
    page.goto(url)

    page.locator('[data-qa="login-email-input"]').fill("bob@example.com")
    page.locator('[data-qa="login-password-input"]').fill("password123")
    page.locator('[data-qa="login-submit-button"]').click()

    page.wait_for_url("**/dashboard", timeout=5000)
    assert "/dashboard" in page.url


@pytest.fixture(autouse=True)
def attach_on_failure(request, page: Page):
    yield
    report = getattr(request.node, "rep_call", None)
    if report and report.failed:
        try:
            allure.attach(
                page.screenshot(full_page=True),
                name="screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
            allure.attach(
                page.url,
                name="Current url",
                attachment_type=allure.attachment_type.URI_LIST,
            )
        except Exception as e:
            print(f"Failed to attach: {e}")
