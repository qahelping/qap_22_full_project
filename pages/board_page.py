import allure
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class BoardPage(BasePage):
    CREATE_BOARD_BUTTON = (By.CSS_SELECTOR, '[data-qa="dashboard-create-board-button"]')

    def __init__(self, driver):
        self.driver: WebDriver = driver
        self.url = '/boards'

        super().__init__(driver, self.url)


    def open_board_by_id(self, board_id: str):
        self.open(with_path=f'/{board_id}')

    @allure.step("Assert that board opened")
    def assert_that_dashboard_opened(self):
        self.assert_that_page_opened()
        self.assert_element_visible(self.CREATE_BOARD_BUTTON)


