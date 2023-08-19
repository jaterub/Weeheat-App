import requests
import pandas as pd
from datetime import datetime, timedelta
from flask import Flask, jsonify
import io

def obtener_agenda_activades_eventos_100dias():
    url = "https://datos.madrid.es/egob/catalogo/300107-0-agenda-actividades-eventos.csv"
    
    try:
        response = requests.get(url)
        response.raise_for_status()

        return response.content

    except requests.exceptions.RequestException as e:
        print("Error al obtener los eventos culturales:", e)
        return None
    
def clean_num_instalacion(num_instalacion):
    if pd.notnull(num_instalacion):
        try:
            return str(int(num_instalacion))
        except ValueError:
            return "N/A o N/D"
    return "N/A o N/D"

app = Flask(__name__)

@app.route('/eventos', methods=['GET'])
def obtener_eventos():
    fecha_actual = datetime.now()
    fecha_actual_str = fecha_actual.strftime("%Y-%m-%d")
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
        df["TIPO"] = df["TIPO"].str.extract(r'\/([^/]+)$')
        df["TIPO"] = df["TIPO"].fillna("No disponible")
        df["NUM-INSTALACION"] = df["NUM-INSTALACION"].apply(clean_num_instalacion)
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
    app.run(debug=True)
