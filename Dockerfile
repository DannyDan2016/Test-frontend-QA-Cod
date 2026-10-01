# Imagen oficial de Playwright para Python. La etiqueta DEBE coincidir con la versión
# de playwright fijada en requirements.txt (playwright==1.63.0): así los navegadores que
# trae la imagen (en /ms-playwright) son exactamente los que espera la librería y no hace
# falta ejecutar `playwright install`.
FROM mcr.microsoft.com/playwright/python:v1.63.0-noble

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Dependencias primero para aprovechar la caché de capas de Docker. Por defecto solo las de
# ejecución; la CI construye con REQUIREMENTS_FILE=requirements-dev.txt para tener también ruff.
ARG REQUIREMENTS_FILE=requirements.txt
COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r "${REQUIREMENTS_FILE}"

# Código de la suite. El .env queda fuera gracias a .dockerignore; la configuración
# se inyecta en tiempo de ejecución (variables de entorno o env_file de docker compose).
COPY --chown=pwuser:pwuser . .

# Directorios de salida con permisos para pwuser (se montan como volúmenes en compose).
RUN mkdir -p reports test-results \
    && chown -R pwuser:pwuser /app

# Usuario no root que ya incluye la imagen oficial.
USER pwuser

# Por defecto, la suite completa como en la CI: en paralelo y después @performance en serie
# (ver ci/ejecutar_suite.sh). Allure en reports/ y artefactos de los fallos en test-results/.
CMD ["bash", "ci/ejecutar_suite.sh", "chromium"]
