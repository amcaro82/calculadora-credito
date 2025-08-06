from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 👈 Habilita CORS

@app.route('/calcular-cuota', methods=['POST'])
def calcular_cuota():
    try:
        data = request.json
        monto = float(data.get('monto', 0))
        ingreso = float(data.get('ingreso', 0))
        plazo = int(data.get('plazo', 12))
        tasa = float(data.get('tasa', 0.02))

        if monto <= 0 or ingreso <= 0 or plazo <= 0 or tasa <= 0:
            return jsonify({'error': 'Todos los valores deben ser mayores que cero'}), 400

        cuota = (monto * tasa) / (1 - (1 + tasa) ** -plazo)
        porcentaje_ingreso = cuota / ingreso

        return jsonify({
            'cuota_mensual': round(cuota, 2),
            'porcentaje_ingreso': round(porcentaje_ingreso * 100, 2),
            'aprobado': porcentaje_ingreso <= 0.4
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

@app.route("/", methods=["GET", "HEAD"])
def home():
    return "API de crédito operativa", 200
