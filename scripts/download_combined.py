import geopandas as gpd
import logging
from datetime import datetime
import os
import earthaccess
from modis_tools.auth import ModisSession
from modis_tools.resources import CollectionApi, GranuleApi
from modis_tools.granule_handler import GranuleHandler
import json
import geojson_validator

# 📁 Configuración
AOI_PATH = "config/aoi.geojson"
LOG_FILE = "logs/acquisition.log"
MODIS_DIR = "data/modis/"
SMAP_DIR = "data/smap/"
os.makedirs(MODIS_DIR, exist_ok=True)
os.makedirs(SMAP_DIR, exist_ok=True)

# 📝 Logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

# 📅 Fechas
START_DATE = "2025-09-01"
END_DATE = "2025-10-01"

# 📦 Productos
MODIS_PRODUCT = "MOD13A1"
MODIS_VERSION = "061"
SMAP_PRODUCT = "SPL3SMP_E"

def validate_geojson(path):
    if not os.path.exists(path):
        logging.error(f"[{datetime.now()}] ❌ Archivo no encontrado: {path}")
        return False
    try:
        with open(path, "r", encoding="utf-8") as f:
            geojson = json.load(f)
    except Exception as e:
        logging.error(f"[{datetime.now()}] ❌ Error al leer el archivo: {e}")
        return False

    structure_issues = geojson_validator.validate_structure(geojson)
    geometry_issues = geojson_validator.validate_geometries(geojson)

    if structure_issues or geometry_issues.get("invalid") or geometry_issues.get("problematic"):
        logging.warning(f"[{datetime.now()}] ⚠️ AOI inválido o problemático.")
        return False

    logging.info(f"[{datetime.now()}] ✅ AOI válido: {path}")
    return True

def get_bbox_from_geojson(path):
    gdf = gpd.read_file(path)
    bounds = gdf.total_bounds  # [minx, miny, maxx, maxy]
    return bounds.tolist()

def download_modis(bbox, username, password):
    try:
        session = ModisSession(username=username, password=password)
        collection_client = CollectionApi(session=session)
        collections = collection_client.query(short_name=MODIS_PRODUCT, version=MODIS_VERSION)

        if not collections:
            logging.warning(f"[{datetime.now()}] No se encontró la colección MODIS.")
            return

        granule_client = GranuleApi.from_collection(collections[0], session=session)
        granules = granule_client.query(start_date=START_DATE, end_date=END_DATE, bounding_box=bbox)

        if not granules:
            logging.warning(f"[{datetime.now()}] No se encontraron granules MODIS.")
            return

        GranuleHandler.download_from_granules(granules, session)
        logging.info(f"[{datetime.now()}] MODIS: {len(granules)} granules descargados.")
    except Exception as e:
        logging.error(f"[{datetime.now()}] Error MODIS: {str(e)}")

def download_smap(bbox):
    try:
        earthaccess.login(strategy="interactive")
        results = earthaccess.search_data(
            short_name=SMAP_PRODUCT,
            bounding_box=bbox,
            temporal=(START_DATE, END_DATE),
            cloud_hosted=True,
            granule=True
        )

        if not results:
            logging.warning(f"[{datetime.now()}] No se encontraron granules SMAP.")
            return

        earthaccess.download(results, SMAP_DIR)
        logging.info(f"[{datetime.now()}] SMAP: {len(results)} granules descargados.")
    except Exception as e:
        logging.error(f"[{datetime.now()}] Error SMAP: {str(e)}")

def main():
    if not validate_geojson(AOI_PATH):
        print("❌ AOI inválido. Revisa el log para más detalles.")
        return

    bbox = get_bbox_from_geojson(AOI_PATH)
    logging.info(f"[{datetime.now()}] AOI cargado: {bbox}")

    # 🔐 Reemplaza con tus credenciales Earthdata
    modis_user = "TU_USUARIO"
    modis_pass = "TU_CONTRASEÑA"

    download_modis(bbox, modis_user, modis_pass)
    download_smap(bbox)

if __name__ == "__main__":
    main()
