"""Fixtures compartidos de la suite de UI.

Los fixtures ``browser``, ``context`` y ``page`` vienen de pytest-playwright, de modo
que el navegador, el modo headed, la base_url y los artefactos (video, captura,
trace) se controlan por CLI o desde pytest.ini.
"""

import json
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Playwright

RAIZ_PROYECTO = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session", autouse=True)
def configurar_test_id(playwright: Playwright) -> None:
    """SauceDemo expone sus selectores estables en el atributo ``data-test``."""
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture(scope="session")
def config() -> dict:
    """Carga los datos de prueba desde config.json (ruta relativa a la raíz del repo)."""
    with (RAIZ_PROYECTO / "config.json").open(encoding="utf-8") as archivo:
        return json.load(archivo)


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    """Adjunta una captura de pantalla a Allure solo cuando el test falla."""
    reporte = yield
    if reporte.when == "call" and reporte.failed:
        page = getattr(item, "funcargs", {}).get("page")
        if page is not None and not page.is_closed():
            allure.attach(
                page.screenshot(full_page=True),
                name="captura-del-fallo",
                attachment_type=allure.attachment_type.PNG,
            )
    return reporte
