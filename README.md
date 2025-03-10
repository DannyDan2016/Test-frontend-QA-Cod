# Testfrontend-QA-Cod

Este repositorio contiene un proyecto de automatización de pruebas para la aplicación web Sauce Demo utilizando Python y Playwright, siguiendo buenas prácticas como el Page Object Model (POM) y la ejecución de pruebas con Pytest.

## Objetivo

Este proyecto automatiza el siguiente flujo en la página de Sauce Demo:

1. **Login:**
   - Acceder a la página de inicio de sesión.
   - Autenticarse con las credenciales:
     - Usuario: standard_user
     - Contraseña: secret_sauce
   - Verificar que el usuario ingresó correctamente al inventario.

2. **Agregar productos al carrito:**
   - Seleccionar los productos: Test.allTheThings() T-Shirt (Red) y Sauce Labs Bike Light.
   - Validar que el contador del carrito se actualiza correctamente.

3. **Verificación en el carrito:**
   - Acceder al carrito.
   - Validar que los productos agregados aparecen con los datos correctos (nombre y precio).

4. **Proceso de Checkout:**
   - Ir al checkout e ingresar datos de usuario (nombre, apellidos, código postal).
   - Validar el subtotal, impuestos y total en la página de resumen.
   - Finalizar la compra y verificar el mensaje de confirmación.

## Estructura del Proyecto

Testfrontend-QA-Cod/
├── pages/                # Clases del Page Object Model (POM)
│   ├── init.py
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   ├── checkout_information_page.py
│   ├── checkout_summary_page.py
│   ├── confirmation_page.py
├── tests/                # Casos de prueba
│   ├── init.py
│   ├── test_shopping.py
│   ├── conftest.py
├── config.json           # Datos de prueba como usuarios y contraseñas
├── pytest.ini            # Configuración de Pytest      # Dependencias del proyecto
├── README.md             # Documentación


## Instalación y Configuración

1. **Clonar el repositorio:**

   ```bash
   git clone git@github.com:DannyDan2016/Testfrontend-QA-Cod
   cd Testfrontend-QA-Cod

2. Crear un entorno virtual e instalar dependencias:
   python -m venv venv
source venv/bin/activate  # En Mac/Linux
venv\Scripts\activate     # En Windows

3. Configurar Playwright:
playwright install

Ejecutar todas las pruebas:

Pytest


Ejecutar una prueba específica:

pytest tests/test_shopping.py

## Reportes
Los reportes de ejecución se generan automáticamente como un archivo HTML denominado report.html. Puedes abrirlos en cualquier navegador web para visualizar los resultados de las pruebas.

Artefactos
Videos: Los videos grabados de las ejecuciones de las pruebas se guardan en el directorio 'videos'.
Capturas de pantalla: Las capturas de pantalla tomadas durante la ejecución de las pruebas se guardan en el directorio 'screenshots'.
Contribuciones
Si deseas contribuir a este proyecto:

Haz un fork del repositorio.
Crea una nueva rama (por ejemplo, git checkout -b feature-nueva).
Realiza tus cambios y haz commit (por ejemplo, git commit -m 'Descripción del cambio').
Sube los cambios (por ejemplo, git push origin feature-nueva).
Abre un Pull Request para revisión.


## Licencia
Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para obtener más detalles.

