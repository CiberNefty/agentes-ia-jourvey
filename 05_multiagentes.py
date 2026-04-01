import requests

def llamar_ollama(mensajes):
    url = "http://localhost:11434/api/chat"
    datos = {
        "model": "llama3.2",
        "messages": mensajes,
        "stream": False
    }
    respuesta = requests.post(url, json=datos)
    return respuesta.json()["message"]["content"]

# --- AGENTE 1: Planificador ---
def agente_planificador(tarea):
    print("\n🧠 Planificador pensando...")
    mensajes = [
        {
            "role": "system",
            "content": """Eres un planificador experto. 
Tu único trabajo es recibir una tarea y dividirla en 3 pasos concretos y simples.
Respondés SOLO con los 3 pasos, numerados, sin explicaciones extra.
Ejemplo:
1. Paso uno
2. Paso dos  
3. Paso tres"""
        },
        {
            "role": "user",
            "content": f"Divide esta tarea en 3 pasos: {tarea}"
        }
    ]
    return llamar_ollama(mensajes)

# --- AGENTE 2: Ejecutor ---
def agente_ejecutor(tarea, plan):
    print("\n⚙️ Ejecutor trabajando...")
    mensajes = [
        {
            "role": "system", 
            "content": """Eres un ejecutor experto en Python y programación.
Recibes una tarea y un plan, y escribís el código Python necesario para completarla.
Respondés con código Python listo para usar, con comentarios en español."""
        },
        {
            "role": "user",
            "content": f"""Tarea: {tarea}
            
Plan a seguir:
{plan}

Escribí el código Python para completar esta tarea."""
        }
    ]
    return llamar_ollama(mensajes)

# --- AGENTE 3: Revisor ---
def agente_revisor(tarea, plan, codigo):
    print("\n🔍 Revisor evaluando...")
    mensajes = [
        {
            "role": "system",
            "content": """Eres un revisor de código experto.
Revisás si el código cumple la tarea y el plan.
Respondés con:
- APROBADO si el código es correcto
- RECHAZADO si hay problemas, explicando qué falta"""
        },
        {
            "role": "user",
            "content": f"""Tarea original: {tarea}

Plan:
{plan}

Código producido:
{codigo}

¿El código cumple la tarea?"""
        }
    ]
    return llamar_ollama(mensajes)

# --- ORQUESTADOR: coordina los 3 agentes ---
def orquestador(tarea):
    print(f"\n{'='*50}")
    print(f"📋 TAREA: {tarea}")
    print(f"{'='*50}")
    
    # Paso 1: Planificar
    plan = agente_planificador(tarea)
    print(f"\n📝 PLAN:\n{plan}")
    
    # Paso 2: Ejecutar
    codigo = agente_ejecutor(tarea, plan)
    print(f"\n💻 CÓDIGO GENERADO:\n{codigo}")
    
    # Paso 3: Revisar
    revision = agente_revisor(tarea, plan, codigo)
    print(f"\n✅ REVISIÓN:\n{revision}")
    
    print(f"\n{'='*50}")
    print("Pipeline multiagente completado!")

if __name__ == "__main__":
    print("=== Sistema Multiagente ===")
    print("3 agentes trabajando juntos: Planificador → Ejecutor → Revisor\n")
    
    tarea = input("Ingresá una tarea de programación: ")
    orquestador(tarea)