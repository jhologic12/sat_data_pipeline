# flask_app/utils/verify_env.py

import os
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shapely.geometry import shape
from config import AOI_PATH, EARTHDATA_USERNAME, EARTHDATA_PASSWORD

def check_env():
    print(" Verificando entorno...")

    # Verificar credenciales
    if not EARTHDATA_USERNAME or not EARTHDATA_PASSWORD:
        print(" Credenciales Earthdata no encontradas en .env")
        return 1
    print(" Credenciales Earthdata cargadas")

    # Verificar AOI
    if not os.path.exists(AOI_PATH):
        print(f" AOI no encontrado en: {AOI_PATH}")
        return 1
    print(f" AOI encontrado en: {AOI_PATH}")

    # Validar estructura GeoJSON
    try:
        with open(AOI_PATH, "r", encoding="utf-8") as f:
            geojson_data = json.load(f)
            geom = shape(geojson_data["geometry"])
            if not geom.is_valid:
                print(" Geometría inválida")
                return 1
            print(f" Geometría válida: {geom.geom_type}, área: {geom.area:.6f}")
    except Exception as e:
        print(f" Error al validar AOI: {str(e)}")
        return 1

    print(" Entorno verificado correctamente")
    return 0

if __name__ == "__main__":
    exit(check_env())


print(f"AOI_PATH resuelto: {AOI_PATH}")


