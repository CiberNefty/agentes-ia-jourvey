import requests
import os
from datetime import datetime

def llamar_ollama(mensajes):
    url = "http://localhost:11434/api/chat"
    datos = {
        "model": "llama3.2",
        "messages": mensajes,
        "stream": False
    }
    respuesta = requests.post(url, json=datos)
    return respuesta.json()["message"]["content"]

def leer_archivo(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error leyendo archivo: {e}"

def guardar_reporte(contenido):
    os.makedirs("resultados", exist_ok=True)
    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta = f"resultados/reporte_batch_{fecha}.txt"
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)
    print(f"\n💾 Reporte guardado en: {ruta}")
    return ruta

def analizar_un_archivo(ruta, numero):
    print(f"\n📄 [{numero}] Analizando: {ruta}")
    contenido = leer_archivo(ruta)
    
    resultado = llamar_ollama([
        {
            "role": "system",
            "content": """Eres un analizador de texto experto.
Analizás cualquier texto y respondés SIEMPRE en este formato exacto:
TEMA: (tema principal en una línea)
RESUMEN: (2 oraciones máximo)
PALABRAS CLAVE: (3 palabras separadas por comas)
TONO: (positivo/negativo/neutral)"""
        },
        {
            "role": "user",
            "content": f"Analiza este texto:\n\n{contenido}"
        }
    ])
    return {"archivo": ruta, "analisis": resultado}

def comparar_archivos(resultados):
    print("\n🔄 Agente comparador trabajando...")
    
    textos = "\n\n".join([
        f"Archivo {i+1} ({r['archivo']}):\n{r['analisis']}"
        for i, r in enumerate(resultados)
    ])
    
    comparacion = llamar_ollama([
        {
            "role": "system",
            "content": "Eres un experto en comparar y sintetizar información. Respondés en español de forma clara."
        },
        {
            "role": "user",
            "content": f"Compará estos análisis e identifica similitudes y diferencias:\n\n{textos}"
        }
    ])
    return comparacion

def agente_batch(carpeta):
    print(f"\n=== Procesando carpeta: {carpeta} ===")
    
    # Buscar todos los .txt en la carpeta
    archivos = [
        os.path.join(carpeta, f) 
        for f in os.listdir(carpeta) 
        if f.endswith(".txt")
    ]
    
    if not archivos:
        print("No encontré archivos .txt en esa carpeta")
        return
    
    print(f"📁 Encontré {len(archivos)} archivos: {[os.path.basename(a) for a in archivos]}")
    
    # Analizar cada archivo
    resultados = []
    for i, archivo in enumerate(archivos):
        resultado = analizar_un_archivo(archivo, i+1)
        resultados.append(resultado)
        print(f"✅ [{i+1}/{len(archivos)}] Listo")
    
    # Comparar todos
    comparacion = comparar_archivos(resultados)
    
    # Armar reporte final
    reporte = f"""REPORTE BATCH — {datetime.now().strftime('%d/%m/%Y %H:%M')}
{'='*50}
Archivos procesados: {len(archivos)}

ANÁLISIS INDIVIDUALES
{'='*50}
"""
    for r in resultados:
        reporte += f"\n📄 {r['archivo']}\n{r['analisis']}\n{'-'*30}\n"
    
    reporte += f"\nCOMPARACIÓN GENERAL\n{'='*50}\n{comparacion}"
    
    guardar_reporte(reporte)
    print("\n✅ Batch completado!")
    print(f"\n🔍 COMPARACIÓN:\n{comparacion}")

if __name__ == "__main__":
    print("=== Agente Batch — Analiza múltiples archivos ===")
    
    # Crear archivos de prueba si no existen
    os.makedirs("documentos", exist_ok=True)
    
    with open("documentos/perfil_daniel.txt", "w", encoding="utf-8") as f:
        f.write("Me llamo Daniel. Soy de Colombia. Aprendo Python y agentes de IA. Quiero trabajar como developer IA.")
    
    with open("documentos/metas_2025.txt", "w", encoding="utf-8") as f:
        f.write("Mis metas son conseguir trabajo en tech, aprender multiagentes, construir proyectos reales y crecer profesionalmente.")
    
    with open("documentos/habilidades.txt", "w", encoding="utf-8") as f:
        f.write("Habilidades actuales: Python básico, Git, GitHub, Ollama, agentes de IA. En progreso: multiagentes, APIs, automatización.")
    
    agente_batch("documentos")