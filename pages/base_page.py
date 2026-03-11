import re

import allure
from playwright.sync_api import Locator, Page, expect

from config import BaseConfig


def _to_selector(locator):
    """Преобразует (By.XXX, selector) в строку для Playwright или возвращает строку как есть."""
    if isinstance(locator, tuple):
        by, selector = locator
        by_name = getattr(by, "name", str(by)) if hasattr(by, "name") else str(by)
        if by_name == "ID":
            return f"#{selector}"
        if by_name == "XPATH":
            return f"xpath={selector}"
        return selector
    return locator


class BasePage:
    def __init__(
        self,
        page: Page,
        url=None,
        timeout=BaseConfig.WEB_DRIVER_WAIT * 1000,
        title="Task Management Board",
    ):
        self.page: Page = page
        self.url = url
        self.title = title
        self.timeout = timeout

    def open(self, with_path=None):
        if self.url is None:
            raise ValueError("Page url is not set")
        with allure.step(f"Open page: {self.url}"):
            url = (
                f"{BaseConfig.ROOT_PATH}{self.url}{with_path}"
                if with_path
                else f"{BaseConfig.ROOT_PATH}{self.url}"
            )
            self.page.goto(url, timeout=self.timeout)

    @allure.step("Wait for element")
    def wait_visible(self, locator) -> Locator:
        sel = _to_selector(locator)
        el = self.page.locator(sel)
        el.wait_for(state="visible", timeout=self.timeout)
        el.scroll_into_view_if_needed()
        return el

    def wait_page_opened(self):
        with allure.step(f"Wait for page: {self.url}"):
            pattern = re.compile(re.escape(self.url))
            expect(self.page).to_have_url(pattern, timeout=self.timeout)

    @allure.step("Click on element")
    def click(self, locator, is_force=False):
        el = self.wait_visible(locator)
        if is_force:
            el.scroll_into_view_if_needed()
            el.dispatch_event("click")
        else:
            el.click(timeout=self.timeout)

    def send_keys(self, locator, value):
        el = self.wait_visible(locator)
        text = str(value) if value is not None else ""
        el.fill(text)

    def select_item_by_value(self, locator, value):
        el = self.wait_visible(locator)
        el.select_option(value=value)

    def select_item_by_visible_text(self, locator, visible_text):
        el = self.wait_visible(locator)
        el.select_option(label=visible_text)

    def assert_element_visible(self, locator):
        el = self.wait_visible(locator)
        assert el.is_visible(), f"Element '{locator}' is not visible on the page"

    def assert_text_in_element(self, locator, text):
        el = self.wait_visible(locator)
        assert el.text_content() == text, (
            f"Element does not have text: {text}, got: {el.text_content()}"
        )

    def assert_text_contain_in_element(self, locator, text):
        el = self.wait_visible(locator)
        content = el.text_content() or ""
        assert text in content, f"Element does not contain text: {text}"

    def assert_that_page_opened(self):
        self.wait_page_opened()
        assert self.url in self.page.url, (
            f"Expected: {self.url}, but got {self.page.url}"
        )
        assert self.title == self.page.title()
