from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# --- CONFIGURACIÓN ---
# Tu URL de Ngrok (asegúrate de que coincida con la que tienes abierta en Ubuntu)
OLLAMA_URL = "https://coherent-facsimile-traverse.ngrok-free.dev/api/chat" 
MODELO = "phi3" 

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    datos = request.get_json()
    mensaje_usuario = datos.get('mensaje')
    
    # Esta es la CABECERA para evitar el error 403 de Ngrok
    headers = {
        "ngrok-skip-browser-warning": "true"
    }
    
    payload = {
        "model": MODELO,
        "messages": [
            {"role": "system", "content": "Eres Pelotina, una asistente virtual alegre con forma de pelota de tenis chica. Eres simpática, usas emojis deportivos y respondes de forma corta."},
            {"role": "user", "content": mensaje_usuario}
        ],
        "stream": False
    }
    
    try:
        # Aquí añadimos 'headers=headers' para que Ngrok nos deje pasar
        r = requests.post(OLLAMA_URL, json=payload, headers=headers, timeout=60)
        respuesta_ollama = r.json()['message']['content']
    except Exception as e:
        # Si hay error, Pelotina avisará
        respuesta_ollama = "¡Ay! Mi cerebro está desconectado. 🎾💤 Revisa que Ngrok y Ollama estén activos en tu Ubuntu."

    return jsonify({'respuesta': respuesta_ollama})

if __name__ == '__main__':
    app.run(debug=True)
