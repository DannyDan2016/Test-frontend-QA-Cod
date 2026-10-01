# language: es
Característica: Usuario con fallos funcionales
  Como responsable de la tienda
  Quiero que los bugs conocidos queden documentados como escenarios ejecutables
  Para enterarme en cuanto se corrijan o cambien

  @regression @known-bug @tc-prob-006
  Escenario: El usuario con problemas puede rellenar sus datos en el checkout
    Dado que inicié sesión como "problematico"
    Y que estoy en el paso de información del checkout
    Cuando completo mis datos con el cliente válido
    Entonces el formulario conserva los datos del cliente válido
