from playwright.sync_api import Page

from pages.base_page import BasePage


class CheckoutSummaryPage(BasePage):
    path = "/checkout-step-two.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.subtotal = page.get_by_test_id("subtotal-label")
        self.tax = page.get_by_test_id("tax-label")
        self.total = page.get_by_test_id("total-label")
        self.finish_button = page.get_by_test_id("finish")

    def complete_purchase(self) -> None:
        self.finish_button.click()
