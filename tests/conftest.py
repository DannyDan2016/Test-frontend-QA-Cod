import os
import json
import pytest
import allure
import time
from playwright.async_api import async_playwright

# Directorios para guardar reportes y videos
RUTA_PROYECTO = "C:\\Users\\ASTRID\\Test-frontend-QA-Cod"
RUTA_REPORTES = os.path.join(RUTA_PROYECTO, "allure-results")
RUTA_CAPTURAS = os.path.join(RUTA_REPORTES, "capturas")
RUTA_VIDEOS = os.path.join(RUTA_PROYECTO, "videos", "Test-frontend-QA-Vid")

# Directorio donde se almacenarán los videos de las pruebas
VIDEO_DIR = "videos"
SCREENSHOT_DIR = "screenshots"

# Crear los directorios si no existen
os.makedirs(VIDEO_DIR, exist_ok=True)
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# Crear carpetas si no existen
os.makedirs(RUTA_REPORTES, exist_ok=True)
os.makedirs(RUTA_CAPTURAS, exist_ok=True)
os.makedirs(RUTA_VIDEOS, exist_ok=True)

@pytest.fixture(scope="session", autouse=True)
def configurar_allure():
    """Configura la carpeta donde se guardarán los reportes de Allure."""
    os.environ["ALLURE_RESULTS_DIR"] = RUTA_REPORTES

@pytest.fixture(scope="session")
def datos_prueba():
    """Carga los datos desde el archivo datos.json."""
    with open("datos.json", "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)
    return datos

@pytest.fixture(scope="session")
def config():
    """Carga la configuración desde el archivo config.json."""
    with open("config.json", "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)
    return datos

@pytest.fixture
async def page(request):
    """ Proporciona una instancia de Playwright con grabación de video y captura de pantalla. """
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        context = await browser.new_context(record_video_dir=VIDEO_DIR)  # Guarda en la carpeta

        page = await context.new_page()
        yield page  # Pasar la página a la prueba

        # Capturar screenshot al final de la prueba
        test_name = request.node.name
        screenshot_path = os.path.join(SCREENSHOT_DIR, f"{test_name}.png")
        await page.screenshot(path=screenshot_path)

        # Adjuntar screenshot a Allure
        with open(screenshot_path, "rb") as image_file:
            allure.attach(image_file.read(), name="screenshot", attachment_type=allure.attachment_type.PNG)

        await context.close()
        await browser.close()


        # Esperar un momento para que el video termine de guardarse
        time.sleep(2)

        # Obtener el último video guardado
        archivos_videos = sorted(os.listdir(RUTA_VIDEOS), key=lambda f: os.path.getctime(os.path.join(RUTA_VIDEOS, f)))
        if archivos_videos:
            ultimo_video = os.path.join(RUTA_VIDEOS, archivos_videos[-1])
            
            # Crear un nombre único con la fecha y hora
            marca_tiempo = time.strftime("%Y%m%d_%H%M%S")
            nombre_final_video = os.path.join(RUTA_VIDEOS, f"Test-frontend-QA-Vid_{marca_tiempo}.webm")

            # Renombrar el video
            os.rename(ultimo_video, nombre_final_video)
            print(f"\n🎥 Video guardado en: {nombre_final_video}")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Adjunta capturas de pantalla a Allure en caso de fallo o éxito."""
    outcome = yield
    reporte = outcome.get_result()

    if reporte.when == "call":  # Solo adjuntar en la fase de ejecución
        nombre_prueba = item.name
        ruta_captura = os.path.join(RUTA_CAPTURAS, f"{nombre_prueba}.png")
        
        if os.path.exists(ruta_captura):
            with open(ruta_captura, "rb") as imagen:
                allure.attach(imagen.read(), name=f"Captura {nombre_prueba}", attachment_type=allure.attachment_type.PNG)
