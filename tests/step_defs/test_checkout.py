"""Steps del checkout: validación de los datos del comprador."""

from playwright.sync_api import expect
from pytest_bdd import parsers, scenarios, then, when

from pages import CheckoutInformationPage
from support.aserciones import verificar_pagina
from support.datos import Datos

scenarios("checkout")


@when(parsers.parse('completo mis datos con el caso "{caso}"'))
def completar_caso(
    checkout_information_page: CheckoutInformationPage, datos: Datos, caso: str
) -> None:
    cliente = datos(f"checkout.informacion.campos_obligatorios.{caso}")
    checkout_information_page.fill_information(
        cliente["nombre"], cliente["apellido"], cliente["codigo_postal"]
    )


@then(parsers.parse('veo el error del checkout del caso "{caso}"'))
def error_checkout(
    checkout_information_page: CheckoutInformationPage, datos: Datos, caso: str
) -> None:
    expect(checkout_information_page.error).to_have_text(
        datos(f"checkout.informacion.campos_obligatorios.{caso}.error")
    )


@then("sigo en el paso de información del checkout")
def sigo_en_informacion(checkout_information_page: CheckoutInformationPage, datos: Datos) -> None:
    verificar_pagina(checkout_information_page, datos("checkout.informacion.titulo"))
