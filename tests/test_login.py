from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from test_data.users import CHARLI


def test_login(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(CHARLI)

    dashboard_page = DashboardPage(driver)
    dashboard_page.assert_that_dashboard_opened()
