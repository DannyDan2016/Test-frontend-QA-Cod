Test-frontend-QA-Cod

Este proyecto consiste en la automatización de pruebas para la aplicación web SauceDemo utilizando Python + Playwright, siguiendo buenas prácticas como el Page Object Model (POM) y la ejecución de pruebas con pytest.

📌 Objetivo

Automatizar el siguiente flujo en la página: SauceDemo:

Login

Acceder a la página de inicio de sesión.

Autenticarse con las credenciales:

Usuario: standard_user

Contraseña: secret_sauce

Verificar que el usuario ingresó correctamente al inventario.

Agregar productos al carrito

Seleccionar los productos Test.allTheThings() T-Shirt (Red) y Sauce Labs Bike Light.

Validar que el contador del carrito se actualiza correctamente.

Verificación en el carrito

Acceder al carrito.

Validar que los productos agregados aparecen con los datos correctos (nombre, precio).

Proceso de Checkout

Ir al checkout e ingresar datos de usuario (nombre, apellido, código postal).

Validar el subtotal, impuestos y total en la página de resumen.

Finalizar la compra y verificar el mensaje de confirmación.

📂 Estructura del Proyecto

Test-frontend-QA-Cod/
│-- pages/                # Clases de Page Object Model (POM)
│   ├── __init__.py
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   ├── checkout_information_page.py
│   ├── checkout_summary_page.py
│   ├── confirmation_page.py
│-- tests/                # Casos de prueba
│   ├── __init__.py
│   ├── test_shopping.py
│   ├── conftest.py
│-- config.json           # Datos de prueba como usuarios y contraseñas
│-- pytest.ini            # Configuración de pytest
│-- requirements.txt      # Dependencias del proyecto
│-- README.md             # Documentación

🚀 Instalación y Configuración

1️⃣ Clonar el repositorio

git clone git@github.com:DannyDan2016/Test-frontend-QA-Cod.git
cd Test-frontend-QA-Cod

2️⃣ Crear un entorno virtual e instalar dependencias

python -m venv venv
source venv/bin/activate  # En Mac/Linux
venv\Scripts\activate     # En Windows


3️⃣ Configurar Playwright

playwright install

🛠️ Ejecución de Pruebas

Ejecutar todas las pruebas:

pytest

Ejecutar pruebas con reporte detallado:

pytest -v --html=report.html --self-contained-html

Ejecutar una prueba específica:

pytest tests/test_shopping.py

📊 Reportes

Los reportes de ejecución se generan automáticamente con allure en un archivo report.html. Puedes abrirlo en cualquier navegador para visualizar los resultados de las pruebas.

🤝 Contribuciones

Si deseas contribuir a este proyecto:

Haz un fork del repositorio.

Crea una nueva rama (git checkout -b feature-nueva).

Realiza tus cambios y haz commit (git commit -m 'Descripción del cambio').

Sube los cambios (git push origin feature-nueva).

Abre un Pull Request para revisión.

📜 Licencia

Autor Danny Parrado