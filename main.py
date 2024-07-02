from flask import Flask, request, jsonify, send_from_directory, render_template
import script_mapa
import os
import time
import threading


app = Flask(__name__, template_folder='templates')


def delete_file(filepath):
    time.sleep(60)  # Esperar 5 segundos
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
        except Exception as e:
            print(f"Error al eliminar el archivo: {str(e)}")


# Ruta principal que renderiza el template index.html
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-map', methods=['POST'])
def generate_map():
    if request.method == 'POST':
        data = request.get_json()
        dep = data.get('Departamento')
        prov = data.get('Provincia')
        distr = data.get('Distrito')
        dicPuntos = data.get('DiccionarioPuntos')

        filepath = None
        try:
            filepath = script_mapa.GeneradorHmtl_mapa(dep, prov, distr, dicPuntos)
            # Devolver el archivo como respuesta
            filename = os.path.basename(filepath)
            directory = os.path.dirname(filepath)
            response = send_from_directory(directory=directory, path=filename)
            # Iniciar un hilo para eliminar el archivo después de enviar la respuesta
            threading.Thread(target=delete_file, args=(filepath,)).start()
            return response, 200
        except Exception as e:
            print(f"Error: {str(e)}")  # Agregar esto para imprimir el error en la consola
            return jsonify({"error": f"Error al generar el mapa: {str(e)}"}), 500

    else:
        return jsonify({"error": "Método no permitido"}), 405

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
