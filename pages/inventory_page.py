from playwright.sync_api import Page

from pages.authenticated_page import AuthenticatedPage


class InventoryPage(AuthenticatedPage):
    path = "/inventory.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.items = page.get_by_test_id("inventory-item")
        self.item_names = page.get_by_test_id("inventory-item-name")
        self.item_prices = page.get_by_test_id("inventory-item-price")

    def _item(self, product_name: str):
        return self.items.filter(has=self.page.get_by_text(product_name, exact=True))

    def add_to_cart(self, product_name: str) -> None:
        self._item(product_name).get_by_role("button", name="Add to cart").click()

    def remove_from_cart(self, product_name: str) -> None:
        self._item(product_name).get_by_role("button", name="Remove").click()
