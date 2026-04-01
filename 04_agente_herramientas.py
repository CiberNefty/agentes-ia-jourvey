import requests
import json
from datetime import datetime

# --- HERRAMIENTAS que el agente puede usar ---

def obtener_hora():
    ahora = datetime.now()
    return f"Son las {ahora.strftime('%H:%M')} del {ahora.strftime('%d/%m/%Y')}"

def calcular(operacion):
    try:
        resultado = eval(operacion)
        return f"{operacion} = {resultado}"
    except:
        return "No pude calcular eso"

def contar_palabras(texto):
    palabras = len(texto.split())
    caracteres = len(texto)
    return f"El texto tiene {palabras} palabras y {caracteres} caracteres"

# Mapa de herramientas disponibles
HERRAMIENTAS = {
    "hora": obtener_hora,
    "calcular": calcular,
    "contar": contar_palabras
}

def detectar_herramienta(mensaje):
    mensaje = mensaje.lower()
    if "hora" in mensaje or "tiempo" in mensaje:
        return "hora", None
    if any(op in mensaje for op in ["+", "-", "*", "/", "cuanto es", "calcula"]):
        # Extraer la operación matemática
        partes = mensaje.replace("cuanto es", "").replace("calcula", "").strip()
        return "calcular", partes
    if "cuantas palabras" in mensaje or "contar" in mensaje:
        return "contar", mensaje
    return None, None

def agente_con_herramientas():
    url = "http://localhost:11434/api/chat"
    historial = [
        {
            "role": "system",
            "content": """Eres un asistente útil con acceso a herramientas.
Respondés siempre en español y eres directo.
Cuando el usuario pregunte la hora, mencionás la hora exacta que te dan.
Cuando calculés algo, mostrás el resultado claramente."""
        }
    ]

    print("=== Agente con Herramientas ===")
    print("Puedo: decirte la hora, calcular matemáticas, contar palabras")
    print("(escribe 'salir' para terminar)\n")

    while True:
        mensaje_usuario = input("Tú: ")

        if mensaje_usuario.lower() == "salir":
            break

        # Detectar si necesita una herramienta
        herramienta, parametro = detectar_herramienta(mensaje_usuario)
        contexto_extra = ""

        if herramienta:
            funcion = HERRAMIENTAS[herramienta]
            if parametro:
                resultado_herramienta = funcion(parametro)
            else:
                resultado_herramienta = funcion()
            contexto_extra = f"\n[Resultado de herramienta: {resultado_herramienta}]"
            print(f"🔧 Usando herramienta '{herramienta}'...")

        historial.append({
            "role": "user",
            "content": mensaje_usuario + contexto_extra
        })

        datos = {
            "model": "llama3.2",
            "messages": historial,
            "stream": False
        }

        respuesta = requests.post(url, json=datos)
        resultado = respuesta.json()
        mensaje_agente = resultado["message"]["content"]

        historial.append({
            "role": "assistant",
            "content": mensaje_agente
        })

        print(f"\nAgente: {mensaje_agente}\n")

if __name__ == "__main__":
    agente_con_herramientas()