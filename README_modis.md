
#  Módulo de descarga MODIS (`modis_downloader.py`)

##  Ubicación / Location

flask_app/modules/modis_downloader.py

Código

---

##  Descripción / 🇺🇸 Description

Este módulo permite descargar datos satelitales MODIS desde Earthdata utilizando un Área de Interés (AOI) en formato GeoJSON. Incluye autenticación, búsqueda de granules, validación de duplicados y registro centralizado de eventos.

This module downloads MODIS satellite data from Earthdata using a GeoJSON Area of Interest (AOI). It includes authentication, granule search, duplicate validation, and centralized logging.

---

##  Requisitos / Requirements

- Archivo `.env` con credenciales y configuración:

```env
EARTHDATA_USERNAME=tu_usuario
EARTHDATA_PASSWORD=tu_contraseña
MODIS_PRODUCT=MOD11A1
MAX_GRANULES=10
Archivo aoi.geojson ubicado en config/ (fuera de flask_app)

Dependencias:

bash
pip install earthaccess geopandas

 Uso básico / Basic usage
python
from modules.modis_downloader import run_modis_download

run_modis_download()
Esto ejecuta:

Autenticación con Earthdata

Carga del AOI desde config/aoi.geojson

Búsqueda de granules según producto y límite

Descarga solo de archivos nuevos

Registro de eventos en logs/modis_download.log

 Estructura recomendada / Recommended structure
Código
sat_data_pipeline/
├── config/
│   └── aoi.geojson
├── flask_app/
│   ├── config.py
│   └── modules/
│       └── modis_downloader.py
├── data/
│   └── downloads/
├── logs/
│   └── modis_download.log

 Extensiones sugeridas / Suggested extensions
Filtro por fechas de adquisición

Exportación de resumen en CSV o JSON

Visualización interactiva con Flask + Folium

Soporte para SMAP u otros sensores

Integración con sistema de trazabilidad y validación de cobertura