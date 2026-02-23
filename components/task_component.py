from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class TaskComponent(BasePage):

    def __init__(self, driver, card_id):
        self.driver: WebDriver = driver

        self.component = f'[data-qa="task-card-content-{card_id}"]'
        self.COMPONENT = (By.CSS_SELECTOR, f"{self.component}")
        self.TASK_ASSIGN = (By.CSS_SELECTOR, f"{self.component} .task-card-assignee")
        self.TASK_TITLE = (By.CSS_SELECTOR, f"{self.component} .task-card-title")
        self.TASK_EDIT = (By.CSS_SELECTOR, f"{self.component} .task-card-edit-btn")
        super().__init__(driver)

    def open_edit_form(self):
        self.click(self.TASK_EDIT)

    def assert_assign_name(self, name):
        self.assert_element_visible(self.TASK_ASSIGN)
        self.assert_text_in_element(self.TASK_ASSIGN, name)

