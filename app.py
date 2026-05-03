from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Esta ruta carga tu página principal
@app.route('/')
def home():
    return render_template('index.html')

# Esta ruta recibe el mensaje del chat y devuelve una respuesta
@app.route('/chat', methods=['POST'])
def chat():
    datos = request.get_json()
    mensaje_usuario = datos.get('mensaje')
    
    # Aquí es donde conectaremos la IA más adelante. 
    # Por ahora, Pelotina repite como un loro para probar:
    respuesta_pelotina = f"¡Guau! Me has dicho: '{mensaje_usuario}'. Aún estoy aprendiendo, ¡pronto tendré mi cerebro IA conectado!"
    
    return jsonify({'respuesta': respuesta_pelotina})

if __name__ == '__main__':
    app.run(debug=True)
