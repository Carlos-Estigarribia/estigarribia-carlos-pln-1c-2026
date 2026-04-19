import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # 1. Instanciamos el navegador Chromium de forma visible (headless=False)
    print("Levantando el navegador...")
    browser = p.chromium.launch(headless=False)

    # 2. Creamos el contexto (modo incógnito puro)
    context = browser.new_context()

    # 3. Abrimos una pestaña nueva en ese contexto
    page = context.new_page()

    # Instruimos a la página a navegar a la URL
    print("Navegando hacia lanacion.com.ar...")
    page.goto("https://www.lanacion.com.ar/")

    # Esperamos 5 segundos reales para observar qué pasa
    time.sleep(5)

    # Obtenemos el título de la pestaña actual para confirmar que cargó
    print(f"Conexión exitosa. Título de la pestaña cargada: {page.title()}")

    # Cerramos el navegador para no saturar la memoria RAM de nuestra máquina
    browser.close()
    print("Navegador cerrado de forma segura.")
