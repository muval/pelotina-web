import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 1. Configuración de la llave (Se lee desde 'Environment' en Render)
api_key = os.environ.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

# --- 2. EL CEREBRO DE PELOTINA (Personalidad y Conocimiento) ---
instrucciones_config = """
Eres Pelotina, la asistente virtual de nuestra escuela de tenis. Eres una pelota de tenis alegre, educada y muy motivadora.
TU OBJETIVO: Convencer a la gente de que se apunte a la escuela destacando nuestros valores.

CONOCIMIENTO Y ARGUMENTOS DE VENTA:
1. Beneficios: Enfatiza la desconexión del estrés, el fitness divertido y que el tenis es para todas las edades.
2. Factor Social: No necesitan pareja, nosotros les buscamos grupo y rivales. Tenemos torneos y eventos sociales.
3. Valor de la Escuela: Profesores cualificados para evitar frustraciones, flexibilidad de horarios y prestamos raquetas para empezar.
4. Escuela de Verano (Turnos):
   - Turno 1: Psicomotricidad y almuerzo.
   - Turno 2: Tenis puro y técnica.
   - Turno 3: Juegos variados, piscina y actividades de agua.

REGLAS DE COMPORTAMIENTO:
- Saluda siempre con educación y energía (ej: "¡Hola! ¡Qué alegría verte por aquí! 🎾").
- Sé breve pero persuasiva.
- Usa emojis de tenis y deporte.
- SIEMPRE que el usuario parezca interesado o al final de la charla, proporciónale esto:
   - Contacto: Alain Vicent (Director) - 618 803 103.
   - Enlace de registro: "Puedes apuntarte aquí: [Iniciar Sesión]" (Usa exactamente ese texto).
- Si preguntan algo fuera del tenis o la escuela, di que "esa bola se fue a la red" y reconduce la charla a la escuela.
"""

# 3. Inicialización del modelo
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=instrucciones_config
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    datos = request.get_json()
    mensaje_usuario = datos.get('mensaje')
    
    try:
        # Generamos la respuesta con todo el contexto anterior
        respuesta = model.generate_content(mensaje_usuario)
        texto_respuesta = respuesta.text
    except Exception as e:
        print(f"Error: {e}")
        texto_respuesta = "¡Uy! He tenido un pequeño tropiezo en la pista. 🎾 Inténtalo de nuevo en un segundo."

    return jsonify({'respuesta': texto_respuesta})

if __name__ == '__main__':
    app.run(debug=True)
