import json
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    print("Inicializando sesión en La Nación web y sorteando bloqueos preliminares...")
    page.goto("https://www.lanacion.com.ar/")

    # Minimizamos avisos de pantalla
    try:
        boton = page.wait_for_selector('button:has-text("Aceptar")', timeout=3000)
        if boton: boton.click()
    except:
        pass

    # Esperamos que cargue la portada
    print("Esperando confirmación del renderizado...")
    page.wait_for_selector("article", timeout=10000)
    page.wait_for_timeout(2000)  # Damos tiempo extra para carga diferida

    # =====================================================================
    # ESTRATEGIA: La Nación organiza su portada en BLOQUES SECCIONALES.
    # Cada bloque tiene un encabezado <h3> con la sección (ej: "Política"),
    # seguido de varios <article> con noticias de esa sección.
    # El <h3> NO está DENTRO del <article>, sino ANTES de ellos.
    # Por eso, usamos JavaScript para recorrer el DOM secuencialmente,
    # asignando a cada artículo la última sección encontrada.
    # =====================================================================

    print("Recolectando artículos con contexto seccional...")

    articulos_extraidos = page.evaluate("""
    () => {
        const resultados = [];
        let seccionActual = "General";

        // Recorremos TODOS los elementos del body en orden de aparición
        const todos = document.querySelectorAll('h3, article');

        for (const nodo of todos) {
            // Si encontramos un h3 de sección, actualizamos la sección activa
            if (nodo.tagName === 'H3') {
                const texto = nodo.innerText.trim();
                if (texto && texto.length < 60) {
                    seccionActual = texto;
                }
            }

            // Si encontramos un article, extraemos su título
            if (nodo.tagName === 'ARTICLE') {
                const h2 = nodo.querySelector('h2');
                const h1 = nodo.querySelector('h1');
                const tituloEl = h1 || h2;

                if (tituloEl) {
                    const titulo = tituloEl.innerText.trim();
                    if (titulo && titulo.length > 5) {
                        resultados.push({
                            seccion: seccionActual,
                            titulo: titulo
                        });
                    }
                }
            }
        }
        return resultados;
    }
    """)

    print(f"Se recolectaron {len(articulos_extraidos)} piezas informativas.")
    browser.close()

# Guardamos el corpus
with open("lanacion_portada.json", "w", encoding="utf-8") as f:
    json.dump(articulos_extraidos, f, indent=4, ensure_ascii=False)

print("Archivo 'lanacion_portada.json' guardado correctamente.")

# Mostramos las primeras 5 noticias con su sección
for noticia in articulos_extraidos[:5]:
    print(f"[{noticia['seccion'].upper()}] -> {noticia['titulo']}")
