from flask import Flask, request, jsonify, send_from_directory, render_template
import script_mapa
import os
import time
import threading

app = Flask(__name__, template_folder='templates')

def delete_file(filepath):
    time.sleep(30)
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
        except Exception as e:
            print(f"Error al eliminar el archivo: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')
#Método POST
@app.route('/generatemap-html', methods=['POST'])
def generatemap_html():
    data = request.get_json()
    dep = data.get('Departamento')
    prov = data.get('Provincia')
    distr = data.get('Distrito')
    sect = data.get('Sector')
    dicPuntos = data.get('DiccionarioPuntos')

    filepath = None
    #kml_filepath=None
    try:
        (html_filepath,kml_filepath)= script_mapa.GeneradorHmtl_mapa(dep, prov, distr,sect, dicPuntos)
        filename = os.path.basename(html_filepath)
        directory = os.path.dirname(html_filepath)
        response = send_from_directory(directory=directory, path=filename)
        threading.Thread(target=delete_file, args=(html_filepath,)).start()
        threading.Thread(target=delete_file, args=(kml_filepath,)).start()
        return response, 200
    except Exception as e:
        # Imprimir el tipo de excepción y el mensaje para depuración
        print(f"Tipo de error: {type(e).__name__}")
        print(f"Mensaje de error: {str(e)}")
        # Convertir la excepción en una cadena para asegurar que sea serializable a JSON
        return jsonify({"error": f"Error al generar el mapa: {str(e)}"}), 500
    

#Método POST
@app.route('/generatemap-kml', methods=['POST'])
def generatemap_kml():
    
    data = request.get_json()
    dep = data.get('Departamento')
    prov = data.get('Provincia')
    distr = data.get('Distrito')
    sect = data.get('Sector')
    dicPuntos = data.get('DiccionarioPuntos')

    kml_filepath=None
    try:
        (html_filepath,kml_filepath) = script_mapa.GeneradorHmtl_mapa(dep, prov, distr,sect, dicPuntos)
        filename = os.path.basename(kml_filepath)
        directory = os.path.dirname(kml_filepath)
        response = send_from_directory(directory=directory, path=filename)
        threading.Thread(target=delete_file, args=(kml_filepath,)).start()
        threading.Thread(target=delete_file, args=(html_filepath,)).start()
        return response, 200
    except Exception as e:
        # Imprimir el tipo de excepción y el mensaje para depuración
        print(f"Tipo de error: {type(e).__name__}")
        print(f"Mensaje de error: {str(e)}")
        # Convertir la excepción en una cadena para asegurar que sea serializable a JSON
        return jsonify({"error": f"Error al generar el mapa: {str(e)}"}), 500
    



@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

