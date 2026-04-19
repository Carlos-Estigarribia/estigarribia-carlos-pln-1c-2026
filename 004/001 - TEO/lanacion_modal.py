from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False) # Lo mantenemos visible
    context = browser.new_context()
    page = context.new_page()

    print("Navegando a La Nación...")
    page.goto("https://www.lanacion.com.ar/")

    # Al ingresar a determinados diarios es común ver modales. 
    # Vamos a crear una táctica de "Intento de cierre" utilizando bloque try-except.
    # Localizamos el típico botón para Aceptar/Cerrar la política de privacidad.

    try:
        # wait_for_selector pausa la ejecución SIN USAR time.sleep hasta que el objeto exista en pantalla
        boton_aceptar = page.wait_for_selector('button:has-text("Aceptar")', timeout=5000)
        if boton_aceptar:
            boton_aceptar.click()
            print("Cuadro de diálogo de cookies identificado y cerrado exitosamente.")
    except Exception as e:
        print("No apareció banner en el plazo de espera de 5 segundos, la vía está libre.")

    browser.close()
    print("Navegador cerrado.")
