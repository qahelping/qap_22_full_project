import time

from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from pages.main_page import MainPage
from test_data.users import CHARLI


def test_login(driver):
    main_page = MainPage(driver)
    main_page.open()
    main_page.open_tms_app()
    time.sleep(5)
    login_page = LoginPage(driver)
    login_page.login(CHARLI)

    dashboard_page = DashboardPage(driver)
    dashboard_page.assert_that_dashboard_opened()
