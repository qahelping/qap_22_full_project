from playwright.sync_api import Page

from pages.base_page import BasePage


class EditTaskModalComponent(BasePage):
    def __init__(self, page: Page):
        self.component = '[data-qa="edit-task-modal"]'
        self.CLOSE_BUTTON = f'{self.component} [data-qa="modal-close-button"]'
        self.FORM = f'{self.component} [data-qa="edit-task-form"]'
        self.TITLE_INPUT = f'{self.component} [data-qa="edit-task-title-input"]'
        self.DESCRIPTION_TEXTAREA = f'{self.component} [data-qa="edit-task-description-textarea"]'
        self.STATUS_SELECT = f'{self.component} [data-qa="edit-task-status-select"]'
        self.PRIORITY_SELECT = f'{self.component} [data-qa="edit-task-priority-select"]'
        self.ASSIGNEE_SELECT = f'{self.component} [data-qa="edit-task-assignee-select"]'
        self.DELETE_BUTTON = f'{self.component} [data-qa="edit-task-delete-button"]'
        self.CANCEL_BUTTON = f'{self.component} [data-qa="edit-task-cancel-button"]'
        self.SAVE_BUTTON = f'{self.component} [data-qa="edit-task-save-button"]'
        super().__init__(page, url=None)

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
