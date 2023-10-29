from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import Var
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!11'


@app.route('/var', methods=['POST'])
def var():
    try:
        # Obtener los datos de la solicitud JSON
        data = request.get_json()

        # Comprobar si se proporciona un DataFrame
        if 'returns' in data:
            # Convertir el diccionario en un DataFrame de Pandas
            df_data = data['returns']
            df_returns = pd.DataFrame(df_data)

            # Comprobar si se proporcionan las dos cadenas de texto
            if 'portfolio_name' in data and 'alpha' in data  and 'time' in data:
                portfolio_name = data['portfolio_name']
                alpha = data['alpha']
                time = data['time']

            else:
                return jsonify({'error': 'Se esperan tres cadenas de texto: portfolio_name, time y alpha'}), 400
            
            if 'w' in data:
                # Convertir la lista de numpy.ndarray
                w_data = data['w']
                w = np.array(w_data)
            else:
                return jsonify({'error': 'Se espera un numpy.ndarray en el parámetro "w"'}), 400


            var = Var.VaRCalculation(time=time, alpha=alpha, name=portfolio_name).predict(df_returns, w)
            
            # Realizar alguna operación con el DataFrame y los datos
            resultado = {
                'resultado':var
            }

            return jsonify(resultado)
        else:
            return jsonify({'error': 'Se espera un DataFrame en el parámetro "returns"'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run()
