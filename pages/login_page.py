from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from config import BaseConfig
from pages.base_page import BasePage
from test_data.users import User


class LoginPage(BasePage):
    # LOGIN_INPUT = 'login-email-input'
    # PASSWORD_INPUT = 'login-password-input'
    # SUBMIT = 'login-submit-button'

    # LOGIN_INPUT = '#id-input-login-email-input'
    # PASSWORD_INPUT = '[id="id-input-login-password-input"]'
    # SUBMIT = '[data-qa="login-submit-button"]'

    LOGIN_INPUT = (By.ID, 'id-input-login-email-input')
    PASSWORD_INPUT = (By.CSS_SELECTOR, '[id="id-input-login-password-input"]')
    SUBMIT = (By.XPATH, '//*[@data-qa="login-submit-button"]')

    def __init__(self, driver):
        self.url = '/login'

        super().__init__(driver, self.url)
        self.driver: WebDriver = driver


    def open(self):
        self.driver.get(f"{BaseConfig.ROOT_PATH}{self.url}")

    def login(self, user: User):
        self.send_keys(self.LOGIN_INPUT, user.email)
        self.send_keys(self.PASSWORD_INPUT, user.password)

        self.click(self.SUBMIT)
