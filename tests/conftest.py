"""Fixtures compartidos de la suite de UI.

Los fixtures ``browser``, ``context`` y ``page`` vienen de pytest-playwright, de modo
que el navegador, el modo headed y los artefactos (video, captura, trace) se controlan
por CLI o desde pytest.ini. El ambiente y la URL base salen de ``config/settings.py``.
"""

import json
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Playwright

from config import Settings, load_settings

RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
CLAVE_SETTINGS = pytest.StashKey[Settings]()


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--env",
        action="store",
        default=None,
        help="Ambiente objetivo (sobrescribe TEST_ENV). Ver AMBIENTES en config/settings.py.",
    )


def pytest_configure(config: pytest.Config) -> None:
    """Resuelve la configuración una sola vez; un ambiente inválido aborta con mensaje claro."""
    try:
        config.stash[CLAVE_SETTINGS] = load_settings(config.getoption("--env"))
    except ValueError as error:
        raise pytest.UsageError(str(error)) from error


def pytest_report_header(config: pytest.Config) -> str:
    settings = config.stash[CLAVE_SETTINGS]
    base_url = config.getoption("base_url") or settings.base_url
    return f"ambiente: {settings.env} | url base: {base_url}"


@pytest.fixture(scope="session")
def settings(pytestconfig: pytest.Config) -> Settings:
    """Configuración del ambiente activo (URL base y credenciales)."""
    return pytestconfig.stash[CLAVE_SETTINGS]


@pytest.fixture(scope="session")
def base_url(pytestconfig: pytest.Config, settings: Settings) -> str:
    """Sobrescribe el fixture de pytest-base-url que usan page.goto() y los page objects.

    Precedencia: --base-url / PYTEST_BASE_URL (CLI) > BASE_URL (entorno o .env) > ambiente.
    """
    return pytestconfig.getoption("base_url") or settings.base_url


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
