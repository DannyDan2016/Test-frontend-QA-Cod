import re
from typing import Self
from urllib.parse import urlencode

from playwright.sync_api import Page


class BasePage:
    """Base común de los page objects: guarda la página y navega por ruta relativa."""

    path = "/"

    def __init__(self, page: Page) -> None:
        self.page = page

    @property
    def url_pattern(self) -> re.Pattern[str]:
        """Patrón de la URL de la página (con o sin query string) para ``to_have_url``."""
        return re.compile(rf"{re.escape(self.path)}(\?.*)?$")

    def open(self, **query: str | int) -> Self:
        """Navega a la ruta de la página; el host lo aporta base_url (pytest-base-url).

        SauceDemo responde HTTP 404 en las rutas profundas aunque la SPA las renderiza
        bien, por eso no se valida el código de la respuesta.
        """
        destino = f"{self.path}?{urlencode(query)}" if query else self.path
        self.page.goto(destino)
        return self
