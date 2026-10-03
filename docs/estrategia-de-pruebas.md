# Estrategia de pruebas: SauceDemo (Swag Labs)

## 1. Alcance

**Sistema bajo prueba:** https://www.saucedemo.com, la tienda de demostración pública de Sauce Labs: login, inventario, detalle de producto, carrito, checkout en tres pasos, menú lateral, footer, la sección *Dynamic Catalog* y seis usuarios con comportamientos especiales.

**Dentro del alcance**

- Funcionalidad de UI de extremo a extremo en Chromium, Firefox y WebKit.
- Validaciones y mensajes de error, control de acceso por sesión y cálculos del checkout.
- Contenido asíncrono (spinner) y rendimiento percibido del usuario degradado.
- Comportamientos incorrectos conocidos del sitio, documentados como bugs ejecutables.

**Fuera del alcance**

- Pruebas visuales por píxeles (Playwright para Python no trae `to_have_screenshot`).
- Accesibilidad automatizada (axe), emulación móvil, carga o estrés.
- Enlaces externos más allá de su `href` (About y redes sociales dependen de terceros).
- Backend o API: SauceDemo es una SPA sin API propia; el estado vive en una cookie y en `localStorage`.

## 2. Inventario y criterio de selección

Antes de automatizar se exploró el sitio con Playwright y se leyó su bundle JavaScript para confirmar la lógica de cada usuario especial. El resultado es un **inventario de 110 escenarios (166 ejecuciones)** repartidos en 18 áreas.

Esta suite **no** intenta automatizarlos todos. Es una muestra curada en la que cada escenario se eligió por al menos uno de estos criterios:

1. **Riesgo de negocio**: si falla, el cliente no puede comprar (login, carrito, checkout y compra completa).
2. **Seguridad y control de acceso**: páginas internas sin sesión, usuario bloqueado y logout.
3. **Técnica de automatización distinta** que aporte algo nuevo a la muestra:
   - partición de equivalencia con Esquemas;
   - oráculo calculado (orden e importes);
   - control del tiempo (`page.clock`);
   - medición de rendimiento;
   - bug documentado como `xfail` estricto.
4. **Coste/beneficio**: se descartan los casos que repiten la misma técnica sobre otra pantalla.

### Resumen del inventario y de lo automatizado

| Área | Qué cubre | Escenarios en el inventario | Automatizados en la muestra |
|---|---|---|---|
| AUTH | Login y mensajes | 11 | 4 (001, 004 parcial, 005 parcial, 006) |
| SES | Sesión y rutas protegidas | 7 | 1 (001: 4 de 10 rutas) |
| INV | Listado del inventario y carrito desde él | 9 | 2 (004, 006) |
| SORT | Ordenación | 4 | 2 (002, 003) |
| PDP | Detalle de producto | 6 | 0 |
| CART | Página del carrito | 7 | 0 (el E2E verifica su contenido) |
| CHK1 | Checkout: datos del comprador | 5 | 1 (002) |
| CHK2 | Checkout: resumen e importes | 6 | 0 (el E2E verifica los importes) |
| CMP | Confirmación | 3 | 0 (el E2E verifica la cabecera) |
| MENU | Menú lateral | 8 | 2 (005, 006) |
| FOOT | Footer y redes | 3 | 0 |
| DYN | Dynamic Catalog (Lazy Load, Spinner, Slider) | 11 | 2 (002, 003) |
| LONG | Ruta oculta `/inventory-long.html` | 2 | 0 |
| PROB | `problem_user` | 10 | 1 (006, `@known-bug`) |
| ERR | `error_user` | 6 | 0 |
| VIS | `visual_user` | 6 | 0 |
| PERF | `performance_glitch_user` | 3 | 1 (001) |
| E2E | Recorridos completos | 3 | 1 (001) |
| **Total** | | **110** | **17 IDs** en 12 escenarios y 23 ejecuciones |

## 3. Matriz de trazabilidad

| TC | Caso | Feature | Escenario | Técnica | Tags |
|---|---|---|---|---|---|
| TC-AUTH-001 | Login correcto | `autenticacion/login.feature` | Login correcto con el usuario estándar | camino feliz | `@smoke` |
| TC-AUTH-004 | Usuario o contraseña vacíos | `autenticacion/login.feature` | Login rechazado: `usuario_vacio`, `password_vacia` | partición de equivalencia (Esquema) | `@negative` `@smoke` (crítico) |
| TC-AUTH-005 | Credenciales inválidas | `autenticacion/login.feature` | Login rechazado: `password_erronea` | partición de equivalencia | `@negative` `@regression` |
| TC-AUTH-006 | Usuario bloqueado | `autenticacion/login.feature` | Login rechazado: `bloqueado` | negativo de seguridad | `@negative` `@smoke` |
| TC-SES-001 | Página interna sin sesión | `autenticacion/sesion.feature` | Sin sesión, `<pagina>` redirige al login | control de acceso (Esquema; el mensaje se construye con la ruta del page object) | `@negative` `@smoke` (inventario) |
| TC-SORT-002 | Las 4 ordenaciones | `inventario/ordenacion.feature` | Ordenar el inventario por `<orden>` | oráculo calculado: catálogo del YAML ordenado en Python | `@regression` |
| TC-SORT-003 | Empate de precio estable | `inventario/ordenacion.feature` | (mismo Esquema, precio) | límite: `sorted()` estable frente a la web | `@regression` |
| TC-INV-004 | Añadir actualiza el badge | `carrito/carrito.feature` | Añadir y quitar productos actualiza el contador | estado de la UI | `@smoke` |
| TC-INV-006 | Quitar decrementa y oculta el badge | `carrito/carrito.feature` | (mismo escenario) | estado de la UI | `@smoke` |
| TC-E2E-001 | Compra completa de 2 productos | `e2e/compra.feature` | Compra de dos productos con el usuario estándar | E2E; importes calculados con `Decimal` y la tasa del YAML | `@smoke` |
| TC-CHK1-002 | Campos obligatorios | `checkout/informacion.feature` | No se puede continuar con `<caso>` | validación (Esquema); precondición por cookie y `localStorage` | `@negative` `@regression` |
| TC-MENU-005 | Logout | `navegacion/menu.feature` | Cerrar sesión desde el menú | sesión: comprueba que desaparece la cookie | `@smoke` |
| TC-MENU-006 | Reset App State | `navegacion/menu.feature` | Reset App State vacía el carrito | estado | `@regression` |
| TC-DYN-002 | Spinner y rejilla | `catalogo_dinamico/spinner.feature` | El indicador de carga se muestra hasta que llegan los productos | tiempo controlado (`page.clock`), sin esperas reales | `@regression` |
| TC-DYN-003 | Productos del spinner = catálogo | `catalogo_dinamico/spinner.feature` | (mismo escenario) | oráculo del YAML ordenado por id | `@regression` |
| TC-PERF-001 | Login del usuario lento dentro del umbral | `usuarios_especiales/performance_glitch_user.feature` | El login del usuario lento termina dentro del umbral aceptado | medición con umbral del YAML, en serie | `@regression` `@performance` |
| TC-PROB-006 | Datos del checkout con `problem_user` | `usuarios_especiales/problem_user.feature` | El usuario con problemas puede rellenar sus datos en el checkout | bug documentado (`xfail` estricto) | `@regression` `@known-bug` |

Cualquier ID se ejecuta con `pytest -k <ID>`, por ejemplo `pytest -k TC-SES-001`.

## 4. Bugs reales encontrados

Todos se reprodujeron con Playwright (Chromium) el 2026-10-01. La lógica de los usuarios especiales se confirmó además en el bundle de la web (`assets/index-D3OxT1jE.js`). Los marcados como **Automatizado** forman parte de la suite como `@known-bug`: el escenario afirma el comportamiento correcto y es un `xfail(strict=True)` con el motivo en `data/comun/bugs.yaml`.

| ID | Usuario | Esperado | Observado (evidencia) | Estado |
|---|---|---|---|---|
| TC-PROB-006 | `problem_user` | Los campos del paso 1 conservan lo escrito | Al escribir en *Last Name* se sobrescribe *First Name* (`First Name = "Doe"`, `Last Name = ""`) y al continuar aparece `Error: Last Name is required` | **Automatizado** |
| TC-PROB-001 | `problem_user` | Cada producto con su imagen | Todas las imágenes son `sl-404` (un perro) | Inventariado |
| TC-PROB-002/003 | `problem_user` | Añadir y quitar los 6 productos | Solo se añaden los de id par y no se pueden quitar | Inventariado |
| TC-PROB-004/010 | `problem_user` | El título abre su detalle | Abre el producto `id + 1` | Inventariado |
| TC-PROB-005 | `problem_user` | Ordenar Z-A reordena | No hace nada | Inventariado |
| TC-PROB-007 | `problem_user` | Totales correctos | Duplica precios sin redondear (`Item total: $95.93999999999998`) | Inventariado |
| TC-ERR-001 | `error_user` | Ordenar sin errores | `alert("Sorting is broken! …")` y no ordena | Inventariado |
| TC-ERR-002/003 | `error_user` | Añadir y quitar productos | Error JS `Failed to add item to the cart.` / `Failed to remove item from cart.` | Inventariado |
| TC-ERR-005/006 | `error_user` | Apellido obligatorio y *Finish* completa | El apellido no se escribe y el formulario avanza sin él; *Finish* no completa (`La.cesetRart is not a function`) | Inventariado |
| TC-VIS-001…005 | `visual_user` | Precios e interfaz correctos | Precios aleatorios en cada carga, imagen `sl-404`, botón desalineado y clases `visual_failure` | Inventariado |
| TC-PERF-002 | `performance_glitch_user` | Login → inventario en menos de 2 s | ~5,15 s por un bloqueo síncrono en cada render | Inventariado (la muestra cubre TC-PERF-001 con un umbral ampliado) |
| TC-AUTH-011 | `locked_out_user` | Sin cookie de sesión | Se crea `session-username=locked_out_user`, aunque no da acceso | Inventariado |
| TC-MENU-007 | todos | *Reset App State* devuelve los botones a "Add to cart" | El badge se vacía pero los botones siguen en "Remove" hasta recargar | Inventariado |
| TC-CHK2-006 | todos | Subtotal `$0.00` con el carrito vacío | `Item total: $0` frente a `Tax: $0.00` | Inventariado |
| TC-DYN-011 / TC-LONG-002 | todos | Sin variantes duplicadas | "Test.allTheThings() T-Shirt (Red) (L)" aparece duplicada | Inventariado |

Hay además comportamientos dudosos pendientes de decisión de producto (bug o comportamiento aceptado):

- una ruta inexistente muestra una página en blanco (TC-SES-006);
- el logout conserva el carrito para el siguiente usuario (TC-SES-007);
- se permite el checkout con el carrito vacío (TC-CART-007);
- se aceptan campos con solo espacios (TC-CHK1-005).

**Hallazgos técnicos que condicionan la automatización**

- El `data-test="open-menu"` es una imagen tapada por el botón real: el menú se abre por rol accesible (`button` "Open Menu").
- Las rutas internas responden HTTP 404 aunque se renderizan: no se valida el código de respuesta de `goto`.
- La sesión es solo la cookie `session-username`: se usa como precondición rápida.

## 5. Decisiones de diseño

| Decisión | Motivo |
|---|---|
| Gherkin en español con steps delgados | El negocio lee los escenarios; la lógica vive en los page objects y en `support/` |
| Datos y esperados en YAML (`comun` + ambiente) | Cambiar un texto o un precio no exige tocar código; los ambientes solo declaran diferencias |
| Importes y órdenes **calculados** a partir del YAML | Un oráculo independiente detecta errores que un valor copiado de la web no detectaría |
| Sesión por cookie y carrito por `localStorage` | Escenarios independientes y rápidos; la UI de login se prueba solo donde es el objetivo |
| `@known-bug` como `xfail(strict=True)` | El bug queda documentado y ejecutable, y si se arregla el XPASS obliga a revisar el escenario |
| Spinner con `page.clock` | El tiempo aleatorio (0,5-3 s) hacía el escenario inestable con 12 navegadores en paralelo; con el reloj pausado es determinista y no usa pausas reales |
| `@performance` en serie | En paralelo se medía la contención de CPU (11-16 s) y no la app (5,15 s) |
| Telemetría `backtrace.io` bloqueada | No se ensucian métricas de terceros ni se depende de su red |
| Todo en la imagen oficial de Playwright | Mismos navegadores y dependencias en local, en Docker y en la CI |

## 6. Ejecución y entornos

| Nivel | Cuándo | Qué |
|---|---|---|
| Smoke | cada PR y push, en los 3 navegadores | 7 ejecuciones (`-m smoke`) |
| Suite curada | cada PR en Chromium; nightly en los 3 navegadores | 23 ejecuciones BDD + 14 unitarios |
| Manual | `workflow_dispatch` con expresión `-m` | a demanda |

## 7. Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| El sitio de terceros cambia sin aviso | Nightly diario; los `xfail` estrictos detectan bugs corregidos |
| Inestabilidad por tiempos aleatorios | Esperas web-first y control del reloj; nunca `wait_for_timeout` |
| Medición de tiempos dependiente del runner | Umbral en YAML por ambiente y ejecución en serie |
| Versiones desalineadas entre la imagen Docker y `playwright` | Versiones fijadas, aviso en `dependabot.yml` y comentario en el `Dockerfile` |

## 8. Próximos pasos propuestos

1. Ampliar la cobertura por áreas siguiendo el inventario: AUTH/SES completos, PDP, CART, CHK2, FOOT, Lazy Load y Slider, y el resto de usuarios especiales.
2. Matriz de trazabilidad generada automáticamente a partir de un `docs/inventario.yaml` y las tags `@tc-*`, con comprobación en la CI.
3. Histórico de Allure 3 entre ejecuciones (persistir el archivo de historia en Pages o en una rama).
4. Accesibilidad con axe y emulación móvil en el nightly.
