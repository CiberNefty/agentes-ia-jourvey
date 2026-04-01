import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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

def generar_reporte_ia(datos_candidatos):
    print("\n🧠 IA generando reporte...")
    
    texto_candidatos = "\n".join([
        f"- {c['nombre']}: puntaje {c['puntaje']}/10, skills: {c['skills']}"
        for c in datos_candidatos
    ])
    
    reporte = llamar_ollama([
        {
            "role": "system",
            "content": """Eres un experto en RRHH. 
Redactás reportes profesionales en español.
Usás un tono formal pero amigable."""
        },
        {
            "role": "user",
            "content": f"""Redactá un reporte ejecutivo breve sobre estos candidatos 
para una vacante de Python Developer:

{texto_candidatos}

Incluí: resumen general, top candidato recomendado y próximos pasos."""
        }
    ])
    return reporte

def enviar_email(destinatario, asunto, cuerpo, remitente, password):
    try:
        msg = MIMEMultipart()
        msg["From"] = remitente
        msg["To"] = destinatario
        msg["Subject"] = asunto
        msg.attach(MIMEText(cuerpo, "plain", "utf-8"))
        
        print(f"\n📧 Enviando email a {destinatario}...")
        
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(remitente, password)
            server.send_message(msg)
        
        print("✅ Email enviado!")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def agente_email():
    print("=== Agente Reportero por Email ===\n")
    
    # Datos de prueba — candidatos simulados
    candidatos = [
        {"nombre": "Ana García",    "puntaje": 9, "skills": "Python, FastAPI, Docker"},
        {"nombre": "Carlos López",  "puntaje": 6, "skills": "Python básico, Excel"},
        {"nombre": "María Torres",  "puntaje": 8, "skills": "Python, SQL, Git"},
        {"nombre": "Juan Pérez",    "puntaje": 4, "skills": "JavaScript, HTML"},
    ]
    
    print("📋 Candidatos a evaluar:")
    for c in candidatos:
        print(f"  - {c['nombre']}: {c['puntaje']}/10")
    
    # IA genera el reporte
    reporte = generar_reporte_ia(candidatos)
    print(f"\n📝 Reporte generado:\n{reporte}")
    
    # Preguntar si quiere enviar email
    print("\n" + "="*40)
    enviar = input("\n¿Querés enviar este reporte por email? (s/n): ")
    
    if enviar.lower() == "s":
        print("\nNecesito tus datos de Gmail:")
        print("(Tip: usá una contraseña de aplicación, no tu contraseña normal)")
        print("Guía: myaccount.google.com/apppasswords\n")
        
        remitente = input("Tu Gmail: ")
        password = input("Contraseña de aplicación: ")
        destinatario = input("Enviar reporte a (email): ")
        
        asunto = f"CVAgent — Reporte de candidatos {datetime.now().strftime('%d/%m/%Y')}"
        
        cuerpo = f"""Reporte generado por CVAgent
{'='*40}
Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}
Candidatos evaluados: {len(candidatos)}

RANKING:
{chr(10).join([f"{i+1}. {c['nombre']} — {c['puntaje']}/10" for i, c in enumerate(sorted(candidatos, key=lambda x: x['puntaje'], reverse=True))])}

REPORTE IA:
{reporte}

---
Enviado automáticamente por CVAgent
        """
        
        enviar_email(destinatario, asunto, cuerpo, remitente, password)
    else:
        print("\n✅ Reporte generado pero no enviado.")
        print("El reporte quedó guardado arriba en consola.")

if __name__ == "__main__":
    agente_email()