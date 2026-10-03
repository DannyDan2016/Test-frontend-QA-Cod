from playwright.sync_api import Page

from pages.authenticated_page import AuthenticatedPage


class CheckoutCompletePage(AuthenticatedPage):
    """Confirmación del pedido ("Checkout: Complete!")."""

    path = "/checkout-complete.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.complete_header = page.get_by_test_id("complete-header")
        self.back_home_button = page.get_by_test_id("back-to-products")
