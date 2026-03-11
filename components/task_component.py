from playwright.sync_api import Page

from pages.base_page import BasePage


class TaskComponent(BasePage):
    def __init__(self, page: Page, card_id):
        self.component = f'[data-qa="task-card-content-{card_id}"]'
        self.TASK_ASSIGN = f"{self.component} .task-card-assignee"
        self.TASK_TITLE = f"{self.component} .task-card-title"
        self.TASK_EDIT = f"{self.component} .task-card-edit-btn"
        super().__init__(page, url=None)

    def open_edit_form(self):
        self.click(self.TASK_EDIT)

    def assert_assign_name(self, name):
        self.assert_element_visible(self.TASK_ASSIGN)
        self.assert_text_contain_in_element(self.TASK_ASSIGN, name)
