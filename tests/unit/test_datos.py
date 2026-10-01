"""Tests unitarios del cargador de datos YAML (sin navegador)."""

from pathlib import Path

import pytest

from support.datos import Datos, DatosNoEncontradosError, fusionar


def _escribir(raiz: Path, nivel: str, nombre: str, contenido: str) -> None:
    carpeta = raiz / nivel
    carpeta.mkdir(parents=True, exist_ok=True)
    (carpeta / f"{nombre}.yaml").write_text(contenido, encoding="utf-8")


@pytest.fixture
def raiz(tmp_path: Path) -> Path:
    directorio = tmp_path / "data"
    _escribir(
        directorio,
        "comun",
        "checkout",
        "cliente:\n  nombre: John\n  apellido: Doe\ntasa: '0.08'\nproductos: [a, b]\n",
    )
    _escribir(directorio, "staging", "checkout", "cliente:\n  nombre: Ana\nproductos: [c]\n")
    return directorio


def test_lee_valores_comunes(raiz: Path) -> None:
    datos = Datos("prod", raiz)
    assert datos("checkout.cliente") == {"nombre": "John", "apellido": "Doe"}


def test_el_ambiente_sobrescribe_en_profundidad(raiz: Path) -> None:
    datos = Datos("staging", raiz)
    assert datos("checkout.cliente") == {"nombre": "Ana", "apellido": "Doe"}
    assert datos("checkout.productos") == ["c"], "las listas se sustituyen, no se concatenan"
    assert datos("checkout.tasa") == "0.08"


def test_archivo_inexistente_indica_rutas_y_ambiente(raiz: Path) -> None:
    with pytest.raises(DatosNoEncontradosError, match=r"usuarios\.yaml.*TEST_ENV=prod"):
        Datos("prod", raiz)("usuarios.estandar")


def test_clave_inexistente_indica_archivo_clave_y_alternativas(raiz: Path) -> None:
    with pytest.raises(DatosNoEncontradosError) as error:
        Datos("prod", raiz)("checkout.cliente.email")
    mensaje = str(error.value)
    assert "data/comun/checkout.yaml" in mensaje
    assert "'email' dentro de 'cliente'" in mensaje
    assert "apellido, nombre" in mensaje


def test_resuelve_variables_de_entorno(raiz: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _escribir(raiz, "comun", "usuarios", "password: ${CLAVE_PRUEBA}\n")
    monkeypatch.setenv("CLAVE_PRUEBA", "desde-entorno")
    assert Datos("prod", raiz)("usuarios.password") == "desde-entorno"


def test_usa_el_defecto_si_la_variable_no_existe(
    raiz: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _escribir(raiz, "comun", "usuarios", "password: ${CLAVE_PRUEBA:-por_defecto}\n")
    monkeypatch.delenv("CLAVE_PRUEBA", raising=False)
    assert Datos("prod", raiz)("usuarios.password") == "por_defecto"


def test_variable_sin_valor_ni_defecto_falla(raiz: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _escribir(raiz, "comun", "usuarios", "password: ${CLAVE_PRUEBA}\n")
    monkeypatch.delenv("CLAVE_PRUEBA", raising=False)
    with pytest.raises(DatosNoEncontradosError, match="CLAVE_PRUEBA"):
        Datos("prod", raiz)("usuarios.password")


def test_devuelve_copias_defensivas(raiz: Path) -> None:
    datos = Datos("prod", raiz)
    datos("checkout.cliente")["nombre"] = "mutado"
    assert datos("checkout.cliente.nombre") == "John"


def test_fusionar_no_modifica_las_entradas() -> None:
    base = {"a": {"b": 1}}
    fusionar(base, {"a": {"c": 2}})
    assert base == {"a": {"b": 1}}
