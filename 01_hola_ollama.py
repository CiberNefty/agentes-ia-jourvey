import requests
import json

def hablar_con_ollama(mensaje):
    url = "http://localhost:11434/api/generate"
    
    datos = {
        "model": "llama3.2",
        "prompt": mensaje,
        "stream": False
    }
    
    print(f"\n🧠 Tú: {mensaje}")
    print("🤖 Ollama pensando...")
    
    respuesta = requests.post(url, json=datos)
    resultado = respuesta.json()
    
    print(f"🦙 Llama3.2: {resultado['response']}")
    return resultado['response']

# Tu primera conversación con IA local
if __name__ == "__main__":
    print("=== Mi primer agente con Ollama ===")
    hablar_con_ollama("Hola! Presentate en español en 2 oraciones.")
    hablar_con_ollama("Cual seria el limite de usar ollama en mi pc?, Podemos hacer una ruta de aprendizaje de ia enfocado a multiagentes? con pyhton?")