# Proyecto de pruebas - SauceDemo

Proyecto de automatizacion de algunas funciones de [SauceDemo](https://www.saucedemo.com/). Se uso Python, pytest y Selenium.

## Que se prueba

El proyecto incluye las pruebas que pide la pre-entrega:

- Login con el usuario `standard_user` y la contraseña `secret_sauce`.
- Revision de la lista de productos, sus nombres y precios.
- Agregar un producto y revisar que aparezca en el carrito.
- Cada prueba arranca por separado para que no dependa de otra.
- Reporte HTML con el resultado de la ejecucion.

## Carpetas y archivos

```text
pages/
  login_page.py
  inventory_page.py
  cart_page.py
tests/
  conftest.py
  test_saucedemo.py
pytest.ini
requirements.txt
```

## Antes de empezar

- Python 3.10 o una version mas nueva.
- Google Chrome instalado.
- Selenium se encarga de buscar el driver compatible.

## Instalacion

```bash
python -m venv .venv
# Windows PowerShell
.\\.venv\\Scripts\\Activate.ps1
# macOS/Linux
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Como ejecutar

Para correr todas las pruebas:

```bash
python -m pytest
```

Para generar el reporte HTML:

```bash
python -m pytest tests/test_saucedemo.py --html=reports/reporte.html --self-contained-html
```

El reporte se guarda en `reports/reporte.html`.

Tambien se guarda un log en `reports/execution.log`. Si alguna prueba falla, se guarda una captura y un archivo de texto con la URL en `reports/evidencias/`.

Si quiero ver el navegador mientras corren las pruebas:

```powershell
$env:HEADLESS = "false"
python -m pytest
```

La URL y las credenciales se pueden cambiar con variables de entorno, sin tocar el codigo:

```powershell
$env:SAUCEDEMO_USER = "standard_user"
$env:SAUCEDEMO_PASSWORD = "secret_sauce"
$env:SAUCEDEMO_URL = "https://www.saucedemo.com/"
python -m pytest
```

## Casos que quedaron hechos

1. Login correcto: se llega a `/inventory.html` y aparecen productos.
2. Catalogo: se controla que los productos tengan nombre y precio.
3. Se revisa que esten `Sauce Labs Backpack` y `Sauce Labs Bike Light`.
4. Se agrega `Sauce Labs Backpack` y se controla que aparezca en el carrito.

## Como se separaron las pruebas

Cada prueba abre un navegador nuevo. Para las pruebas del catalogo y del carrito se hace el login nuevamente, asi una prueba no queda dependiendo del resultado de otra.

## Para subirlo a Git

Los commits se pueden hacer separados para mostrar los cambios del proyecto:

```bash
git commit -m "chore: configurar proyecto de automatizacion"
git commit -am "test: agregar pruebas de login y catalogo"
git commit -am "test: agregar prueba del carrito"
git commit -am "docs: agregar README y reporte"
git push origin main
```
