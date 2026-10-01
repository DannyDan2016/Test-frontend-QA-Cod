"""Configuración global de la suite (sin navegador).

* Opción ``--env`` y fixtures ``settings``, ``base_url`` y ``datos`` (YAML del ambiente).
* Traducción de tags de Gherkin a marcas de pytest (``@tc-*`` y ``@known-bug``).
* Adjunto de captura a Allure cuando un escenario falla.

Los fixtures de navegador y los steps compartidos viven en ``tests/step_defs/conftest.py``,
de modo que los tests unitarios (``tests/unit``) no arrancan Playwright.
"""

from collections.abc import Callable

import allure
import pytest

from config import Settings, load_settings
from support.datos import Datos, DatosNoEncontradosError

CLAVE_SETTINGS = pytest.StashKey[Settings]()
CLAVE_DATOS = pytest.StashKey[Datos]()

MOTIVO_RENDIMIENTO_EN_PARALELO = (
    "medición de rendimiento: en paralelo mediría la contención de CPU entre navegadores; "
    "se ejecuta en serie con: pytest -m performance"
)


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
        settings = load_settings(config.getoption("--env"))
    except ValueError as error:
        raise pytest.UsageError(str(error)) from error
    config.stash[CLAVE_SETTINGS] = settings
    config.stash[CLAVE_DATOS] = Datos(settings.env)


def pytest_report_header(config: pytest.Config) -> str:
    settings = config.stash[CLAVE_SETTINGS]
    base_url = config.getoption("base_url") or settings.base_url
    return f"ambiente: {settings.env} | url base: {base_url}"


@pytest.fixture(scope="session")
def settings(pytestconfig: pytest.Config) -> Settings:
    """Configuración del ambiente activo."""
    return pytestconfig.stash[CLAVE_SETTINGS]


@pytest.fixture(scope="session")
def datos(pytestconfig: pytest.Config) -> Datos:
    """Datos de prueba y valores esperados: ``datos("checkout.cliente_valido")``."""
    return pytestconfig.stash[CLAVE_DATOS]


@pytest.fixture(scope="session")
def base_url(pytestconfig: pytest.Config, settings: Settings) -> str:
    """Sobrescribe el fixture de pytest-base-url que usan page.goto() y los page objects.

    Precedencia: --base-url / PYTEST_BASE_URL (CLI) > BASE_URL (entorno o .env) > ambiente.
    """
    return pytestconfig.getoption("base_url") or settings.base_url


# --- Tags de Gherkin -----------------------------------------------------------------------


def pytest_bdd_apply_tag(tag: str, function: Callable[..., object]) -> bool | None:
    """Traduce las tags con guion, que no son nombres de marca válidos.

    * ``@tc-auth-001`` -> ``pytest.mark.tc("TC-AUTH-001")`` (trazabilidad).
    * ``@known-bug``   -> ``pytest.mark.known_bug`` (el xfail se añade al recolectar).

    El resto (smoke, regression, negative) sigue el comportamiento estándar de pytest-bdd;
    con ``--strict-markers`` una tag no declarada en pytest.ini aborta la recolección.
    """
    if tag.startswith("tc-"):
        pytest.mark.tc(tag.upper())(function)
        return True
    if tag == "known-bug":
        pytest.mark.known_bug(function)
        return True
    return None


# tryfirst: los IDs deben estar disponibles antes de que pytest aplique el filtro -k
@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """Hace filtrable el ID de caso y convierte ``@known-bug`` en xfail estricto.

    * ``pytest -k TC-AUTH-001`` selecciona los escenarios con esa tag.
    * El motivo del xfail sale de ``bugs.yaml`` (clave = ID del caso).
    * ``@performance`` se omite en ejecuciones con pytest-xdist (ver motivo).
    """
    datos = config.stash[CLAVE_DATOS]
    en_paralelo = hasattr(config, "workerinput")  # proceso worker de pytest-xdist
    for item in items:
        ids = [marca.args[0] for marca in item.iter_markers("tc")]
        item.extra_keyword_matches.update(ids)
        if en_paralelo and item.get_closest_marker("performance"):
            item.add_marker(pytest.mark.skip(reason=MOTIVO_RENDIMIENTO_EN_PARALELO))
        if item.get_closest_marker("known_bug") is None:
            continue
        try:
            motivos = [datos(f"bugs.bugs.{id_caso}") for id_caso in ids]
        except DatosNoEncontradosError as error:
            raise pytest.UsageError(f"{item.nodeid}: @known-bug sin motivo. {error}") from error
        if not motivos:
            raise pytest.UsageError(f"{item.nodeid}: @known-bug necesita una tag @tc-*")
        item.add_marker(pytest.mark.xfail(strict=True, reason=" | ".join(motivos)))


# --- Evidencias ----------------------------------------------------------------------------


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
