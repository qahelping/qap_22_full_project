import allure
from playwright.sync_api import Page
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class DashboardPage(BasePage):
    CREATE_BOARD_BUTTON = (By.CSS_SELECTOR, '[data-qa="dashboard-create-board-button"]')

    def __init__(self, page: Page):
        self.url = "/dashboard"
        super().__init__(page, self.url)

    @allure.step("Assert that dashboard opened")
    def assert_that_dashboard_opened(self):
        self.assert_that_page_opened()
        self.assert_element_visible(self.CREATE_BOARD_BUTTON)
