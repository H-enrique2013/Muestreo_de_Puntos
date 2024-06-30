from flask import Flask, request, jsonify, send_from_directory,render_template
import script_mapa

app = Flask(__name__)

# Ruta principal que renderiza el template index.html
@app.route('/')
def index():
    json_data = {
        "Departamento": "AYACUCHO",
        "Provincia": "HUANTA",
        "Distrito": "IGUAIN",
        "DiccionarioPuntos": {
            "Punto 1": [-74.22177636647999, -12.990092382255995],
            "Punto 2": [-74.2169500514367, -12.96851318157424],
            "Punto 3": [-74.22122551977878, -12.983558205695665],
            "Punto 4": [-74.22264087758928, -12.980474113395678],
            "Punto 5": [-74.21986777821412, -12.975849290825769],
            "Punto 6": [-74.22186511449841, -12.974253850116721],
            "Punto 7": [-74.2184392018611, -12.99043919073571],
            "Punto 8": [-74.2202314606623, -12.968993352057701],
            "Punto 9": [-74.21809553370747, -12.976150035827443],
            "Punto 10": [-74.22237603049598, -12.989333931691757],
            "Punto 11": [-74.22196046558193, -12.996294387451847]
        }
    }
    return render_template('index.html', title='API de generación de Coordenadas está activa.', json_data=json_data)

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

