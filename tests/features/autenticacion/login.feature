# language: es
Característica: Inicio de sesión
  Como cliente de Swag Labs
  Quiero entrar con mis credenciales
  Para acceder al catálogo, y que se me avise claramente si algo falla

  Antecedentes:
    Dado que estoy en la página de login

  @smoke @tc-auth-001
  Escenario: Login correcto con el usuario estándar
    Cuando inicio sesión como "estandar"
    Entonces estoy en el inventario

  @negative @tc-auth-004 @tc-auth-005 @tc-auth-006
  Esquema del escenario: Login rechazado: <caso>
    Cuando intento iniciar sesión con el caso "<caso>"
    Entonces veo el error de login del caso "<caso>"
    Y sigo en la página de login

    @smoke
    Ejemplos: Críticos
      | caso          |
      | bloqueado     |
      | usuario_vacio |

    @regression
    Ejemplos: Validaciones
      | caso             |
      | password_erronea |
      | password_vacia   |
