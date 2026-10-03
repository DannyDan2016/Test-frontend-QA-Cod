import re

from playwright.sync_api import Page, expect

from config import Settings
from pages import (
    CartPage,
    CheckoutInformationPage,
    CheckoutSummaryPage,
    ConfirmationPage,
    InventoryPage,
    LoginPage,
)

# Datos ficticios del formulario de envío (no dependen del ambiente)
DATOS_CHECKOUT = {"first_name": "John", "last_name": "Doe", "postal_code": "12345"}


def test_end_to_end_shopping(page: Page, settings: Settings) -> None:
    product1 = "Test.allTheThings() T-Shirt (Red)"
    product2 = "Sauce Labs Bike Light"

    # Paso 1: inicio de sesión
    LoginPage(page).open().login(settings.user, settings.password)
    expect(page).to_have_url(re.compile(r"/inventory\.html$"))

    # Paso 2: agregar productos al carrito
    inventory_page = InventoryPage(page)
    inventory_page.add_to_cart(product1)
    inventory_page.add_to_cart(product2)
    expect(inventory_page.cart_badge).to_have_text("2")

    # Paso 3: verificar el carrito
    inventory_page.open_cart()
    expect(page).to_have_url(re.compile(r"/cart\.html$"))
    cart_page = CartPage(page)
    expect(cart_page.item_names).to_have_text([product1, product2])
    expect(cart_page.item_prices).to_have_text(["$15.99", "$9.99"])

    # Paso 4: datos del checkout
    cart_page.checkout()
    expect(page).to_have_url(re.compile(r"/checkout-step-one\.html$"))
    CheckoutInformationPage(page).fill_information(**DATOS_CHECKOUT)
    expect(page).to_have_url(re.compile(r"/checkout-step-two\.html$"))

    # Paso 5: verificar el resumen (impuesto del 8 %)
    summary_page = CheckoutSummaryPage(page)
    expect(summary_page.subtotal).to_have_text("Item total: $25.98")
    expect(summary_page.tax).to_have_text("Tax: $2.08")
    expect(summary_page.total).to_have_text("Total: $28.06")

    # Paso 6: completar la compra
    summary_page.complete_purchase()
    expect(page).to_have_url(re.compile(r"/checkout-complete\.html$"))

    # Paso 7: verificar el mensaje de confirmación
    expect(ConfirmationPage(page).complete_header).to_have_text("Thank you for your order!")
