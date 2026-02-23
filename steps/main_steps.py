from pages.login_page import LoginPage
from pages.main_page import MainPage


class MainSteps:
    def __init__(self, driver):
        self.main_page = MainPage(driver)
        self.login_page = LoginPage(driver)

    def open_tms(self):
        self.main_page.open()
        self.main_page.open_tms_app()

        self.login_page.assert_that_page_opened()
