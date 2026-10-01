#!/usr/bin/env bash
# Ejecuta la suite igual que la CI (GitHub Actions, Jenkins o docker compose):
#   1. En paralelo (pytest-xdist) todo lo que no mide tiempos.
#   2. En serie los escenarios @performance: en paralelo medirían la contención de CPU
#      entre navegadores, no la aplicación.
#
# Uso: ci/ejecutar_suite.sh [navegador] [expresión -m]
#   ci/ejecutar_suite.sh chromium              # suite completa en Chromium
#   ci/ejecutar_suite.sh firefox smoke         # solo @smoke en Firefox
#
# Resultados: reports/allure-results (fase 1) y reports/allure-results-rendimiento (fase 2);
# artefactos de fallos en test-results/ y test-results/rendimiento/.
set -uo pipefail

navegador="${1:-chromium}"
marcadores="${2:-}"

filtro_paralelo="not performance"
filtro_serie="performance"
if [[ -n "${marcadores}" ]]; then
  filtro_paralelo="(${marcadores}) and not performance"
  filtro_serie="(${marcadores}) and performance"
fi

echo "::group::Fase 1/2 - en paralelo: -m \"${filtro_paralelo}\" (${navegador})"
pytest --browser "${navegador}" -n auto -m "${filtro_paralelo}"
estado_paralelo=$?
echo "::endgroup::"

echo "::group::Fase 2/2 - en serie: -m \"${filtro_serie}\" (${navegador})"
pytest --browser "${navegador}" -m "${filtro_serie}" \
  --alluredir=reports/allure-results-rendimiento --output=test-results/rendimiento
estado_serie=$?
echo "::endgroup::"

# Código 5 = ningún test seleccionado (p. ej. @smoke no incluye @performance): no es fallo.
[[ ${estado_paralelo} -eq 5 ]] && estado_paralelo=0
[[ ${estado_serie} -eq 5 ]] && estado_serie=0

echo "Resultado: fase en paralelo=${estado_paralelo}, fase en serie=${estado_serie}"
if [[ ${estado_paralelo} -ne 0 || ${estado_serie} -ne 0 ]]; then
  exit 1
fi
