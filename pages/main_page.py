from playwright.sync_api import Page
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class MainPage(BasePage):
    OPEN_TMS_BUTTON = (By.CSS_SELECTOR, '[href="/dashboard"]')

    def __init__(self, page: Page):
        self.url = "/"
        super().__init__(page, self.url)

    def open_tms_app(self):
        self.click(self.OPEN_TMS_BUTTON)

    def assert_that_main_page_opened(self):
        self.assert_that_page_opened()
        self.assert_element_visible(self.OPEN_TMS_BUTTON)
