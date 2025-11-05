#!/usr/bin/env python3

"""
GDMS SELENIUM + PYTHON/test.py

Ejemplo mínimo con Selenium para cargar la página https://www.gdms.cloud/login

Instrucciones rápidas:
- Instala Selenium: pip install selenium
- Asegúrate de tener un navegador (ej. Chrome) instalado. Desde Selenium 4.6+ Selenium Manager maneja el driver automáticamente.
- Ejecuta: python "GDMS SELENIUM + PYTHON/test.py"
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

def load_page(url: str, timeout: int = 10, headless: bool = False):
    """
    Abre el navegador, carga la URL y espera hasta que el documento esté totalmente cargado.
    - url: URL a cargar
    - timeout: segundos máximos a esperar por la carga
    - headless: si True, ejecuta el navegador sin interfaz (útil para servidores/CI)
    """
    # Opciones del navegador (aquí configuramos Chrome como ejemplo).
    # Options permite añadir banderas (flags) y preferencias.
    options = Options()
    if headless:
        # Ejecutar en modo headless (sin UI). Útil para pruebas en entornos sin display.
        options.add_argument("--headless=new")  # en versiones recientes usar "--headless=new"
        # Evitar problemas en algunos entornos:
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

    # Crear la instancia del WebDriver.
    # webdriver.Chrome() usará Selenium Manager para localizar/descargar el driver automáticamente
    # (a partir de Selenium 4.6+). Si prefieres usar otro navegador, cambia aquí la clase.
    driver = webdriver.Chrome(options=options)

    try:
        # Navega a la URL. driver.get bloquea hasta que la respuesta HTTP se reciba y ocurra el evento load,
        # pero a veces recursos asíncronos siguen cargando, por eso hacemos una espera explícita.
        driver.get(url)

        # Espera explícita: comprobamos que document.readyState sea "complete".
        # WebDriverWait ejecuta la lambda periódicamente hasta que retorne True o ocurra timeout.
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        # A estas alturas el documento principal está completamente cargado.
        # Podemos obtener información útil, por ejemplo el título de la página.
        print("Página cargada. Título:", driver.title)

        # Podemos tomar una captura para comprobar visualmente (útil en modo headless).
        driver.save_screenshot("gdms_login_screenshot.png")
        print("Captura guardada en gdms_login_screenshot.png")

        # Aquí podrías localizar elementos y realizar interacciones (ej.: completar formularios).
        # Ejemplo (no usado): driver.find_element(By.NAME, "username").send_keys("mi_usuario")

    except TimeoutException:
        # Si la espera excede el timeout, capturamos la excepción y avisamos.
        print(f"No se completó la carga en {timeout} segundos.")
    finally:
        # Cerramos el navegador para liberar recursos.
        driver.quit()

if __name__ == "__main__":
    # URL objetivo
    target_url = "https://www.gdms.cloud/login"
    # Llamada de ejemplo: timeout 15 segundos, sin headless para ver la ventana.
    load_page(target_url, timeout=15, headless=False)