import requests

def chat_con_memoria():
    url = "http://localhost:11434/api/chat"
    historial = []
    
    print("=== Agente con Memoria ===")
    print("(escribe 'salir' para terminar)\n")
    
    while True:
        mensaje_usuario = input("Tú: ")
        
        if mensaje_usuario.lower() == "salir":
            print("Agente: ¡Hasta luego!")
            break
        
        # Agregar mensaje del usuario al historial
        historial.append({
            "role": "user",
            "content": mensaje_usuario
        })
        
        # Enviar TODO el historial a Ollama
        datos = {
            "model": "llama3.2",
            "messages": historial,
            "stream": False
        }
        
        respuesta = requests.post(url, json=datos)
        resultado = respuesta.json()
        mensaje_agente = resultado["message"]["content"]
        
        # Guardar respuesta en historial también
        historial.append({
            "role": "assistant", 
            "content": mensaje_agente
        })
        
        print(f"Agente: {mensaje_agente}\n")

if __name__ == "__main__":
    chat_con_memoria()