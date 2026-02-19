import allure
import pytest

from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from pages.main_page import MainPage
from test_data.users import CHARLI


@pytest.mark.tms
@allure.epic("Task management system")
class TestTMS:
    @pytest.mark.auth
    @allure.feature("Auth")
    class TestAuth:

        @pytest.mark.smoke
        @allure.title("Login")
        def test_login(self, driver):
            """Test for login simple user"""

            main_page = MainPage(driver)
            main_page.open()
            main_page.open_tms_app()

            login_page = LoginPage(driver)
            login_page.login(CHARLI)

            dashboard_page = DashboardPage(driver)
            dashboard_page.assert_that_dashboard_opened()
