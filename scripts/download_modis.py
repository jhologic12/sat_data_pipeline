from modis_tools.auth import ModisSession
from modis_tools.resources import CollectionApi, GranuleApi
from modis_tools.granule_handler import GranuleHandler
import logging

# 🔐 Credenciales Earthdata
USERNAME = "TU_USUARIO"
PASSWORD = "TU_CONTRASEÑA"

# 🌍 Área de interés (ej. Colombia)
BBOX = [-79.0, -4.0, -66.0, 13.0]  # [lon_min, lat_min, lon_max, lat_max]

# 📅 Rango de fechas
START_DATE = "2025-09-01"
END_DATE = "2025-10-01"

# 📦 Producto MODIS (ej. NDVI)
PRODUCT = "MOD13A1"
VERSION = "061"

# 📝 Logging
logging.basicConfig(filename="../logs/acquisition.log", level=logging.INFO)

def main():
    session = ModisSession(username=USERNAME, password=PASSWORD)
    collection_client = CollectionApi(session=session)
    collections = collection_client.query(short_name=PRODUCT, version=VERSION)

    if not collections:
        logging.error("No se encontró la colección especificada.")
        return

    granule_client = GranuleApi.from_collection(collections[0], session=session)
    granules = granule_client.query(start_date=START_DATE, end_date=END_DATE, bounding_box=BBOX)

    if not granules:
        logging.warning("No se encontraron granules en el rango especificado.")
        return

    GranuleHandler.download_from_granules(granules, session)
    logging.info(f"Descargados {len(granules)} granules MODIS para {PRODUCT} entre {START_DATE} y {END_DATE}")

if __name__ == "__main__":
    main()
