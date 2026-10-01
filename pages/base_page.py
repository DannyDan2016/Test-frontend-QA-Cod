from playwright.sync_api import Page


class BasePage:
    """Base común de los page objects: guarda la página y navega por ruta relativa."""

    path = "/"

    def __init__(self, page: Page) -> None:
        self.page = page

    def open(self):
        """Navega a la ruta de la página; el host lo aporta base_url (pytest-base-url)."""
        self.page.goto(self.path)
        return self
