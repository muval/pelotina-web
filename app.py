import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 1. Buscamos la llave secreta en la caja fuerte de Render
api_key = os.environ.get("GEMINI_API_KEY")

# Le damos la llave a Google
if api_key:
    genai.configure(api_key=api_key)

# --- 2. AQUÍ LE ENSEÑAMOS A PELOTINA ---
# Puedes cambiar este texto en el futuro para que aprenda cosas nuevas
informacion_pelotina = """
Eres Pelotina, una asistente virtual alegre con forma de pelota de tenis chica.
REGLAS:
1. Solo puedes hablar de tenis y de la información que yo te diga.
2. Si te preguntan sobre quién te creó, di que fuiste creada por Alain.
3. Si el usuario pregunta algo que no sabes o no tiene que ver con tenis, responde amablemente: "¡Uy! Esa bola se fue fuera. 🎾 Solo sé de tenis y de mi creador."
4. Mantén siempre una personalidad simpática, responde corto y usa emojis deportivos.
"""

# 3. Configuramos el cerebro de Gemini 1.5 Flash
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=informacion_pelotina
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    datos = request.get_json()
    mensaje_usuario = datos.get('mensaje')
    
    try:
        # Preguntamos a Gemini
        respuesta = model.generate_content(mensaje_usuario)
        texto_respuesta = respuesta.text
    except Exception as e:
        texto_respuesta = "¡Uy! Mi red se ha roto por un momento. 🎾🔌 Inténtalo de nuevo."

    return jsonify({'respuesta': texto_respuesta})

if __name__ == '__main__':
    app.run(debug=True)
