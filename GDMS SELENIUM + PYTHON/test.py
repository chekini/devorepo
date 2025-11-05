#!/usr/bin/env python3

"""
GDMS SELENIUM + PYTHON/test.py

Ejemplo mínimo con Selenium para cargar la página https://www.gdms.cloud/login

Instrucciones rápidas:
- Instala Selenium: pip install selenium
- Asegúrate de tener un navegador (ej. Chrome) instalado. Desde Selenium 4.6+ Selenium Manager maneja el driver automáticamente.
- Ejecuta: python "GDMS SELENIUM + PYTHON/test.py"

Este archivo incluye comentarios inline que explican qué hace cada bloque y por qué se utiliza.
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

def load_page(url: str, timeout: int = 10, headless: bool = False,
              wait_css_selector: str = None, take_screenshot: bool = True,
              screenshot_path: str = "gdms_login_screenshot.png"):
    """
    Abre el navegador, carga la URL y espera hasta que el documento esté totalmente cargado.

    Parámetros:
    - url: URL a cargar
    - timeout: segundos máximos a esperar por las condiciones de carga
    - headless: si True, ejecuta el navegador sin interfaz (útil para servidores/CI)
    - wait_css_selector: CSS selector del elemento que indica que la página está lista (ej. campo usuario)
    - take_screenshot: si True guarda una captura después de las esperas
    - screenshot_path: ruta/nombre del archivo de la captura

    Estrategia de espera:
    1) document.readyState == "complete" (carga inicial).
    2) Espera por un selector específico (recomendado para SPAs).
    3) Intento de jQuery.active == 0 si existe jQuery.
    4) (Opcional) Espera a que un spinner desaparezca.
    Sólo después de esas condiciones se toma la captura y se cierra el navegador.
    """

    # Options: permite configurar el navegador (modo headless, flags de estabilidad).
    options = Options()
    if headless:
        # Ejecutar en modo headless (sin UI). Útil para servidores/CI.
        # "--headless=new" es la recomendación en versiones recientes de Chrome/Selenium.
        options.add_argument("--headless=new")
        # Flags adicionales para evitar problemas en contenedores/CI.
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

    # Crear la instancia del WebDriver.
    # webdriver.Chrome() usa Selenium Manager (Selenium >=4.6) para localizar/descargar chromedriver.
    # Si usas otro navegador, cambia por webdriver.Firefox() y las opciones correspondientes.
    driver = webdriver.Chrome(options=options)

    try:
        # driver.get solicita la URL y espera el evento load del documento principal.
        # Sin embargo, muchas aplicaciones modernas cargan recursos asíncronos (fetch/XHR) después,
        # por eso hacemos esperas adicionales más abajo.
        driver.get(url)

        # Espera básica: document.readyState == "complete".
        # Esto indica que el documento y recursos iniciales terminaron de cargarse.
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        # Si se proporciona un selector, esperar explícitamente a que ese elemento sea visible.
        # Esto es la estrategia más robusta para SPAs: esperar por el input del login o el formulario.
        if wait_css_selector:
            WebDriverWait(driver, timeout).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, wait_css_selector))
            )
        else:
            # Si no hay selector, intentamos comprobar si jQuery ha terminado sus XHRs.
            # Muchas apps antiguas usan jQuery; jQuery.active == 0 indica que no hay requests activas.
            try:
                WebDriverWait(driver, max(1, int(timeout / 2))).until(
                    lambda d: d.execute_script("return (window.jQuery ? jQuery.active == 0 : true)")
                )
            except TimeoutException:
                # Si falla o no existe jQuery, lo ignoramos: recomendamos usar wait_css_selector para mayor fiabilidad.
                pass

        # (Opcional) Espera por la invisibilidad de un spinner/loader si conoces su selector.
        # Ejemplo:
        # try:
        #     WebDriverWait(driver, 5).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".spinner")))
        # except TimeoutException:
        #     pass

        # Tras las esperas, hacemos la captura (si está habilitada).
        # driver.save_screenshot toma el viewport actual y lo guarda en disco.
        # Esto es útil en modo headless o para debug cuando algo falla.
        if take_screenshot:
            driver.save_screenshot(screenshot_path)
            print("Captura guardada en", screenshot_path)

        # Información útil después de la carga: por ejemplo, el título de la página.
        print("Página cargada. Título:", driver.title)

        # Aquí puedes añadir interacciones: localizar inputs, enviar credenciales, pulsar botones, etc.
        # Ejemplo (no activado): driver.find_element(By.NAME, "username").send_keys("mi_usuario")

    except TimeoutException:
        # Si una de las condiciones de espera no se completa en el timeout indicado.
        print(f"No se completó la condición en {timeout} segundos.")
    finally:
        # Cerramos el navegador para liberar recursos.
        driver.quit()

if __name__ == "__main__":
    # URL objetivo
    target_url = "https://www.gdms.cloud/login"
    # Llamada de ejemplo: timeout 15 segundos, sin headless para ver la ventana.
    # Se recomienda pasar wait_css_selector al llamar, por ejemplo 'input[name=\"username\"]'
    load_page(target_url, timeout=15, headless=False, wait_css_selector='input[name=\"username\"]')