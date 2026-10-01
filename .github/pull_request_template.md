## Resumen

<!-- Qué cambia y por qué, en dos o tres líneas. -->

## Cambios

-

## Casos de prueba afectados

<!-- IDs @tc-* añadidos o modificados y, si aplica, bugs conocidos (@known-bug). -->

## Cómo probar

```bash
pytest -m smoke
```

## Checklist

- [ ] `ruff check .` y `ruff format --check .` en verde
- [ ] Los page objects solo exponen locators y acciones; las verificaciones están en los steps
- [ ] Datos y valores esperados en `data/comun` (o en `data/<env>`), sin literales en los steps
- [ ] Sin esperas fijas (assertions web-first, `page.clock` o esperas con límite desde YAML)
- [ ] Escenarios con `@smoke` o `@regression` y su `@tc-*`; los bugs reales con `@known-bug` y motivo en `bugs.yaml`
- [ ] Sin secretos ni artefactos (reports/, test-results/) en el commit
