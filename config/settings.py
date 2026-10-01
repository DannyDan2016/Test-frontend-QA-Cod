"""Configuración de la suite por ambiente.

Orden de precedencia de cada valor (de mayor a menor):

1. Variables de entorno del proceso (por ejemplo, las que inyecta la CI).
2. Archivo ``.env`` en la raíz del repo (local e ignorado por git).
3. Valores por defecto del ambiente definidos en ``AMBIENTES``.

La URL base además se puede forzar por CLI con ``--base-url`` (ver ``tests/conftest.py``).
"""

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

RAIZ_PROYECTO = Path(__file__).resolve().parents[1]

AMBIENTE_POR_DEFECTO = "prod"

# Ambientes disponibles; se eligen con TEST_ENV o --env. Cada uno puede sobrescribir datos
# en data/<env>/*.yaml (ver support/datos.py). SauceDemo solo publica producción, así que
# "staging" es un ambiente de EJEMPLO que apunta a la misma URL y demuestra los overrides.
AMBIENTES: dict[str, dict[str, str]] = {
    "prod": {"base_url": "https://www.saucedemo.com"},
    "staging": {"base_url": "https://www.saucedemo.com"},
}

# Credenciales públicas de SauceDemo: la propia pantalla de login las muestra, no son secretos.
USUARIO_POR_DEFECTO = "standard_user"
PASSWORD_POR_DEFECTO = "secret_sauce"


@dataclass(frozen=True)
class Settings:
    """Valores de configuración resueltos para una ejecución."""

    env: str
    base_url: str
    user: str
    password: str = field(repr=False)


def _leer(variable: str, por_defecto: str) -> str:
    """Devuelve la variable de entorno o el valor por defecto si no existe o está vacía."""
    return os.getenv(variable, "").strip() or por_defecto


def load_settings(env: str | None = None) -> Settings:
    """Carga la configuración del ambiente ``env`` (o de ``TEST_ENV`` si no se indica).

    Raises:
        ValueError: si el ambiente solicitado no está definido en ``AMBIENTES``.
    """
    # override=False: las variables ya definidas en el entorno (CI) tienen prioridad sobre .env
    load_dotenv(RAIZ_PROYECTO / ".env", override=False)

    nombre = (env or _leer("TEST_ENV", AMBIENTE_POR_DEFECTO)).strip().lower()
    if nombre not in AMBIENTES:
        disponibles = ", ".join(sorted(AMBIENTES))
        raise ValueError(f"Ambiente desconocido: '{nombre}'. Ambientes disponibles: {disponibles}")

    return Settings(
        env=nombre,
        base_url=_leer("BASE_URL", AMBIENTES[nombre]["base_url"]).rstrip("/"),
        user=_leer("SAUCE_USER", USUARIO_POR_DEFECTO),
        password=_leer("SAUCE_PASSWORD", PASSWORD_POR_DEFECTO),
    )
