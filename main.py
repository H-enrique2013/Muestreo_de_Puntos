from flask import Flask, request, jsonify, send_from_directory
import script_mapa

app = Flask(__name__)

@app.route('/')
def index():
    return "API de generación de mapas está activa."

@app.route('/generate-map', methods=['GET', 'POST'])
def generate_map():
    if request.method=='POST':
        data = request.get_json()
        dep = data.get('dep')
        prov = data.get('prov')
        distr = data.get('distr')
        dicPuntos = script_mapa.generar_puntos()
        script_mapa.GeneradorHmtl_mapa(dep, prov, distr, dicPuntos)
        return jsonify({"status": "success", "message": "Mapa generado exitosamente"}),200
    else:
        return jsonify({"error":"Método no permitido"}),405

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
