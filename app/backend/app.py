import requests
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask,jsonify,request

app = Flask(__name__)


@app.route("/")

def index():
    return 

@app.route("/api/pogoda")
def get_weather():
    id_str = request.args.get('id')

    if not id_str:
        return jsonify({"error": "Brak parametru id"}), 400

    try:
        loc_id = int(id_str)
    except ValueError:
        return jsonify({"error": "ID musi być liczbą"}), 400

    try:
        conn = psycopg2.connect(
            dbname="moja_db",
            port=5432,
            user="admin",
            password="haslo123",
            host="db"
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT latitude, longitude FROM pogoda WHERE id = %s", (loc_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()

        if not row:
            return jsonify({"error": "Nie znaleziono miasta o podanym ID"}), 404

        latitude = row['latitude']
        longitude = row['longitude']

    except Exception as e:
        print(f"Błąd bazy danych: {e}")
        return jsonify({"error": "Błąd połączenia z bazą"}), 500


    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        pogoda_data = response.json()  
        return jsonify(pogoda_data)
    else:
        print(f"Error API pogody: {response.status_code}")
        return jsonify({"error": "Błąd pobierania pogody"}), 500

@app.route("/api/lokalizacje")

def get_place():

    conn = psycopg2.connect(

    dbname="moja_db",
    port=5432,
    user="admin",
    password="haslo123",
    host="db"
    

    )

    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM pogoda")


    rows = cur.fetchall()            

    cur.close()                     
    conn.close()                     

    return jsonify(rows)


app.run(host="0.0.0.0" , port=5000)