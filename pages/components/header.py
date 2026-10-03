from playwright.sync_api import Page


class Header:
    """Cabecera compartida de las páginas autenticadas: título y acceso al carrito."""

    def __init__(self, page: Page) -> None:
        self.title = page.get_by_test_id("title")
        self.cart_link = page.get_by_test_id("shopping-cart-link")
        self.cart_badge = page.get_by_test_id("shopping-cart-badge")

    def open_cart(self) -> None:
        self.cart_link.click()
