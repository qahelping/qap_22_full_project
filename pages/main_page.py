from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class MainPage(BasePage):
    OPEN_TMS_BUTTON = (By.CSS_SELECTOR, '[href="/dashboard"]')

    def __init__(self, driver):
        self.driver: WebDriver = driver
        self.url = '/'

        super().__init__(driver, self.url)

    def open_tms_app(self):
        self.click(self.OPEN_TMS_BUTTON)

    def assert_that_main_page_opened(self):
        self.assert_that_page_opened()
        self.assert_element_visible(self.OPEN_TMS_BUTTON)


