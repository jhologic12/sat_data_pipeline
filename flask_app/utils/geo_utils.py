import json
from shapely.geometry import shape

def get_bbox_from_geojson(path):
    """
    Extrae el bounding box [west, south, east, north] desde un archivo GeoJSON.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            geojson_data = json.load(f)
            geometry = shape(geojson_data["geometry"])
            bounds = geometry.bounds  # (minx, miny, maxx, maxy)
            return [bounds[0], bounds[1], bounds[2], bounds[3]]
    except Exception as e:
        raise RuntimeError(f"Error al extraer bounding box del AOI: {str(e)}")

def validate_aoi(path, min_area=0.0001):
    """
    Valida que el AOI tenga geometría válida y área suficiente.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            geojson_data = json.load(f)
            geom = shape(geojson_data["geometry"])
            if not geom.is_valid:
                raise ValueError("La geometría del AOI es inválida.")
            if geom.area < min_area:
                raise ValueError(f"El AOI es demasiado pequeño (área: {geom.area:.6f})")
    except Exception as e:
        raise RuntimeError(f"Error al validar AOI: {str(e)}")
