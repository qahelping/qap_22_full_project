import time

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions


# def generate_path():
#     os.makedirs("artifacts/screenshots", exist_ok=True)
#
#     ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#     name = _safe_name(request.node.nodeid)
#     return f"artifacts/screenshots/{name}__{ts}.png"


def pytest_addoption(parser):
    parser.addoption("--br", action="store", default="chrome", help="the name of the browser")
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


@pytest.fixture(autouse=False)
def driver(request, pytestconfig):
    browser = pytestconfig.getoption("--br")
    if browser == "firefox":
        opts = FirefoxOptions()
        opts.add_argument("--width=1980")
        opts.add_argument("--height=1600")
        web_driver = webdriver.Firefox(options=opts)

    else:
        opts = Options()
        # opts.add_argument("--headless=new")
        opts.add_argument("--incognito")

        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        }
        opts.add_experimental_option("prefs", prefs)

        web_driver = webdriver.Chrome(options=opts)
        web_driver.maximize_window()
        web_driver.implicitly_wait(3)

    yield web_driver

    report = getattr(request.node, "rep_call", None)

    if report:
        try:
            allure.attach(
                web_driver.get_screenshot_as_png(),
                name="screenshot",
                attachment_type=allure.attachment_type.PNG,
            )

            allure.attach(
                web_driver.current_url,
                name="Current url",
                attachment_type=allure.attachment_type.URI_LIST,
            )
        except Exception as e:
            print(f"Failed to attach: {e}")

    web_driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


# @pytest.fixture(autouse=False, params=["chrome"])
# def driver(request):
#     if request.param == "firefox":
#         opts = FirefoxOptions()
#         opts.add_argument("--width=1980")
#         opts.add_argument("--height=1600")
#         web_driver = webdriver.Firefox(options=opts)
#
#     else:
#         opts = Options()
#         # opts.add_argument("--headless=new")
#         opts.add_argument("--incognito")
#
#         prefs = {
#             "credentials_enable_service": False,
#             "profile.password_manager_enabled": False,
#             "profile.password_manager_leak_detection": False,
#         }
#         opts.add_experimental_option("prefs", prefs)
#
#         web_driver = webdriver.Chrome(options=opts)
#         web_driver.maximize_window()
#         web_driver.implicitly_wait(3)
#
#     yield web_driver
#     web_driver.quit()
@pytest.fixture()
def login(driver):
    URL = "http://localhost:3000/login"

    driver.get(URL)
    email = driver.find_element(By.CSS_SELECTOR, '[data-qa="login-email-input"]')
    password = driver.find_element(By.CSS_SELECTOR, '[data-qa="login-password-input"]')
    submit = driver.find_element(By.CLASS_NAME, "btn-primary")

    email.send_keys("bob@example.com")
    password.send_keys("password123")
    submit.click()

    time.sleep(2)

    driver.execute_cdp_cmd("Page.setDownloadBehavior", {"behavior": "deny"})
    assert driver.current_url.endswith("/dashboard")

# //*[@id="card-expiry-input"]
