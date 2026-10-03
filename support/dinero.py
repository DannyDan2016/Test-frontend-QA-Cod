"""Cálculo de importes del checkout con Decimal (sin errores de coma flotante)."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

CENTIMOS = Decimal("0.01")


@dataclass(frozen=True)
class Totales:
    """Importes del resumen del checkout."""

    subtotal: Decimal
    impuesto: Decimal
    total: Decimal


def redondear(importe: Decimal) -> Decimal:
    """Redondea a céntimos, mitad hacia arriba (como ``toFixed(2)`` en la web)."""
    return importe.quantize(CENTIMOS, rounding=ROUND_HALF_UP)


def calcular_totales(precios: Iterable[str | Decimal], tasa_impuesto: str | Decimal) -> Totales:
    """Subtotal, impuesto (subtotal * tasa, redondeado) y total de una compra."""
    subtotal = sum((Decimal(precio) for precio in precios), start=Decimal("0"))
    impuesto = redondear(subtotal * Decimal(tasa_impuesto))
    return Totales(subtotal=subtotal, impuesto=impuesto, total=subtotal + impuesto)


def formatear(importe: Decimal, moneda: str) -> str:
    """Formatea un importe con dos decimales y su moneda: ``$25.98``."""
    return f"{moneda}{redondear(importe):.2f}"
