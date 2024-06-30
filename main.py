from flask import Flask, request, jsonify, send_from_directory,render_template
import script_mapa
import os

app = Flask(__name__, template_folder='templates')


# Ruta principal que renderiza el template index.html
@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/generate-map', methods=['POST'])
def generate_map():
    if request.method=='GET':
        data = request.get_json()
        dep = data.get('Departamento')
        prov = data.get('Provincia')
        distr = data.get('Distrito')
        dicPuntos=data.get('DiccionarioPuntos')

        try:
            filepath = script_mapa.GeneradorHmtl_mapa(dep, prov, distr, dicPuntos)
            # Devolver el archivo como respuesta
            return send_from_directory(directory='static', filename=filepath.split('/')[-1]), 200
        except Exception as e:
            return jsonify({"error": f"Error al generar el mapa: {str(e)}"}), 500
        finally:
            # Eliminar el archivo después de enviar la respuesta
            if os.path.exists(filepath):
                os.remove(filepath)
 
    else:
        #metodo=request.method
        return jsonify({"error":"Método no permitido"}),405
        #return jsonify({"error":metodo}),405

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

