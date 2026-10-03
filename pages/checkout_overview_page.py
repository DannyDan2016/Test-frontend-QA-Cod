from playwright.sync_api import Page

from pages.authenticated_page import AuthenticatedPage


class CheckoutOverviewPage(AuthenticatedPage):
    """Paso 2 del checkout ("Checkout: Overview"): resumen de la compra e importes."""

    path = "/checkout-step-two.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.item_names = page.get_by_test_id("inventory-item-name")
        self.subtotal = page.get_by_test_id("subtotal-label")
        self.tax = page.get_by_test_id("tax-label")
        self.total = page.get_by_test_id("total-label")
        self.finish_button = page.get_by_test_id("finish")

    def finish(self) -> None:
        self.finish_button.click()
