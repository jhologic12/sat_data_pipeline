import os
import json
import geojson_validator
from datetime import datetime
import logging

#  Rutas
AOI_PATH = "config/aoi.geojson"
LOG_FILE = "logs/acquisition.log"

# 📝 Configurar logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

def validate_geojson(path):
    if not os.path.exists(path):
        logging.error(f"[{datetime.now()}]  Archivo no encontrado: {path}")
        return False

    try:
        with open(path, "r", encoding="utf-8") as f:
            geojson = json.load(f)
    except Exception as e:
        logging.error(f"[{datetime.now()}]  Error al leer el archivo: {e}")
        return False

    #  Validar estructura
    structure_issues = geojson_validator.validate_structure(geojson)
    if structure_issues:
        logging.error(f"[{datetime.now()}]  Estructura inválida: {structure_issues}")
        return False

    #  Validar geometrías
    geometry_issues = geojson_validator.validate_geometries(geojson)
    if geometry_issues.get("invalid") or geometry_issues.get("problematic"):
        logging.warning(f"[{datetime.now()}]  Geometrías con problemas: {geometry_issues}")
        return False

    logging.info(f"[{datetime.now()}]  AOI válido y listo para usar: {path}")
    return True

if __name__ == "__main__":
    if validate_geojson(AOI_PATH):
        print("AOI válido. Puedes continuar con los flujos MODIS/SMAP.")
    else:
        print(" AOI inválido. Revisa el log para más detalles.")
