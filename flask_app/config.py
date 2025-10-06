import os
from dotenv import load_dotenv

#  Cargar variables desde .env
load_dotenv()

#  Exportar credenciales al entorno global para earthaccess
os.environ["EARTHDATA_USERNAME"] = os.getenv("EARTHDATA_USERNAME", "")
os.environ["EARTHDATA_PASSWORD"] = os.getenv("EARTHDATA_PASSWORD", "")

#  Rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
AOI_PATH = os.path.join(PROJECT_ROOT, "config", "aoi.geojson")

#  Credenciales Earthdata (también disponibles como variables locales si las necesitas)
EARTHDATA_USERNAME = os.getenv("EARTHDATA_USERNAME")
EARTHDATA_PASSWORD = os.getenv("EARTHDATA_PASSWORD")

#  Configuración general
MAX_GRANULES = int(os.getenv("MAX_GRANULES", 10))
MODIS_PRODUCT = os.getenv("MODIS_PRODUCT", "MOD11A1")
