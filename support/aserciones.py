"""Aserciones reutilizables (web-first) sobre page objects y datos calculados."""

from playwright.sync_api import expect

from pages.authenticated_page import AuthenticatedPage
from pages.base_page import BasePage
from support.dinero import Totales, formatear


def verificar_pagina(pagina: BasePage, titulo: str | None = None) -> None:
    """La URL es la de la página y, si se indica, la cabecera muestra su título."""
    expect(pagina.page).to_have_url(pagina.url_pattern)
    if titulo is not None:
        assert isinstance(pagina, AuthenticatedPage), "solo las páginas con sesión tienen título"
        expect(pagina.header.title).to_have_text(titulo)


def etiquetas_de_importes(
    totales: Totales, plantillas: dict[str, str], moneda: str
) -> dict[str, str]:
    """Textos esperados de subtotal, impuesto y total a partir de las plantillas del YAML."""
    importes = {
        "subtotal": totales.subtotal,
        "impuesto": totales.impuesto,
        "total": totales.total,
    }
    return {
        clave: plantillas[clave].format(importe=formatear(importe, moneda))
        for clave, importe in importes.items()
    }
