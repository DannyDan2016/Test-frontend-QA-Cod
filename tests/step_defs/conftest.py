"""Fixtures de navegador y steps compartidos por todas las features.

Los steps son delgados: delegan las acciones en los page objects, toman los datos y los
valores esperados del YAML (fixture ``datos``) y verifican con assertions web-first.
"""

import re

import allure
import pytest
from playwright.sync_api import BrowserContext, Page, Playwright, expect
from pytest_bdd import given, parsers, then, when

from pages import (
    CartPage,
    CheckoutCompletePage,
    CheckoutInformationPage,
    CheckoutOverviewPage,
    InventoryPage,
    LoginPage,
)
from pages.components import Header, Menu
from support.aserciones import etiquetas_de_importes, verificar_pagina
from support.datos import Datos
from support.dinero import calcular_totales
from support.estado_app import iniciar_sesion_por_cookie, precargar_carrito

# Telemetría de errores que la app envía a backtrace.io (error_user manda varias peticiones
# por flujo): se bloquea para no ensuciar métricas de terceros ni depender de su red.
TELEMETRIA = re.compile(r"^https?://([^/]+\.)?backtrace\.io/")


# --- Navegador -----------------------------------------------------------------------------


@pytest.fixture(scope="session", autouse=True)
def configurar_test_id(playwright: Playwright) -> None:
    """SauceDemo expone sus selectores estables en el atributo ``data-test``."""
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.hookimpl(trylast=True)
def pytest_bdd_before_scenario(request: pytest.FixtureRequest) -> None:
    """Añade el navegador como parámetro de Allure: separa los resultados de cada navegador en
    el reporte combinado de la CI (forma parte del historyId).

    trylast: allure-pytest-bdd crea el resultado del escenario en este mismo hook.
    """
    allure.dynamic.parameter("navegador", request.getfixturevalue("browser_name"))


@pytest.fixture
def context(context: BrowserContext) -> BrowserContext:
    """Contexto de pytest-playwright con la telemetría de terceros bloqueada."""
    context.route(TELEMETRIA, lambda route: route.abort())
    return context


# --- Page objects --------------------------------------------------------------------------


@pytest.fixture
def header(page: Page) -> Header:
    """Cabecera compartida (título y carrito) de la página autenticada en curso."""
    return Header(page)


@pytest.fixture
def menu(page: Page) -> Menu:
    """Menú lateral de la página autenticada en curso."""
    return Menu(page)


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture
def inventory_page(page: Page) -> InventoryPage:
    return InventoryPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    return CartPage(page)


@pytest.fixture
def checkout_information_page(page: Page) -> CheckoutInformationPage:
    return CheckoutInformationPage(page)


@pytest.fixture
def checkout_overview_page(page: Page) -> CheckoutOverviewPage:
    return CheckoutOverviewPage(page)


@pytest.fixture
def checkout_complete_page(page: Page) -> CheckoutCompletePage:
    return CheckoutCompletePage(page)


# --- Estado del escenario ------------------------------------------------------------------


@pytest.fixture
def carrito_esperado() -> list[str]:
    """Claves de catálogo que el escenario ha añadido al carrito, en orden."""
    return []


def _producto(datos: Datos, clave: str) -> dict:
    return datos(f"catalogo.productos.{clave}")


def _compra(datos: Datos, compra: str) -> list[str]:
    return datos(f"carrito.compras.{compra}")


# --- Sesión --------------------------------------------------------------------------------


@given("que estoy en la página de login")
def abrir_login(login_page: LoginPage) -> None:
    login_page.open()


@given(parsers.parse('que inicié sesión como "{usuario}"'))
def sesion_por_cookie(
    context: BrowserContext,
    base_url: str,
    datos: Datos,
    inventory_page: InventoryPage,
    usuario: str,
) -> None:
    """Precondición rápida: crea la cookie de sesión y abre el inventario sin pasar por la UI."""
    iniciar_sesion_por_cookie(
        context, base_url, datos("sesion.cookie"), datos(f"usuarios.usuarios.{usuario}")
    )
    inventory_page.open()
    verificar_pagina(inventory_page, datos("inventario.titulo"))


@when(parsers.parse('inicio sesión como "{usuario}"'))
def login_por_ui(login_page: LoginPage, datos: Datos, usuario: str) -> None:
    login_page.login(datos(f"usuarios.usuarios.{usuario}"), datos("usuarios.password"))


@then("sigo en la página de login")
def sigo_en_login(login_page: LoginPage) -> None:
    verificar_pagina(login_page)
    expect(login_page.login_button).to_be_visible()


@then("estoy en el inventario")
def en_inventario(inventory_page: InventoryPage, datos: Datos) -> None:
    verificar_pagina(inventory_page, datos("inventario.titulo"))


# --- Carrito -------------------------------------------------------------------------------


@given(parsers.parse('que tengo en el carrito la compra "{compra}"'))
def carrito_precargado(page: Page, datos: Datos, carrito_esperado: list[str], compra: str) -> None:
    claves = _compra(datos, compra)
    ids = [_producto(datos, clave)["id"] for clave in claves]
    precargar_carrito(page, datos("sesion.clave_carrito_local_storage"), ids)
    carrito_esperado.extend(claves)


@when(parsers.parse('añado al carrito los productos de la compra "{compra}"'))
def anadir_compra(
    inventory_page: InventoryPage, datos: Datos, carrito_esperado: list[str], compra: str
) -> None:
    for clave in _compra(datos, compra):
        inventory_page.add_to_cart(_producto(datos, clave)["nombre"])
        carrito_esperado.append(clave)


@when(parsers.parse('quito del carrito el producto "{producto}"'))
def quitar_producto(
    inventory_page: InventoryPage, datos: Datos, carrito_esperado: list[str], producto: str
) -> None:
    inventory_page.remove_from_cart(_producto(datos, producto)["nombre"])
    carrito_esperado.remove(producto)


@then("el contador del carrito coincide con los productos del carrito")
def contador_carrito(header: Header, carrito_esperado: list[str]) -> None:
    if carrito_esperado:
        expect(header.cart_badge).to_have_text(str(len(carrito_esperado)))
    else:
        expect(header.cart_badge).to_be_hidden()


@then("el contador del carrito desaparece")
def contador_carrito_oculto(header: Header) -> None:
    expect(header.cart_badge).to_be_hidden()


@when("voy al carrito")
def ir_al_carrito(header: Header, cart_page: CartPage, datos: Datos) -> None:
    header.open_cart()
    verificar_pagina(cart_page, datos("carrito.titulo"))


@then(parsers.parse('el carrito lista los productos de la compra "{compra}"'))
def carrito_lista_compra(cart_page: CartPage, datos: Datos, compra: str) -> None:
    productos = [_producto(datos, clave) for clave in _compra(datos, compra)]
    moneda = datos("catalogo.moneda")
    expect(cart_page.item_names).to_have_text([p["nombre"] for p in productos])
    expect(cart_page.item_prices).to_have_text([f"{moneda}{p['precio']}" for p in productos])


# --- Checkout ------------------------------------------------------------------------------


@when("inicio el checkout")
def iniciar_checkout(
    cart_page: CartPage, checkout_information_page: CheckoutInformationPage, datos: Datos
) -> None:
    cart_page.checkout()
    verificar_pagina(checkout_information_page, datos("checkout.informacion.titulo"))


@given("que estoy en el paso de información del checkout")
def en_informacion_checkout(
    checkout_information_page: CheckoutInformationPage, datos: Datos
) -> None:
    checkout_information_page.open()
    verificar_pagina(checkout_information_page, datos("checkout.informacion.titulo"))


@when("completo mis datos con el cliente válido")
def completar_cliente_valido(
    checkout_information_page: CheckoutInformationPage, datos: Datos
) -> None:
    cliente = datos("checkout.cliente_valido")
    checkout_information_page.fill_information(
        cliente["nombre"], cliente["apellido"], cliente["codigo_postal"]
    )


@when("continúo con el checkout")
def continuar_checkout(checkout_information_page: CheckoutInformationPage) -> None:
    checkout_information_page.continue_checkout()


@then(parsers.parse('el resumen muestra los importes calculados de la compra "{compra}"'))
def resumen_importes(
    checkout_overview_page: CheckoutOverviewPage, datos: Datos, compra: str
) -> None:
    verificar_pagina(checkout_overview_page, datos("checkout.resumen.titulo"))
    precios = [_producto(datos, clave)["precio"] for clave in _compra(datos, compra)]
    totales = calcular_totales(precios, datos("checkout.resumen.tasa_impuesto"))
    esperado = etiquetas_de_importes(
        totales, datos("checkout.resumen.etiquetas"), datos("catalogo.moneda")
    )
    expect(checkout_overview_page.subtotal).to_have_text(esperado["subtotal"])
    expect(checkout_overview_page.tax).to_have_text(esperado["impuesto"])
    expect(checkout_overview_page.total).to_have_text(esperado["total"])


@when("finalizo la compra")
def finalizar_compra(checkout_overview_page: CheckoutOverviewPage) -> None:
    checkout_overview_page.finish()


@then("veo la confirmación del pedido")
def confirmacion(checkout_complete_page: CheckoutCompletePage, datos: Datos) -> None:
    verificar_pagina(checkout_complete_page, datos("checkout.confirmacion.titulo"))
    expect(checkout_complete_page.complete_header).to_have_text(
        datos("checkout.confirmacion.cabecera")
    )
