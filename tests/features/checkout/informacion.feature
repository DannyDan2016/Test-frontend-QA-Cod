# language: es
Característica: Datos del comprador en el checkout
  Como responsable de la tienda
  Quiero que nombre, apellido y código postal sean obligatorios
  Para poder entregar cada pedido

  Antecedentes:
    Dado que inicié sesión como "estandar"
    Y que tengo en el carrito la compra "un_producto"
    Y que estoy en el paso de información del checkout

  @regression @negative @tc-chk1-002
  Esquema del escenario: No se puede continuar con <caso>
    Cuando completo mis datos con el caso "<caso>"
    Y continúo con el checkout
    Entonces veo el error del checkout del caso "<caso>"
    Y sigo en el paso de información del checkout

    Ejemplos:
      | caso                |
      | nombre_vacio        |
      | apellido_vacio      |
      | codigo_postal_vacio |
