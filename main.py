from flask import Flask, request, jsonify, send_from_directory,render_template
import script_mapa


app = Flask(__name__, template_folder='templates')


# Ruta principal que renderiza el template index.html
@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/generate-map', methods=['GET', 'POST'])
def generate_map():
    if request.method=='POST':
        data = request.get_json()
        dep = data.get('Departamento')
        prov = data.get('Provincia')
        distr = data.get('Distrito')
        #dicPuntos = script_mapa.generar_puntos()
        dicPuntos=data.get('DiccionarioPuntos')
        script_mapa.GeneradorHmtl_mapa(dep, prov, distr, dicPuntos)
        # Verificar si el resultado es un JSON válido
        try:
            response_data = jsonify({"status": "success", "message": "Mapa generado exitosamente"})
            return response_data, 200
        except Exception as e:
            return jsonify({"error": f"Error al generar JSON: {str(e)}"}), 500
        
        
    else:
        #metodo=request.method
        return jsonify({"error":"Método no permitido"}),405
        #return jsonify({"error":metodo}),405

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

