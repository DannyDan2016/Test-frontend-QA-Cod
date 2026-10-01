# language: es
Característica: Usuario con rendimiento degradado
  Como responsable de la tienda
  Quiero detectar cuándo el acceso tarda más de lo aceptable
  Para que una degradación de rendimiento no pase desapercibida

  @regression @performance @tc-perf-001
  Escenario: El login del usuario lento termina dentro del umbral aceptado
    Dado que estoy en la página de login
    Cuando inicio sesión como "lento" cronometrando la carga del inventario
    Entonces el inventario carga dentro del umbral de rendimiento
