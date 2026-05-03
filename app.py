from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# --- CONFIGURACIÓN ---
# Tu URL de Ngrok actualizada:
OLLAMA_URL = "https://coherent-facsimile-traverse.ngrok-free.dev/api/chat" 
MODELO = "phi3" # Asegúrate de que este es el que tienes en Ollama (puedes cambiarlo por llama3, etc.)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    datos = request.get_json()
    mensaje_usuario = datos.get('mensaje')
    
    payload = {
        "model": MODELO,
        "messages": [
            {"role": "system", "content": "Eres Pelotina, una asistente virtual alegre con forma de pelota de tenis chica. Eres simpática, usas emojis deportivos y respondes de forma corta."},
            {"role": "user", "content": mensaje_usuario}
        ],
        "stream": False
    }
    
    try:
        # Llamada a tu ordenador Ubuntu
        r = requests.post(OLLAMA_URL, json=payload, timeout=60)
        respuesta_ollama = r.json()['message']['content']
    except Exception as e:
        respuesta_ollama = "¡Ay! Mi cerebro está desconectado. 🎾💤 Revisa que Ngrok y Ollama estén activos en tu PC."

    return jsonify({'respuesta': respuesta_ollama})

if __name__ == '__main__':
    app.run(debug=True)
