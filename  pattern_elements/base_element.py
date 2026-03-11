import allure
from playwright.sync_api import Locator, Page


class BaseElement:
    def __init__(
        self,
        page: Page,
        selector,
        timeout=10000,
    ):
        self.page: Page = page
        self.selector = selector
        self.timeout = timeout

    def _locator(self) -> Locator:
        return self.page.locator(self.selector)

    @allure.step("Wait for element: {self._selector_str}")
    def wait_visible(self) -> Locator:
        el = self._locator()
        el.wait_for(state="visible", timeout=self.timeout)
        el.scroll_into_view_if_needed()
        return el

    @allure.step("Click on element with force={is_force}")
    def click(self, is_force=False):
        el = self.wait_visible()
        if is_force:
            el.scroll_into_view_if_needed()
            el.dispatch_event("click")
        else:
            el.click(timeout=self.timeout)

    def send_keys(self, value: str):
        self.wait_visible().fill(value)

    def select_item_by_value(self, value: str):
        self.wait_visible().select_option(value=value)

    def select_item_by_visible_text(self, visible_text: str):
        self.wait_visible().select_option(label=visible_text)

    def assert_element_visible(self):
        el = self.wait_visible()
        assert el.is_visible(), f"Element '{self.selector}' is not visible on the page"

    def assert_text_in_element(self, text: str):
        el = self.wait_visible()
        assert el.text_content() == text, (
            f"Element does not have text: {text}, got: {el.text_content()}"
        )

    def assert_text_contain_in_element(self, text: str):
        el = self.wait_visible()
        content = el.text_content() or ""
        assert text in content, f"Element does not contain text: {text}"
