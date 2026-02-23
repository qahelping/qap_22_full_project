from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class EditTaskModalComponent(BasePage):

    def __init__(self, driver):
        self.driver: WebDriver = driver

        self.component = '[data-qa="edit-task-modal"]'
        self.COMPONENT = (By.CSS_SELECTOR, f"{self.component}")

        self.CLOSE_BUTTON = (By.CSS_SELECTOR, f'{self.component} [data-qa="modal-close-button"]')
        self.FORM = (By.CSS_SELECTOR, f'{self.component} [data-qa="edit-task-form"]')

        self.TITLE_INPUT = (By.CSS_SELECTOR, f'{self.component} [data-qa="edit-task-title-input"]')
        self.DESCRIPTION_TEXTAREA = (By.CSS_SELECTOR, f'{self.component} [data-qa="edit-task-description-textarea"]')
        self.STATUS_SELECT = (By.CSS_SELECTOR, f'{self.component} [data-qa="edit-task-status-select"]')
        self.PRIORITY_SELECT = (By.CSS_SELECTOR, f'{self.component} [data-qa="edit-task-priority-select"]')
        self.ASSIGNEE_SELECT = (By.CSS_SELECTOR, f'{self.component} [data-qa="edit-task-assignee-select"]')

        self.DELETE_BUTTON = (By.CSS_SELECTOR, f'{self.component} [data-qa="edit-task-delete-button"]')
        self.CANCEL_BUTTON = (By.CSS_SELECTOR, f'{self.component} [data-qa="edit-task-cancel-button"]')
        self.SAVE_BUTTON = (By.CSS_SELECTOR, f'{self.component} [data-qa="edit-task-save-button"]')

        super().__init__(driver, self.url)

    def close_modal(self):
        self.click(self.CLOSE_BUTTON)

    def save(self):
        self.click(self.SAVE_BUTTON)

    def delete(self):
        self.click(self.DELETE_BUTTON)

    def set_title(self, title):
        self.send_keys(self.TITLE_INPUT, title)

    def set_description(self, text: str):
        self.send_keys(self.DESCRIPTION_TEXTAREA, text)

    def select_assignee(self, value: str):
        self.select_item_by_visible_text(self.ASSIGNEE_SELECT, value)
