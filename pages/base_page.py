from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from config import BaseConfig


class BasePage:

    def __init__(self, driver, url, timeout=BaseConfig.WEB_DRIVER_WAIT, title='Task Management Board'):
        self.driver: WebDriver = driver
        self.url = url
        self.title = title

        self.wait = WebDriverWait(driver, timeout)

    def open(self):
        self.driver.get(f"{BaseConfig.ROOT_PATH}{self.url}")

    def wait_visible(self, locator):
        el = self.wait.until(EC.visibility_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        return el

    def wait_page_opened(self):
        self.wait.until(EC.url_contains(self.url))

    def click(self, locator, is_force=False):
        el = self.wait.until(EC.element_to_be_clickable(locator))
        if is_force:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
            self.driver.execute_script("arguments[0].click();", el)

        else:
            el.click()

    def send_keys(self, locator, value):
        el = self.wait_visible(locator)
        el.send_keys(value)

    def assert_element_visible(self, locator):
        el = self.wait_visible(locator)
        assert el.is_displayed(), f"Element '{locator[-1]}' does not found on the page"

    def assert_that_page_opened(self):
        self.wait_page_opened()

        assert self.url in self.driver.current_url, f"Expected: {self.url}, but {self.driver.current_url}"
        assert self.title == self.driver.title
