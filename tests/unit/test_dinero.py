"""Tests unitarios del cálculo de importes del checkout."""

from decimal import Decimal

import pytest

from support.dinero import calcular_totales, formatear


@pytest.mark.parametrize(
    ("precios", "esperado"),
    [
        (["29.99"], ("$29.99", "$2.40", "$32.39")),
        (["15.99", "9.99"], ("$25.98", "$2.08", "$28.06")),
        (["29.99", "9.99"], ("$39.98", "$3.20", "$43.18")),
        ([], ("$0.00", "$0.00", "$0.00")),
    ],
    ids=["un-producto", "dos-productos", "redondeo-a-la-baja", "carrito-vacio"],
)
def test_calcula_totales_con_impuesto_del_8(
    precios: list[str], esperado: tuple[str, str, str]
) -> None:
    totales = calcular_totales(precios, "0.08")
    obtenido = tuple(formatear(i, "$") for i in (totales.subtotal, totales.impuesto, totales.total))
    assert obtenido == esperado


def test_redondea_mitad_hacia_arriba() -> None:
    assert calcular_totales(["0.0625"], "0.08").impuesto == Decimal("0.01")
