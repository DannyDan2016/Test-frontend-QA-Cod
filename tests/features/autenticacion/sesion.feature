# language: es
Característica: Páginas protegidas por sesión
  Como responsable de la tienda
  Quiero que las páginas internas exijan sesión
  Para que nadie navegue por ellas sin identificarse

  @negative @tc-ses-001
  Esquema del escenario: Sin sesión, <pagina> redirige al login
    Dado que no he iniciado sesión
    Cuando accedo directamente a la página "<pagina>"
    Entonces vuelvo al login con el aviso de acceso restringido a "<pagina>"

    @smoke
    Ejemplos: Inventario
      | pagina     |
      | inventario |

    @regression
    Ejemplos: Resto de páginas internas
      | pagina                |
      | carrito               |
      | checkout_informacion  |
      | catalogo_con_spinner  |
