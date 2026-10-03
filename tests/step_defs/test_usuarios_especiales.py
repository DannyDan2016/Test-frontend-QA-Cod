"""Steps de los usuarios especiales de SauceDemo (rendimiento y bugs conocidos)."""

import time

import allure
import pytest
from playwright.sync_api import expect
from pytest_bdd import parsers, scenarios, then, when

from pages import CheckoutInformationPage, InventoryPage, LoginPage
from support.datos import Datos

scenarios("usuarios_especiales")


@pytest.fixture
def mediciones() -> dict[str, float]:
    """Tiempos medidos durante el escenario, en milisegundos."""
    return {}


@when(parsers.parse('inicio sesión como "{usuario}" cronometrando la carga del inventario'))
def login_cronometrado(
    login_page: LoginPage,
    inventory_page: InventoryPage,
    datos: Datos,
    mediciones: dict[str, float],
    usuario: str,
) -> None:
    espera = datos("rendimiento.login_inventario.espera_maxima_ms")
    inicio = time.perf_counter()
    login_page.login(datos(f"usuarios.usuarios.{usuario}"), datos("usuarios.password"))
    # Espera web-first (sin pausas fijas) hasta que el inventario es visible
    expect(inventory_page.header.title).to_have_text(datos("inventario.titulo"), timeout=espera)
    mediciones["login_inventario"] = (time.perf_counter() - inicio) * 1000


@then("el inventario carga dentro del umbral de rendimiento")
def dentro_del_umbral(datos: Datos, mediciones: dict[str, float]) -> None:
    umbral = datos("rendimiento.login_inventario.umbral_ms")
    medido = mediciones["login_inventario"]
    allure.attach(
        f"login -> inventario: {medido:.0f} ms (umbral {umbral} ms)",
        name="tiempo-medido",
        attachment_type=allure.attachment_type.TEXT,
    )
    assert medido <= umbral, f"login -> inventario tardó {medido:.0f} ms (umbral {umbral} ms)"


@then("el formulario conserva los datos del cliente válido")
def formulario_conserva_datos(
    checkout_information_page: CheckoutInformationPage, datos: Datos
) -> None:
    cliente = datos("checkout.cliente_valido")
    expect(checkout_information_page.first_name).to_have_value(cliente["nombre"])
    expect(checkout_information_page.last_name).to_have_value(cliente["apellido"])
    expect(checkout_information_page.postal_code).to_have_value(cliente["codigo_postal"])
