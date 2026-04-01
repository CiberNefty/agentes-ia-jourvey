import requests

def crear_agente(nombre, personalidad):
    url = "http://localhost:11434/api/chat"
    
    # System prompt — le da identidad fija al agente
    historial = [
        {
            "role": "system",
            "content": f"""Eres {nombre}, un asistente inteligente.
Tu personalidad: {personalidad}
Reglas importantes:
- Siempre recordás todo lo que el usuario te dijo en esta conversación
- Respondés siempre en español
- Eres directo y amigable
- Si el usuario te dice su nombre, lo usás en cada respuesta"""
        }
    ]
    
    print(f"\n=== {nombre} está listo ===")
    print("(escribe 'salir' para terminar)\n")
    
    while True:
        mensaje_usuario = input("Tú: ")
        
        if mensaje_usuario.lower() == "salir":
            print(f"{nombre}: ¡Hasta luego! Fue un placer charlar.")
            break
        
        historial.append({
            "role": "user",
            "content": mensaje_usuario
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
        
        print(f"\n{nombre}: {mensaje_agente}\n")

if __name__ == "__main__":
    # Podés cambiar el nombre y personalidad como quieras
    crear_agente(
        nombre="Nefty",
        personalidad="Eres un mentor de programación paciente y motivador. Celebrás cada logro del usuario."
    )