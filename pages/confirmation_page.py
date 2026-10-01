from playwright.sync_api import Page

from pages.base_page import BasePage


class ConfirmationPage(BasePage):
    path = "/checkout-complete.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.complete_header = page.get_by_test_id("complete-header")
