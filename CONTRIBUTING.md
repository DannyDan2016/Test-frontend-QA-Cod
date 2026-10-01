# Cómo contribuir

## Flujo

1. Crea una rama desde `main` con el formato `tipo/descripcion-kebab` (`feat`, `fix`, `test`, `refactor`, `ci`, `build`, `docs`, `chore`).
2. Haz commits atómicos con [Conventional Commits](https://www.conventionalcommits.org/es/): el tipo en inglés y la descripción en español, por ejemplo `test(checkout): cubre el código postal vacío`.
3. Antes de abrir el PR:

   ```bash
   ruff check . && ruff format --check .
   pytest -m smoke
   pytest -n auto
   ```

4. Abre el PR rellenando la plantilla. La CI debe quedar en verde.

## Page objects (`pages/`)

- Exponen **locators y acciones**, nunca verificaciones (`expect` va en los steps o en `support/aserciones.py`).
- Una acción hace una sola cosa. Por ejemplo, `fill_information` solo rellena y `continue_checkout` solo continúa.
- Usa selectores estables en este orden: `get_by_test_id` (`data-test`), roles accesibles (`get_by_role`) y texto visible. Nada de CSS frágil ni XPath.
- Lo que se repite en varias páginas va en `pages/components/` (cabecera, menú). Las páginas con sesión heredan de `AuthenticatedPage`.
- El código de `pages/` va en inglés (convención de Playwright).

## Datos (`data/`)

- Todo dato de entrada o valor esperado (usuarios, mensajes, productos, precios, umbrales) va en `data/comun/<area>.yaml`. Los textos de la UI se copian **literalmente**, con sus erratas si las hay.
- Lo que cambie por ambiente va en `data/<env>/<area>.yaml` con **solo** las claves que difieren (merge profundo).
- Los secretos nunca se escriben en un YAML: usa `${VARIABLE}` o `${VARIABLE:-defecto}` y define el valor en `.env` (local) o en los secrets de la CI. Documenta la variable en `.env.example`.
- Los steps leen los datos con `datos("archivo.clave.subclave")`. Si un esperado se puede **calcular** a partir de otros datos (importes, órdenes), calcúlalo.

## Features y steps

- Las features van en `tests/features/<area>/`, con `# language: es` y escenarios declarativos (qué, no cómo).
- Cada escenario lleva `@smoke` o `@regression`, su `@tc-area-nnn` del inventario y, si aplica, `@negative` o `@performance`.
- Un bug real del sitio se escribe afirmando el comportamiento **correcto**, con `@known-bug` y el motivo en `data/comun/bugs.yaml` bajo su ID. Sin motivo, la recolección falla.
- Una tag nueva se declara en `pytest.ini` (se ejecuta con `--strict-markers`).
- Los steps deben ser delgados: llaman a page objects, leen el YAML y verifican con `expect`. Los compartidos van en `tests/step_defs/conftest.py`; los de un área, en `tests/step_defs/test_<area>.py`.
- **Prohibidas las esperas fijas** (`time.sleep`, `wait_for_timeout`). Usa assertions web-first, `expect(...).to_be_hidden(timeout=...)` con el límite desde YAML o `page.clock` para el tiempo.
- Las precondiciones que no son el objetivo del escenario (sesión, carrito) se preparan con `support/estado_app.py`, no por la UI.

## Qué no se versiona

`.env`, `.venv/`, `reports/`, `test-results/`, `allure-results/`, `allure-report/` y las cachés. Ya están en `.gitignore`.
