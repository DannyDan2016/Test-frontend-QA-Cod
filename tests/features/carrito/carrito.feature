# language: es
Característica: Carrito de compra
  Como cliente de Swag Labs
  Quiero ver cuántos productos llevo en el carrito
  Para saber en todo momento qué voy a comprar

  Antecedentes:
    Dado que inicié sesión como "estandar"

  @smoke @tc-inv-004 @tc-inv-006
  Escenario: Añadir y quitar productos actualiza el contador del carrito
    Cuando añado al carrito los productos de la compra "dos_productos"
    Entonces el contador del carrito coincide con los productos del carrito
    Cuando quito del carrito el producto "camiseta_roja"
    Entonces el contador del carrito coincide con los productos del carrito
    Cuando quito del carrito el producto "luz_bicicleta"
    Entonces el contador del carrito desaparece
