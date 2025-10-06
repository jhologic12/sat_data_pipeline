from flask import Flask, render_template, request, jsonify
import os, json
from shapely.geometry import shape
from earthaccess import Auth, DataGranules , search_data
from utils.aoi_utils import get_bbox_from_geojson
from config import AOI_PATH, MODIS_PRODUCT, MAX_GRANULES
from utils.geo_utils import get_bbox_from_geojson , validate_aoi
from utils.granules_utils import format_granule

# from auth_utils import login_earthdata
try:
    from utils.auth_utils import login_earthdata

except ImportError:
    # Fallback: define a dummy login_earthdata or handle the error
    def login_earthdata():
        raise ImportError("auth_utils module not found. Please ensure auth_utils.py exists in your project directory.")

from config import AOI_PATH, EARTHDATA_USERNAME, MODIS_PRODUCT

app = Flask(__name__)
print("✅ Ejecutando app.py desde:", __file__)

AOI_PATH = "../config/aoi.geojson"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_aoi", methods=["GET"])
def get_aoi():
    if os.path.exists(AOI_PATH):
        with open(AOI_PATH, "r", encoding="utf-8") as f:
            geojson_data = json.load(f)
        return jsonify(geojson_data)
    return jsonify({})

def validate_aoi_structure(geojson_data):
    try:
        geom = shape(geojson_data["geometry"])
        if not geom.is_valid:
            return False, "Geometría inválida"
        if geom.geom_type != "Polygon":
            return False, f"Tipo de geometría no soportado: {geom.geom_type}"
        if geom.area < 0.0001:
            return False, "Área demasiado pequeña para consulta satelital"
        return True, "AOI válido para MODIS/SMAP"
    except Exception as e:
        return False, f"Error en estructura: {str(e)}"

import os

@app.route("/save_aoi", methods=["POST"])
def save_aoi():
    geojson_data = request.get_json()
    is_valid, validation_msg = validate_aoi_structure(geojson_data)

    if not is_valid:
        return jsonify({
            "status": "error",
            "message": validation_msg
        })

    #  Crear el directorio si no existe
    os.makedirs(os.path.dirname(AOI_PATH), exist_ok=True)

    try:
        with open(AOI_PATH, "w", encoding="utf-8") as f:
            json.dump(geojson_data, f)
        return jsonify({
            "status": "success",
            "message": f"{validation_msg}. AOI guardado correctamente."
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error al guardar el AOI: {str(e)}"
        })

from flask import request

import traceback
from earthaccess import DataGranules

@app.route("/get_granules")
def get_granules():
    try:
        print(" Iniciando autenticación...")
        auth = login_earthdata()
        if not auth.authenticated:
            raise RuntimeError("No se pudo autenticar con Earthdata.")

        print(" Validando AOI...")
        validate_aoi(AOI_PATH)

        start_date = request.args.get("start", "2023-01-01")
        end_date = request.args.get("end", "2023-01-31")

        west, south, east, north = get_bbox_from_geojson(AOI_PATH)

        # Crear objeto DataGranules y aplicar filtros
        granules = DataGranules(auth)
        granules.temporal(start_date, end_date)
        granules.bounding_box(south, west, north, east)
        granules.short_name(MODIS_PRODUCT)

        results = granules.get()

        ## Debug: Mostrar algunos granules recibidos
        print("🔍 Granules recibidos:")
        for g in results[:3]:  # Solo los primeros 3 para no saturar la consola
         print(g.__dict__)  # Muestra todos los atributos internos del objeto

        output = [format_granule(granule) for granule in results[:MAX_GRANULES]]



        return jsonify({
            "status": "success",
            "granules": output,
            "count": len(output)
        })

    except Exception as e:
        print(" Error detectado:")
        traceback.print_exc()
        return jsonify({
            "status": "error",
            "message": f"Error interno: {str(e)}"
        })






if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
