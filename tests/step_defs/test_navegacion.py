"""Steps del menú lateral: logout y Reset App State."""

from playwright.sync_api import BrowserContext
from pytest_bdd import scenarios, then, when

from pages.components import Menu
from support.datos import Datos

scenarios("navegacion")


@when("cierro sesión desde el menú")
def cerrar_sesion(menu: Menu) -> None:
    menu.logout()


@when("restablezco el estado de la aplicación desde el menú")
def restablecer_estado(menu: Menu) -> None:
    menu.reset_app_state()


@then("ya no tengo la sesión iniciada")
def sin_cookie_de_sesion(context: BrowserContext, datos: Datos) -> None:
    cookie = datos("sesion.cookie")
    nombres = [c["name"] for c in context.cookies()]
    assert cookie not in nombres, f"la cookie '{cookie}' sigue presente tras el logout"
