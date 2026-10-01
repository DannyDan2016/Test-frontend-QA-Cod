# language: es
Característica: Ordenación del inventario
  Como cliente de Swag Labs
  Quiero ordenar los productos por nombre o por precio
  Para encontrar antes lo que busco

  Antecedentes:
    Dado que inicié sesión como "estandar"

  @regression @tc-sort-002 @tc-sort-003
  Esquema del escenario: Ordenar el inventario por <orden>
    Cuando ordeno el inventario por "<orden>"
    Entonces el selector muestra la opción del orden "<orden>"
    Y los productos aparecen ordenados según "<orden>"

    Ejemplos:
      | orden              |
      | nombre_ascendente  |
      | nombre_descendente |
      | precio_ascendente  |
      | precio_descendente |
