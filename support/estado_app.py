"""Precondiciones rápidas: sesión por cookie y carrito por localStorage.

Sirven para preparar el estado de los escenarios que NO prueban el login ni el
añadido al carrito, sin pasar por la UI (más rápido y sin dependencias entre áreas).
"""

from playwright.sync_api import BrowserContext, Page


def iniciar_sesion_por_cookie(
    context: BrowserContext, base_url: str, cookie: str, usuario: str
) -> None:
    """Crea la cookie de sesión que la app escribe tras un login correcto."""
    context.add_cookies([{"name": cookie, "value": usuario, "url": base_url}])


def precargar_carrito(page: Page, clave: str, ids_productos: list[int]) -> None:
    """Escribe el carrito en localStorage y recarga para que la app lo lea.

    La página debe estar ya en el dominio de la app (localStorage es por origen).
    """
    page.evaluate(
        "([clave, ids]) => localStorage.setItem(clave, JSON.stringify(ids))",
        [clave, ids_productos],
    )
    page.reload()
