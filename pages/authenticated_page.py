from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.components import Header, Menu


class AuthenticatedPage(BasePage):
    """Página que requiere sesión: incluye la cabecera y el menú lateral compartidos."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.header = Header(page)
        self.menu = Menu(page)
