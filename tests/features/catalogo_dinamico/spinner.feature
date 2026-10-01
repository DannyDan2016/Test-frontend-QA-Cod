# language: es
Característica: Catálogo dinámico con indicador de carga
  Como cliente de Swag Labs
  Quiero ver un indicador mientras se cargan los productos
  Para saber que la página está trabajando

  @regression @tc-dyn-002 @tc-dyn-003
  Escenario: El catálogo muestra los productos al terminar la carga
    Dado que inicié sesión como "estandar"
    Cuando abro el catálogo dinámico con indicador de carga
    Entonces veo el indicador de carga
    Y el indicador desaparece al terminar la carga
    Y la rejilla muestra todos los productos del catálogo
