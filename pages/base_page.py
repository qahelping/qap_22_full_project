import allure
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from config import BaseConfig


class BasePage:

    def __init__(self, driver, url=None, timeout=BaseConfig.WEB_DRIVER_WAIT, title='Task Management Board'):
        self.driver: WebDriver = driver
        self.url = url
        self.title = title

        self.wait = WebDriverWait(driver, timeout)

    def open(self, with_path=None):
        with allure.step(f"Open page: {self.url}"):
            url = f"{BaseConfig.ROOT_PATH}{self.url}{with_path}" if with_path else f"{BaseConfig.ROOT_PATH}{self.url}"
            self.driver.get(url)

    @allure.step("Wait for: {locator}")
    def wait_visible(self, locator):
        el = self.wait.until(EC.visibility_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        return el


    @allure.step("Wait for disappear: {locator}")
    def wait_invisibility_of_element(self, locator):
        el = self.wait.until(EC.invisibility_of_element(locator))
        return el

    def wait_page_opened(self):
        with  allure.step(f"Wait for page: {self.url}"):
            self.wait.until(EC.url_contains(self.url))

    @allure.step("Click on: {locator} with force={is_force}")
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

    def select_item_by_value(self, locator, value):
        el = self.wait_visible(locator)
        select = Select(el)
        select.select_by_value(value)

    def select_item_by_visible_text(self, locator, visible_text):
        el = self.wait_visible(locator)
        select = Select(el)
        select.select_by_visible_text(visible_text)

    def assert_element_visible(self, locator):
        el = self.wait_visible(locator)
        assert el.is_displayed(), f"Element '{locator[-1]}' does not found on the page"

    def assert_text_in_element(self, locator, text):
        el = self.wait_visible(locator)
        assert el.text == text, f"Element '{locator[-1]}' does not have text: {text}"

    def assert_text_contain_in_element(self, locator, text):
        el = self.wait_visible(locator)
        assert text in el.text, f"Element '{locator[-1]}' does not contain text: {text}"


    def assert_that_page_opened(self):
        self.wait_page_opened()

        assert self.url in self.driver.current_url, f"Expected: {self.url}, but {self.driver.current_url}"
        assert self.title == self.driver.title
