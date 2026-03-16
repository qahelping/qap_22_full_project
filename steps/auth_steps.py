from core.web.local_starage import LocalStorage
from pages.login_page import LoginPage
from services.authentication_service import AuthServices
from steps.main_steps import MainSteps


class AuthStep:
    def __init__(self, driver):
        self.driver = driver


    def login(self, user):
        main_steps = MainSteps(self.driver)
        auth_service = AuthServices()
        token = auth_service.get_token(user.email, user.password)
        main_steps.open_tms()
        LocalStorage(self.driver).add_local_storage('token', token)
        main_steps.open_tms()
        login_page = LoginPage(self.driver)
        login_page.login_form_is_not_visible()

