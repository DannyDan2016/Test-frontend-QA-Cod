"""Datos de prueba y valores esperados por ambiente.

Cada conjunto de datos es un YAML con el mismo nombre en dos niveles:

* ``data/comun/<nombre>.yaml``: valores compartidos por todos los ambientes.
* ``data/<env>/<nombre>.yaml``: overrides opcionales del ambiente activo.

Ambos se fusionan en profundidad (los diccionarios se mezclan clave a clave y, ante
conflicto, gana el ambiente; listas y escalares se sustituyen enteros). Los strings
admiten ``${VAR}`` y ``${VAR:-defecto}`` para leer variables de entorno (por ejemplo,
contraseñas que viven en ``.env`` o en los secrets de la CI).

Uso::

    datos = Datos("prod")
    datos("checkout.cliente_valido.nombre")   # primer segmento = archivo YAML
"""

from __future__ import annotations

import copy
import os
import re
from pathlib import Path
from typing import Any

import yaml

from config.settings import RAIZ_PROYECTO

DIR_DATOS = RAIZ_PROYECTO / "data"
COMUN = "comun"

_VARIABLE = re.compile(r"\$\{(?P<nombre>[A-Z0-9_]+)(?::-(?P<defecto>[^}]*))?\}")


class DatosNoEncontradosError(LookupError):
    """El archivo, la clave o la variable de entorno pedida no existe."""


def fusionar(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Fusión profunda: devuelve un dict nuevo donde ``override`` gana a ``base``."""
    resultado = copy.deepcopy(base)
    for clave, valor in override.items():
        if isinstance(valor, dict) and isinstance(resultado.get(clave), dict):
            resultado[clave] = fusionar(resultado[clave], valor)
        else:
            resultado[clave] = copy.deepcopy(valor)
    return resultado


def expandir(valor: Any, origen: str = "") -> Any:
    """Resuelve ``${VAR}`` y ``${VAR:-defecto}`` de forma recursiva."""
    if isinstance(valor, str):

        def sustituir(coincidencia: re.Match[str]) -> str:
            nombre, defecto = coincidencia["nombre"], coincidencia["defecto"]
            resultado = os.getenv(nombre) or defecto
            if resultado is None:
                raise DatosNoEncontradosError(
                    f"La variable de entorno '{nombre}' no tiene valor ni defecto ({origen})"
                )
            return resultado

        return _VARIABLE.sub(sustituir, valor)
    if isinstance(valor, dict):
        return {clave: expandir(v, origen) for clave, v in valor.items()}
    if isinstance(valor, list):
        return [expandir(v, origen) for v in valor]
    return valor


def _leer_yaml(ruta: Path) -> dict[str, Any]:
    with ruta.open(encoding="utf-8") as archivo:
        contenido = yaml.safe_load(archivo)
    if contenido is None:
        return {}
    if not isinstance(contenido, dict):
        raise DatosNoEncontradosError(f"{ruta} debe contener un mapa clave: valor en la raíz")
    return contenido


class Datos:
    """Acceso de solo lectura a los YAML del ambiente activo."""

    def __init__(self, env: str, directorio: Path = DIR_DATOS) -> None:
        self.env = env
        self.directorio = directorio
        self._cache: dict[str, dict[str, Any]] = {}

    def _rutas(self, nombre: str) -> tuple[Path, Path]:
        return (
            self.directorio / COMUN / f"{nombre}.yaml",
            self.directorio / self.env / f"{nombre}.yaml",
        )

    def _describir(self, nombre: str) -> str:
        comun, ambiente = self._rutas(nombre)
        partes = [p.relative_to(self.directorio.parent).as_posix() for p in (comun, ambiente)]
        return " + ".join(partes)

    def archivo(self, nombre: str) -> dict[str, Any]:
        """Contenido fusionado (comun + ambiente) y expandido de ``<nombre>.yaml``."""
        if nombre not in self._cache:
            comun, ambiente = self._rutas(nombre)
            if not comun.is_file() and not ambiente.is_file():
                raise DatosNoEncontradosError(
                    f"No existe el archivo de datos '{nombre}.yaml' "
                    f"(buscado en {self._describir(nombre)}, TEST_ENV={self.env})"
                )
            base = _leer_yaml(comun) if comun.is_file() else {}
            override = _leer_yaml(ambiente) if ambiente.is_file() else {}
            self._cache[nombre] = expandir(fusionar(base, override), self._describir(nombre))
        return self._cache[nombre]

    def __call__(self, clave: str) -> Any:
        """Devuelve una copia del valor en ``archivo.clave.subclave``.

        Raises:
            DatosNoEncontradosError: con el archivo y la clave que faltan, y las claves disponibles.
        """
        nombre, *camino = clave.split(".")
        nodo: Any = self.archivo(nombre)
        recorrido: list[str] = []
        for parte in camino:
            if not isinstance(nodo, dict) or parte not in nodo:
                disponibles = ", ".join(sorted(nodo)) if isinstance(nodo, dict) else "(no es mapa)"
                padre = ".".join(recorrido) or "(raíz)"
                raise DatosNoEncontradosError(
                    f"Clave inexistente '{clave}' en {self._describir(nombre)}: "
                    f"falta '{parte}' dentro de '{padre}'. Claves disponibles: {disponibles}"
                )
            nodo = nodo[parte]
            recorrido.append(parte)
        # Copia defensiva: ningún test puede alterar la caché compartida
        return copy.deepcopy(nodo)
