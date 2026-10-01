"""Steps de autenticación: login y páginas protegidas por sesión."""

from playwright.sync_api import BrowserContext, Page, expect
from pytest_bdd import given, parsers, scenarios, then, when

from pages import (
    AuthenticatedPage,
    CartPage,
    CheckoutInformationPage,
    InventoryPage,
    LoginPage,
)
from pages.dynamic_catalog import SpinnerPage
from support.aserciones import verificar_pagina
from support.datos import Datos

scenarios("autenticacion")

# Clave usada en los .feature -> page object de la página protegida
PAGINAS_PROTEGIDAS: dict[str, type[AuthenticatedPage]] = {
    "inventario": InventoryPage,
    "carrito": CartPage,
    "checkout_informacion": CheckoutInformationPage,
    "catalogo_con_spinner": SpinnerPage,
}


@when(parsers.parse('intento iniciar sesión con el caso "{caso}"'))
def login_invalido(login_page: LoginPage, datos: Datos, caso: str) -> None:
    credenciales = datos(f"login.casos_invalidos.{caso}")
    login_page.login(credenciales["usuario"], credenciales["password"])


@then(parsers.parse('veo el error de login del caso "{caso}"'))
def error_de_login(login_page: LoginPage, datos: Datos, caso: str) -> None:
    expect(login_page.error).to_have_text(datos(f"login.casos_invalidos.{caso}.error"))


@then("sigo en la página de login")
def sigo_en_login(login_page: LoginPage) -> None:
    verificar_pagina(login_page)
    expect(login_page.login_button).to_be_visible()


@given("que no he iniciado sesión")
def sin_sesion(context: BrowserContext, datos: Datos) -> None:
    cookie = datos("sesion.cookie")
    assert all(c["name"] != cookie for c in context.cookies()), "el contexto ya tiene sesión"


@when(parsers.parse('accedo directamente a la página "{pagina}"'))
def acceso_directo(page: Page, pagina: str) -> None:
    PAGINAS_PROTEGIDAS[pagina](page).open()


@then(parsers.parse('vuelvo al login con el aviso de acceso restringido a "{pagina}"'))
def aviso_acceso_restringido(login_page: LoginPage, datos: Datos, pagina: str) -> None:
    ruta = PAGINAS_PROTEGIDAS[pagina].path
    verificar_pagina(login_page)
    expect(login_page.error).to_have_text(
        datos("sesion.mensaje_acceso_restringido").format(ruta=ruta)
    )
