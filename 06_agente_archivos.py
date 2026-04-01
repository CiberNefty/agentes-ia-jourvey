import requests
import os

def leer_archivo(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return f"Error: no pude leer el archivo {ruta}"

def guardar_resultado(nombre, contenido):
    os.makedirs("resultados", exist_ok=True)
    ruta = f"resultados/{nombre}"
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)
    print(f"💾 Guardado en: {ruta}")

def llamar_ollama(mensajes):
    url = "http://localhost:11434/api/chat"
    datos = {
        "model": "llama3.2",
        "messages": mensajes,
        "stream": False
    }
    respuesta = requests.post(url, json=datos)
    return respuesta.json()["message"]["content"]

def analizar_archivo(ruta):
    print(f"\n📂 Leyendo: {ruta}")
    contenido = leer_archivo(ruta)
    print(f"📄 Contenido leído ({len(contenido)} caracteres)")

    # Agente 1 — Resume
    print("\n🧠 Agente 1: resumiendo...")
    resumen = llamar_ollama([
        {"role": "system", "content": "Eres un experto en resumir textos. Respondés en español, de forma clara y breve."},
        {"role": "user", "content": f"Resume este texto en 3 puntos clave:\n\n{contenido}"}
    ])
    print(f"📝 Resumen:\n{resumen}")

    # Agente 2 — Analiza
    print("\n🔍 Agente 2: analizando...")
    analisis = llamar_ollama([
        {"role": "system", "content": "Eres un analista experto. Identificás fortalezas y oportunidades de mejora. Respondés en español."},
        {"role": "user", "content": f"Analiza este perfil e identifica 2 fortalezas y 2 áreas de mejora:\n\n{contenido}"}
    ])
    print(f"💡 Análisis:\n{analisis}")

    # Agente 3 — Recomienda
    print("\n🎯 Agente 3: recomendando...")
    recomendaciones = llamar_ollama([
        {"role": "system", "content": "Eres un mentor de carrera tech. Das consejos prácticos y motivadores. Respondés en español."},
        {"role": "user", "content": f"Basándote en este perfil, da 3 recomendaciones concretas para conseguir trabajo como developer:\n\n{contenido}"}
    ])
    print(f"🚀 Recomendaciones:\n{recomendaciones}")

    # Guardar todo
    reporte = f"""REPORTE DE ANÁLISIS
==================
Archivo: {ruta}

RESUMEN
-------
{resumen}

ANÁLISIS
--------
{analisis}

RECOMENDACIONES
---------------
{recomendaciones}
"""
    guardar_resultado("reporte_perfil.txt", reporte)
    print("\n✅ Análisis completo!")

if __name__ == "__main__":
    print("=== Agente Analizador de Archivos ===")
    ruta = input("Ruta del archivo a analizar (Enter para usar mi_perfil.txt): ").strip()
    if not ruta:
        ruta = "documentos/mi_perfil.txt"
    analizar_archivo(ruta)