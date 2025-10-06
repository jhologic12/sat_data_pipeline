import earthaccess
import logging
import os
from datetime import datetime

# 📁 Configuración de carpetas
DATA_DIR = "../data/smap/"
LOG_FILE = "../logs/acquisition.log"
os.makedirs(DATA_DIR, exist_ok=True)

# 📝 Configurar logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

# 🌍 Área de interés (Colombia)
BBOX = [-79.0, -4.0, -66.0, 13.0]  # [lon_min, lat_min, lon_max, lat_max]

# 📅 Rango de fechas
START_DATE = "2025-09-01"
END_DATE = "2025-10-01"

# 📦 Producto SMAP L3 (humedad del suelo)
PRODUCT = "SPL3SMP_E"

def main():
    try:
        # 🔐 Autenticación interactiva
        earthaccess.login(strategy="interactive")

        # 🔍 Buscar granules
        results = earthaccess.search_data(
            short_name=PRODUCT,
            bounding_box=BBOX,
            temporal=(START_DATE, END_DATE),
            cloud_hosted=True,
            granule=True
        )

        if not results:
            logging.warning(f"[{datetime.now()}] No se encontraron granules para {PRODUCT} en el rango especificado.")
            return

        # 📥 Descargar
        earthaccess.download(results, DATA_DIR)

        # 🧾 Registrar evento
        logging.info(f"[{datetime.now()}] Descargados {len(results)} granules SMAP ({PRODUCT}) entre {START_DATE} y {END_DATE} en {DATA_DIR}")

    except Exception as e:
        logging.error(f"[{datetime.now()}] Error durante la descarga: {str(e)}")

if __name__ == "__main__":
    main()
