"""Steps del Dynamic Catalog: carga con spinner.

El spinner dura un tiempo aleatorio (0,5-3 s). En vez de esperar y confiar en llegar a tiempo,
se pausa el reloj del navegador (``page.clock``) y se avanza de forma explícita: el escenario
es determinista y no contiene pausas reales.
"""

import time

import pytest
from playwright.sync_api import Page, expect
from pytest_bdd import given, scenarios, then, when

from pages.dynamic_catalog import SpinnerPage
from support.aserciones import verificar_pagina
from support.datos import Datos

scenarios("catalogo_dinamico")

# Segundos que se adelanta el reloj al pausarlo (detalle técnico, no dato de negocio)
MARGEN_PAUSA_S = 60


@pytest.fixture
def spinner_page(page: Page) -> SpinnerPage:
    return SpinnerPage(page)


@given("que el reloj del navegador está en pausa")
def reloj_en_pausa(page: Page) -> None:
    # El reloj instalado avanza mientras tanto: pausar en "ahora" puede quedar en el pasado
    # si la máquina va cargada (Cannot fast-forward to the past), así que se pausa con margen.
    inicio = time.time()
    page.clock.install(time=inicio)
    page.clock.pause_at(inicio + MARGEN_PAUSA_S)


@when("abro el catálogo dinámico con indicador de carga")
def abrir_spinner(spinner_page: SpinnerPage, datos: Datos) -> None:
    spinner_page.open()
    verificar_pagina(spinner_page, datos("catalogo_dinamico.spinner.titulo"))


@then("veo el indicador de carga")
def indicador_visible(spinner_page: SpinnerPage) -> None:
    expect(spinner_page.spinner).to_be_visible()


@when("transcurre el tiempo máximo de carga")
def avanzar_reloj(page: Page, datos: Datos) -> None:
    page.clock.run_for(datos("catalogo_dinamico.spinner.duracion_maxima_carga_ms"))


@then("el indicador de carga desaparece")
def indicador_oculto(spinner_page: SpinnerPage) -> None:
    expect(spinner_page.spinner).to_be_hidden()
    expect(spinner_page.grid).to_be_visible()


@then("la rejilla muestra todos los productos del catálogo")
def rejilla_con_catalogo(spinner_page: SpinnerPage, datos: Datos) -> None:
    # La rejilla presenta los productos por id, no alfabéticamente
    productos = sorted(datos("catalogo.productos").values(), key=lambda p: p["id"])
    moneda = datos("catalogo.moneda")
    expect(spinner_page.item_names).to_have_text([p["nombre"] for p in productos])
    expect(spinner_page.item_prices).to_have_text([f"{moneda}{p['precio']}" for p in productos])
