import os
import geopandas as gpd
from earthaccess import Auth, DataCollections, DataGranules
from config import AOI_PATH, EARTHDATA_USERNAME, EARTHDATA_PASSWORD, MODIS_PRODUCT, MAX_GRANULES
import logging

# Configurar logging centralizado
LOG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "logs", "modis_download.log"))
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def authenticate():
    try:
        Auth().login(strategy="environment")
        logging.info("Autenticación Earthdata exitosa.")
    except Exception as e:
        logging.error(f"Error de autenticación: {e}")
        raise

def get_bbox_from_aoi(aoi_path):
    try:
        aoi = gpd.read_file(aoi_path)
        bbox = aoi.total_bounds  # [minx, miny, maxx, maxy]
        logging.info(f"AOI cargado correctamente: {aoi_path}")
        return bbox
    except Exception as e:
        logging.error(f"Error al cargar AOI: {e}")
        raise

def get_collection(short_name):
    try:
        collection = DataCollections().search_short_name(short_name)[0]
        logging.info(f"Colección MODIS encontrada: {short_name}")
        return collection
    except Exception as e:
        logging.error(f"No se encontró la colección: {short_name}")
        raise

def download_granules(short_name, bbox, limit, download_dir):
    os.makedirs(download_dir, exist_ok=True)
    granules = DataGranules().search(
        short_name=short_name,
        bounding_box=bbox,
        cloud_hosted=True,
        limit=limit
    )

    for granule in granules:
        filename = os.path.basename(granule.data_links()[0])
        filepath = os.path.join(download_dir, filename)

        if os.path.exists(filepath):
            logging.info(f"Granule ya existe, omitido: {filename}")
            continue

        try:
            granule.download(download_dir)
            logging.info(f"Granule descargado: {filename}")
        except Exception as e:
            logging.error(f"Error al descargar {filename}: {e}")

def run_modis_download():
    authenticate()
    bbox = get_bbox_from_aoi(AOI_PATH)
    get_collection(MODIS_PRODUCT)
    download_dir = os.path.join("data", "downloads")
    download_granules(MODIS_PRODUCT, bbox, MAX_GRANULES, download_dir)
