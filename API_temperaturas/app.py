from flask import Flask, request, jsonify  # Importamos jsonify para manejar el JSON
from datetime import datetime, timedelta
from flask_cors import CORS, cross_origin
import os
import zipfile
import requests
from api_key import *
import pickle
import io
import pandas as pd

def obtener_agenda_activades_eventos_100dias():
    url = "https://datos.madrid.es/egob/catalogo/300107-0-agenda-actividades-eventos.csv"

    try:
        response = requests.get(url)
        response.raise_for_status()

        return response.content

    except requests.exceptions.RequestException as e:
        print("Error al obtener los eventos culturales:", e)
        return None

os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
CORS(app)
app.config['DEBUG'] = True
 # CORS Headers
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route("/", methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def hello():
    return "Bienvenido a la API de temperaturas"

@app.route('/v1/predict', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def predict():

    zip_file_path = "./model/model_temp.zip"
    model_file_path = "model_temp.pkl"

    with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
        with zip_file.open(model_file_path) as model_file:
            model = pickle.load(model_file)

    ano = request.args.get('ano', None)
    mes = request.args.get('mes', None)
    dia = request.args.get('dia', None)
    hora = request.args.get('hora', None)

    if ano is None or mes is None or dia is None or hora is None:
        return jsonify({"error": "Faltan argumentos en la llamada"})
    else:
        prediccion = model.predict([[ano, mes, dia, hora]])
        temperatura_prediccion = round(prediccion[0], 2)
        return jsonify({"Prediccion_temperatura_Madrid": temperatura_prediccion})

@app.route('/v1/temp_actual', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def temp():
    city = "Madrid"
    url = f"https://api.openweathermap.org/data/2.5/weather?q=Madrid,es&appid={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()
        temperature_kelvin = weather_data["main"]["temp"]
        temperature_celsius = temperature_kelvin - 273.15  # Convertir a Celsius
        temperature_data = {
            "city": city,
            "temperature_celsius": round(temperature_celsius,2)
        }
        return jsonify(temperature_data)  # Devolver la información en formato JSON
    else:
        error_data = {
            "error": "Error al obtener los datos meteorológicos."
        }
        return jsonify(error_data)  # Devolver mensaje de error en formato JSON

@app.route('/v1/eventos', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def obtener_eventos():
    fecha_actual = datetime.now()
    # fecha_actual_str = fecha_actual.strftime("%Y-%m-%d")
    fecha_maxima = fecha_actual + timedelta(days=10)

    contenido_csv = obtener_agenda_activades_eventos_100dias()

    if contenido_csv:
        df = pd.read_csv(io.BytesIO(contenido_csv), sep=";", encoding="latin-1")
        df.dropna(subset=["LONGITUD"], inplace=True)
        df = df.drop(["PRECIO", "Unnamed: 29", "AUDIENCIA", "LARGA-DURACION", "DESCRIPCION", "TITULO-ACTIVIDAD", "URL-ACTIVIDAD",
                      "CODIGO-POSTAL-INSTALACION", "URL-INSTALACION", "ACCESIBILIDAD-INSTALACION", "DIAS-EXCLUIDOS", "GRATUITO",
                      "COORDENADA-X", "COORDENADA-Y"," ID-EVENTO"],
                     axis=1)
        df["DIAS-SEMANA"].fillna("No disponible", inplace=True)
        df["HORA"].fillna("No disponible", inplace=True)
        df["DISTRITO-INSTALACION"].fillna("No disponible", inplace=True)
        df["TIPO"].fillna("No disponible", inplace=True)
        df["NOMBRE-INSTALACION"].fillna("No disponible", inplace=True)
        df["CLASE-VIAL-INSTALACION"].fillna("No disponible", inplace=True)
        df["NOMBRE-VIA-INSTALACION"].fillna("No disponible", inplace=True)
        df["BARRIO-INSTALACION"].fillna("No disponible", inplace=True)
        df["NUM-INSTALACION"].fillna("N/A o N/D", inplace=True)
        df['NUM-INSTALACION'] = pd.to_numeric(df['NUM-INSTALACION'], errors='coerce')
        df['NUM-INSTALACION'] = df['NUM-INSTALACION'].astype(pd.Int64Dtype(), errors='ignore')
        df["TIPO"] = df["TIPO"].str.extract(r'\/([^/]+)$')
        df["TIPO"] = df["TIPO"].fillna("No disponible")
        df["NUM-INSTALACION"] = df["NUM-INSTALACION"].astype(str)
        df["DIRECCION"] = df["CLASE-VIAL-INSTALACION"] + " " + df["NOMBRE-VIA-INSTALACION"] + " " + df["NUM-INSTALACION"]
        df = df.drop(["CLASE-VIAL-INSTALACION","NOMBRE-VIA-INSTALACION","NUM-INSTALACION","NOMBRE-INSTALACION","DISTRITO-INSTALACION",
                      "BARRIO-INSTALACION"],axis=1)
        tipo_column = df.pop("TIPO")
        df.insert(1, "TIPO", tipo_column)
        direccion_column = df.pop("DIRECCION")
        df.insert(6, "DIRECCION", direccion_column)

        # Convertir las columnas de fecha a objetos datetime
        df["FECHA"] = pd.to_datetime(df["FECHA"])
        df["FECHA-FIN"] = pd.to_datetime(df["FECHA-FIN"])

        # Realizar las comparaciones
        df_filtrado = df[((df["FECHA"] <= fecha_actual) & (df["FECHA-FIN"] >= fecha_actual)) | (df["FECHA"] <= fecha_maxima)]

        return jsonify(df_filtrado.to_dict(orient='records'))

    return jsonify({"error": "No se pudo obtener la agenda de eventos."}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)