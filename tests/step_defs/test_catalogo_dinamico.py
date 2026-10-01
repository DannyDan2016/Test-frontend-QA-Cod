"""Steps del Dynamic Catalog: carga con spinner (tiempo aleatorio, solo esperas web-first)."""

import pytest
from playwright.sync_api import Page, expect
from pytest_bdd import scenarios, then, when

from pages.dynamic_catalog import SpinnerPage
from support.aserciones import verificar_pagina
from support.datos import Datos

scenarios("catalogo_dinamico")


@pytest.fixture
def spinner_page(page: Page) -> SpinnerPage:
    return SpinnerPage(page)


@when("abro el catálogo dinámico con indicador de carga")
def abrir_spinner(spinner_page: SpinnerPage, datos: Datos) -> None:
    spinner_page.open()
    verificar_pagina(spinner_page, datos("catalogo_dinamico.spinner.titulo"))


@then("veo el indicador de carga")
def indicador_visible(spinner_page: SpinnerPage) -> None:
    expect(spinner_page.spinner).to_be_visible()


@then("el indicador desaparece al terminar la carga")
def indicador_oculto(spinner_page: SpinnerPage, datos: Datos) -> None:
    espera = datos("catalogo_dinamico.spinner.espera_maxima_carga_ms")
    expect(spinner_page.spinner).to_be_hidden(timeout=espera)
    expect(spinner_page.grid).to_be_visible()


@then("la rejilla muestra todos los productos del catálogo")
def rejilla_con_catalogo(spinner_page: SpinnerPage, datos: Datos) -> None:
    # La rejilla presenta los productos por id, no alfabéticamente
    productos = sorted(datos("catalogo.productos").values(), key=lambda p: p["id"])
    moneda = datos("catalogo.moneda")
    expect(spinner_page.item_names).to_have_text([p["nombre"] for p in productos])
    expect(spinner_page.item_prices).to_have_text([f"{moneda}{p['precio']}" for p in productos])
