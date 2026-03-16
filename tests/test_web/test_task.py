import allure
import pytest

from components.edit_task_modal_component import EditTaskModalComponent
from components.task_component import TaskComponent
from pages.board_page import BoardPage
from steps.auth_steps import AuthStep
from test_data.users import ADMIN


@pytest.mark.tms
@allure.epic("Task management system")
class TestTMS2:
    @pytest.mark.task_auth
    @allure.feature("Task")
    class TestTasks2:

        @pytest.mark.smoke1
        @allure.title("Assign user")
        def test_assign_on2(self, driver):
            """Test for assign user"""
            auth = AuthStep(driver)
            auth.login(ADMIN)

            board_page = BoardPage(driver)
            board_page.open_board_by_id('2')

            # создание задачи через АПИ
            task_component = TaskComponent(driver, 10)
            task_component.open_edit_form()

            edit_modal = EditTaskModalComponent(driver)
            edit_modal.select_assignee('diana')
            edit_modal.save()

            task_component.assert_assign_name('diana')

            # удалить задачу через BD или API
