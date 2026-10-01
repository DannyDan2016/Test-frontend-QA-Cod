# language: es
Característica: Compra completa
  Como cliente de Swag Labs
  Quiero elegir productos y pagarlos
  Para recibir mi pedido

  @smoke @tc-e2e-001
  Escenario: Compra de dos productos con el usuario estándar
    Dado que estoy en la página de login
    Cuando inicio sesión como "estandar"
    Y añado al carrito los productos de la compra "dos_productos"
    Entonces el contador del carrito refleja los productos añadidos
    Cuando voy al carrito
    Entonces el carrito lista los productos de la compra "dos_productos"
    Cuando inicio el checkout
    Y completo mis datos con el cliente válido
    Y continúo con el checkout
    Entonces el resumen muestra los importes calculados de la compra "dos_productos"
    Cuando finalizo la compra
    Entonces veo la confirmación del pedido
