# language: es
Característica: Catálogo dinámico con indicador de carga
  Como cliente de Swag Labs
  Quiero ver un indicador mientras se cargan los productos
  Para saber que la página está trabajando

  @regression @tc-dyn-002 @tc-dyn-003
  Escenario: El indicador de carga se muestra hasta que llegan los productos
    Dado que inicié sesión como "estandar"
    Y que el reloj del navegador está en pausa
    Cuando abro el catálogo dinámico con indicador de carga
    Entonces veo el indicador de carga
    Cuando transcurre el tiempo máximo de carga
    Entonces el indicador de carga desaparece
    Y la rejilla muestra todos los productos del catálogo
