import pytest
import sys
import os
from playwright.async_api import Page

# Agregar la raíz del proyecto al PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pages import (
    LoginPage, InventoryPage, CartPage,
    CheckoutInformationPage, CheckoutSummaryPage, ConfirmationPage
)

@pytest.mark.asyncio
async def test_end_to_end_shopping(page: Page, config):  
    # Cargar datos desde config.json
    username = config["credentials"]["username"]
    password = config["credentials"]["password"]
    first_name = config["checkout_info"]["first_name"]
    last_name = config["checkout_info"]["last_name"]
    postal_code = config["checkout_info"]["postal_code"]

    # **Paso 1: Inicio de sesión**
    login_page = LoginPage(page)
    await page.goto("https://www.saucedemo.com/")
    await page.wait_for_timeout(3000)  # Espera para visualizar la página de login

    await login_page.login(username, password)
    await page.wait_for_url("https://www.saucedemo.com/inventory.html")
    await page.wait_for_timeout(3000)  # Espera después de iniciar sesión

    # **Paso 2: Agregar productos al carrito**
    inventory_page = InventoryPage(page)
    product1 = "Test.allTheThings() T-Shirt (Red)"
    product2 = "Sauce Labs Bike Light"
    
    await inventory_page.add_to_cart(product1)
    await page.wait_for_timeout(2000)  # Espera después de agregar primer producto
    await inventory_page.add_to_cart(product2)
    await page.wait_for_timeout(2000)  # Espera después de agregar segundo producto
    assert await inventory_page.get_cart_count() == "2"

    # **Paso 3: Verificar carrito**
    await page.locator(".shopping_cart_link").click()
    await page.wait_for_url("https://www.saucedemo.com/cart.html")
    await page.wait_for_timeout(3000)  # Espera en la página del carrito

    cart_page = CartPage(page)
    products = await cart_page.get_products()
    expected_products = [(product1, "$15.99"), (product2, "$9.99")]
    assert sorted(products) == sorted(expected_products)

    # **Paso 4: Proceso de checkout**
    await page.locator("//button[@id='checkout']").click()
    await page.wait_for_url("https://www.saucedemo.com/checkout-step-one.html")
    await page.wait_for_timeout(3000)  # Espera en la página de checkout

    checkout_info_page = CheckoutInformationPage(page)
    await checkout_info_page.fill_information(first_name, last_name, postal_code)
    await page.wait_for_url("https://www.saucedemo.com/checkout-step-two.html")
    await page.wait_for_timeout(3000)  # Espera en la página de resumen

    # **Paso 5: Verificar página de resumen**
    checkout_summary_page = CheckoutSummaryPage(page)
    subtotal = await checkout_summary_page.get_subtotal()
    tax = await checkout_summary_page.get_tax()
    total = await checkout_summary_page.get_total()

    assert subtotal == "Item total: $25.98"
    assert tax == "Tax: $2.08"
    assert total == "Total: $28.06"
    await page.wait_for_timeout(3000)  # Espera para visualizar los precios

    # **Paso 6: Completar compra**
    await checkout_summary_page.complete_purchase()
    await page.wait_for_url("https://www.saucedemo.com/checkout-complete.html")
    await page.wait_for_timeout(3000)  # Espera en la página de confirmación

    # **Paso 7: Verificar mensaje de confirmación**
    confirmation_page = ConfirmationPage(page)
    assert await confirmation_page.is_confirmation_displayed()
    await page.wait_for_timeout(3000)  # Espera final para ver el mensaje





