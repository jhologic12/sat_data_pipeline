from shapely.geometry import shape
import json

def get_bbox_from_geojson(path):
    with open(path, "r", encoding="utf-8") as f:
        geojson_data = json.load(f)
    geom = shape(geojson_data["geometry"])
    return geom.bounds  # (minx, miny, maxx, maxy)
