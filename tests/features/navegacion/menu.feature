# language: es
Característica: Menú lateral
  Como cliente de Swag Labs
  Quiero cerrar sesión y restablecer la tienda desde el menú
  Para dejar la aplicación en un estado limpio

  Antecedentes:
    Dado que inicié sesión como "estandar"

  @smoke @tc-menu-005
  Escenario: Cerrar sesión desde el menú
    Cuando cierro sesión desde el menú
    Entonces sigo en la página de login
    Y ya no tengo la sesión iniciada

  @regression @tc-menu-006
  Escenario: Reset App State vacía el carrito
    Dado que tengo en el carrito la compra "dos_productos"
    Cuando restablezco el estado de la aplicación desde el menú
    Entonces el contador del carrito desaparece
