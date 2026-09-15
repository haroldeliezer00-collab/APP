from flask import Flask, jsonify, request, send_from_directory
import json
import os

app = Flask(__name__)

DATA_FILE = 'data_agencia.json'

DEFAULT_DATA = {
    "ag_pago_movil": [{"cedula": "18274410", "telefono": "04124489363", "saldo": 0}],
    "ag_transferencia": [
        {"terminacion": "7201", "titular": "Harold Eliezer Galea Sanchez", "saldo": 0},
        {"terminacion": "0163", "titular": "Harold Eliezer Galea Sanchez", "saldo": 0}
    ],
    "ag_clientes": [{"nombre": "Cliente General", "saldo": 0}],
    "ag_referencias_usadas": [],
    "ag_sistemas": [
        {"id": 'maxplay', "nombre": 'Maxplay', "porcentaje": 14},
        {"id": 'matrix', "nombre": 'Matrix Comp', "porcentaje": 14},
        {"id": 'srq', "nombre": 'SRQ Polla', "porcentaje": 14},
        {"id": 'atenas', "nombre": 'Atenas', "porcentaje": 12}
    ],
    "ag_sistemas_datos": {}
}

dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
default_datos = {}
for dia in dias:
    default_datos[dia] = {}
    for sys in DEFAULT_DATA["ag_sistemas"]:
        default_datos[dia][sys['id']] = {"ventas": 0, "premios": 0, "comision": 0}
DEFAULT_DATA["ag_sistemas_datos"] = default_datos

def cargar_datos():
    if not os.path.exists(DATA_FILE):
        guardar_datos(DEFAULT_DATA)
        return DEFAULT_DATA
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return DEFAULT_DATA

def guardar_datos(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(cargar_datos())

@app.route('/api/data', methods=['POST'])
def update_data():
    new_data = request.json
    if new_data:
        guardar_datos(new_data)
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "No data provided"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
