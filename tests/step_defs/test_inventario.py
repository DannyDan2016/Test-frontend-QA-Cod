"""Steps del inventario: ordenación del listado."""

from decimal import Decimal

from playwright.sync_api import expect
from pytest_bdd import parsers, scenarios, then, when

from pages import InventoryPage
from support.datos import Datos

scenarios("inventario")


@when(parsers.parse('ordeno el inventario por "{orden}"'))
def ordenar(inventory_page: InventoryPage, datos: Datos, orden: str) -> None:
    inventory_page.sort_by(datos(f"inventario.ordenacion.{orden}.valor"))


@then(parsers.parse('el selector muestra la opción del orden "{orden}"'))
def opcion_activa(inventory_page: InventoryPage, datos: Datos, orden: str) -> None:
    expect(inventory_page.active_sort_option).to_have_text(
        datos(f"inventario.ordenacion.{orden}.etiqueta")
    )


@then(parsers.parse('los productos aparecen ordenados según "{orden}"'))
def productos_ordenados(inventory_page: InventoryPage, datos: Datos, orden: str) -> None:
    criterio = datos(f"inventario.ordenacion.{orden}")
    # catalogo.yaml está en orden A-Z: sorted() es estable también con reverse=True,
    # así que los empates de precio conservan ese orden, igual que la web.
    productos = list(datos("catalogo.productos").values())

    def clave(producto: dict) -> Decimal | str:
        return Decimal(producto["precio"]) if criterio["campo"] == "precio" else producto["nombre"]

    esperados = sorted(productos, key=clave, reverse=criterio["descendente"])
    moneda = datos("catalogo.moneda")
    expect(inventory_page.item_names).to_have_text([p["nombre"] for p in esperados])
    expect(inventory_page.item_prices).to_have_text([f"{moneda}{p['precio']}" for p in esperados])
