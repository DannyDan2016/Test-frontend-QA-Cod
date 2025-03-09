import os
import json
import pytest
import allure
import time
from playwright.async_api import async_playwright

# Directorios para reportes y videos
BASE_DIR = "C:\\Users\\ASTRID\\Test-frontend-QA-Cod"
REPORT_DIR = os.path.join(BASE_DIR, "allure-results")
SCREENSHOT_DIR = os.path.join(REPORT_DIR, "screenshots")
VIDEO_DIR = os.path.join(BASE_DIR, "videos", "Test-frontend-QA-Vid")  # Carpeta del video

# Nombre fijo del video
VIDEO_NAME = "Test-frontend-QA-Vid.webm"
VIDEO_PATH = os.path.join(VIDEO_DIR, VIDEO_NAME)

# Crear directorios si no existen
os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(SCREENSHOT_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)

@pytest.fixture(scope="session", autouse=True)
def configure_allure():
    """Configura el directorio de resultados de Allure."""
    os.environ["ALLURE_RESULTS_DIR"] = REPORT_DIR

@pytest.fixture(scope="session")
def test_data():
    """Carga los datos desde un archivo JSON."""
    with open("datos.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

@pytest.fixture(scope="session")
def config():
    """Carga la configuración desde config.json."""
    with open("config.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

@pytest.fixture
async def page(request):
    """ Proporciona una instancia de Playwright con grabación de video """
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=False)
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

        # Obtener el video generado (último archivo en la carpeta)
        video_files = sorted(os.listdir(VIDEO_DIR), key=lambda f: os.path.getctime(os.path.join(VIDEO_DIR, f)))
        if video_files:
            last_video = os.path.join(VIDEO_DIR, video_files[-1])  # Último archivo generado
            if os.path.exists(last_video):
                os.rename(last_video, VIDEO_PATH)  # Renombrar el video final

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """ Agrega capturas de pantalla al reporte de Allure en caso de éxito o falla """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":  # Solo adjuntar en la fase de ejecución
        test_name = item.name
        screenshot_path = os.path.join(SCREENSHOT_DIR, f"{test_name}.png")
        
        if os.path.exists(screenshot_path):
            with open(screenshot_path, "rb") as image_file:
                allure.attach(image_file.read(), name=f"Screenshot {test_name}", attachment_type=allure.attachment_type.PNG)

@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    """Genera el reporte Allure al finalizar las pruebas y lo abre automáticamente."""
    print("\n✅ Generando el reporte Allure...")
    os.system(f"allure generate {REPORT_DIR} --clean -o {os.path.join(BASE_DIR, 'allure-report')}")
    print("\n✅ Reporte generado. Abriendo en el navegador...")
    os.system(f"allure open {os.path.join(BASE_DIR, 'allure-report')}")  # Abre el reporte automáticamente

    # Mostrar mensaje con la ruta del video final
    if os.path.exists(VIDEO_PATH):
        print(f"\n🎥 El video de la ejecución está guardado en: {VIDEO_PATH}")
    else:
        print("\n⚠️ No se encontró el video de la prueba.")





















