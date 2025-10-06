from flask import Flask, render_template, request, jsonify
import os, json
from shapely.geometry import shape
from earthaccess import Auth, DataGranules
# from auth_utils import login_earthdata
try:
    from auth_utils import login_earthdata
except ImportError:
    # Fallback: define a dummy login_earthdata or handle the error
    def login_earthdata():
        raise ImportError("auth_utils module not found. Please ensure auth_utils.py exists in your project directory.")

from config import AOI_PATH, EARTHDATA_USERNAME, MODIS_PRODUCT

app = Flask(__name__)
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

@app.route("/save_aoi", methods=["POST"])
def save_aoi():
    geojson_data = request.get_json()
    is_valid, validation_msg = validate_aoi_structure(geojson_data)

    if not is_valid:
        return jsonify({
            "status": "error",
            "message": validation_msg
        })

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

@app.route("/get_granules", methods=["GET"])
def get_granules():
    try:
        login_earthdata()
        granules = DataGranules().short_name("MOD11A1").bbox_from_file(AOI_PATH).get()

        if not granules:
            return jsonify({
                "status": "error",
                "message": "No se encontraron granules para el AOI actual."
            })

        results = []
        for g in granules[:10]:
            results.append({
                "title": g.title,
                "date": g.temporal,
                "url": g.download_links()[0] if g.download_links() else "Sin enlace"
            })

        return jsonify({
            "status": "success",
            "granules": results,
            "count": len(results)
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error interno: {str(e)}"
        })

if __name__ == "__main__":
    app.run(debug=True)
