import allure
from playwright.sync_api import Page
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from test_data.users import User


class LoginPage(BasePage):
    LOGIN_INPUT = (By.CSS_SELECTOR, '[data-qa="login-email-input"]')
    PASSWORD_INPUT = (By.CSS_SELECTOR, '[data-qa="login-password-input"]')
    SUBMIT = (By.CSS_SELECTOR, '[data-qa="login-submit-button"]')

    def __init__(self, page: Page):
        self.url = "/login"
        super().__init__(page, self.url)

    @allure.step("Login with email {user}")
    def login(self, user: User):
        self.send_keys(self.LOGIN_INPUT, user.email)
        self.send_keys(self.PASSWORD_INPUT, user.password)
        self.click(self.SUBMIT)
