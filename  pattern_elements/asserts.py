from playwright.sync_api import expect


class Assertions:

    def __init__(self, locator):
        self.locator = locator

    def assert_element_visible(self):
        expect(self.locator).to_be_visible()

    def assert_text_in_element(self, text):
        expect(self.locator).to_have_text(text)

    def assert_text_contain_in_element(self, text):
        expect(self.locator).to_contain_text(text)
