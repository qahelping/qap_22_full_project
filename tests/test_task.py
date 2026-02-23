import allure
import pytest

from components.edit_task_modal_component import  EditTaskModalComponent
from components.task_component import TaskComponent
from pages.board_page import BoardPage
from pages.login_page import LoginPage
from steps.main_steps import MainSteps
from test_data.users import CHARLI, ADMIN


@pytest.mark.tms
@allure.epic("Task management system")
class TestTMS:
    @pytest.mark.task
    @allure.feature("Task")
    class TestTasks:

        @pytest.mark.smoke
        @allure.title("Assign user")
        def test_assign_on(self, driver):
            """Test for assign user"""

            main_steps = MainSteps(driver)
            main_steps.open_tms()

            login_page = LoginPage(driver)
            login_page.login(ADMIN)


            board_page = BoardPage(driver)
            board_page.open_board_by_id('2')

            task_component = TaskComponent(driver, 10)
            task_component.open_edit_form()

            edit_modal = EditTaskModalComponent(driver)
            edit_modal.select_assignee('diana')
            edit_modal.save()

            task_component.assert_assign_name('diana')
