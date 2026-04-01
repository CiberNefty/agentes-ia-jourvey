import requests
import time
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

def guardar_log(mensaje):
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("logs/agente_autonomo.log", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {mensaje}\n")
    print(f"[{timestamp}] {mensaje}")

def tarea_analizar_carpeta():
    carpeta = "documentos"
    if not os.path.exists(carpeta):
        return "Sin archivos para analizar"
    
    archivos = [f for f in os.listdir(carpeta) if f.endswith(".txt")]
    if not archivos:
        return "Carpeta vacía"
    
    resumen = llamar_ollama([
        {"role": "system", "content": "Eres un monitor de archivos. Respondés en español en 1 oración."},
        {"role": "user", "content": f"Hay {len(archivos)} archivos: {archivos}. Resume qué tipo de contenido esperarías."}
    ])
    return resumen

def tarea_reporte_estado():
    reporte = llamar_ollama([
        {"role": "system", "content": "Eres un agente autónomo de monitoreo. Respondés en español."},
        {"role": "user", "content": f"Genera un reporte de estado del sistema para las {datetime.now().strftime('%H:%M')}. Sé breve y profesional."}
    ])
    return reporte

def tarea_sugerencia():
    sugerencia = llamar_ollama([
        {"role": "system", "content": "Eres un asistente proactivo. Das una sugerencia útil diferente cada vez. Respondés en español en 1 oración."},
        {"role": "user", "content": f"Da una sugerencia de productividad para un developer que está aprendiendo IA. Hora actual: {datetime.now().strftime('%H:%M')}"}
    ])
    return sugerencia

# Mapa de tareas que el agente ejecuta solo
TAREAS = {
    1: ("Analizar carpeta documentos", tarea_analizar_carpeta),
    2: ("Generar reporte de estado",   tarea_reporte_estado),
    3: ("Dar sugerencia proactiva",    tarea_sugerencia),
}

def agente_autonomo(ciclos=3, pausa_segundos=10):
    guardar_log("=== Agente autónomo iniciado ===")
    
    for ciclo in range(1, ciclos + 1):
        guardar_log(f"\n--- CICLO {ciclo}/{ciclos} ---")
        
        for numero, (nombre, funcion) in TAREAS.items():
            guardar_log(f"Ejecutando tarea {numero}: {nombre}")
            try:
                resultado = funcion()
                guardar_log(f"Resultado: {resultado}")
            except Exception as e:
                guardar_log(f"Error en tarea {numero}: {e}")
        
        if ciclo < ciclos:
            guardar_log(f"Esperando {pausa_segundos} segundos...")
            time.sleep(pausa_segundos)
    
    guardar_log("=== Agente autónomo finalizado ===")
    print("\n📋 Log guardado en: logs/agente_autonomo.log")

if __name__ == "__main__":
    print("=== Agente Autónomo ===")
    print("Ejecuta tareas solo, sin intervención humana")
    print("Revisa logs/agente_autonomo.log para ver el historial\n")
    
    ciclos = input("¿Cuántos ciclos? (Enter = 3): ").strip()
    ciclos = int(ciclos) if ciclos.isdigit() else 3
    
    agente_autonomo(ciclos=ciclos, pausa_segundos=10)