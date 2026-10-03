import re

from playwright.sync_api import Page

from pages.authenticated_page import AuthenticatedPage


class SpinnerPage(AuthenticatedPage):
    """Dynamic Catalog - Spinner: muestra un indicador de carga (0,5-3 s aleatorios) y
    después la rejilla de productos."""

    path = "/dynamic-catalog-spinner.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        # Rol accesible del indicador: role="status" con aria-label="Loading"
        self.spinner = page.get_by_role("status", name="Loading")
        self.grid = page.get_by_test_id("dynamic-catalog-spinner-grid")
        self.item_names = self.grid.get_by_test_id(re.compile(r"^spinner-item-\d+-name$"))
        self.item_prices = self.grid.get_by_test_id(re.compile(r"^spinner-item-\d+-price$"))
