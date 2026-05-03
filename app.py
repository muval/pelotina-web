import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Configuras tu llave (API Key) de Google
genai.configure(api_key="TU_API_KEY_DE_GOOGLE")

# AQUÍ ES DONDE LE ENSEÑAS Y LO LIMITAS
instrucciones_sistema = """
Eres Pelotina, una asistente experta en [TU TEMA AQUÍ].
REGLAS ESTRICTAS:
1. Solo responde preguntas basadas en la siguiente información: [AQUÍ PEGAS TU CONOCIMIENTO].
2. Si el usuario pregunta algo que no está en esa información, responde: 'Lo siento, como Pelotina solo puedo ayudarte con temas de [TU TEMA]'.
3. Mantén siempre una personalidad alegre y usa emojis de tenis.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=instrucciones_sistema
)

@app.route('/chat', methods=['POST'])
def chat():
    datos = request.get_json()
    mensaje_usuario = datos.get('mensaje')
    
    # El modelo ya tiene las instrucciones de no salirse del tema
    respuesta = model.generate_content(mensaje_usuario)
    
    return jsonify({'respuesta': respuesta.text})
