from playwright.sync_api import Page

from pages.base_page import BasePage


class InventoryPage(BasePage):
    path = "/inventory.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.items = page.get_by_test_id("inventory-item")
        self.cart_badge = page.get_by_test_id("shopping-cart-badge")
        self.cart_link = page.get_by_test_id("shopping-cart-link")

    def add_to_cart(self, product_name: str) -> None:
        self.items.filter(has_text=product_name).get_by_role("button", name="Add to cart").click()

    def open_cart(self) -> None:
        self.cart_link.click()
