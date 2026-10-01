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

# Dependencias primero para aprovechar la caché de capas de Docker.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Código de la suite. El .env queda fuera gracias a .dockerignore; la configuración
# se inyecta en tiempo de ejecución (variables de entorno o env_file de docker compose).
COPY --chown=pwuser:pwuser . .

# Directorios de salida con permisos para pwuser (se montan como volúmenes en compose).
RUN mkdir -p reports/allure-results test-results \
    && chown -R pwuser:pwuser /app

# Usuario no root que ya incluye la imagen oficial.
USER pwuser

# Resultados de Allure en reports/allure-results y artefactos de Playwright
# (vídeo, captura y trace de los fallos) en test-results/.
CMD ["pytest", "--alluredir=reports/allure-results", "--output=test-results"]
