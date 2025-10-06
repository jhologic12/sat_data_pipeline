def format_granule(granule):
    """
    Extrae información clave desde granule.render_dict.
    """
    try:
        g = granule.render_dict  # Aquí están los metadatos reales

        # Fecha de inicio
        date = g.get("Temporal coverage", {}).get("RangeDateTime", {}).get("BeginningDateTime", "Sin fecha")

        # Enlace de descarga
        url = g.get("Data", ["Sin enlace"])[0]

        # Producto
        product = g.get("ShortName", "Sin producto")

        # Coordenadas del primer punto del polígono
        points = g.get("Spatial coverage", {}) \
                  .get("HorizontalSpatialDomain", {}) \
                  .get("Geometry", {}) \
                  .get("GPolygons", [{}])[0] \
                  .get("Boundary", {}) \
                  .get("Points", [])

        lat = points[0]["Latitude"] if points else None
        lon = points[0]["Longitude"] if points else None

        return {
            "uuid": getattr(granule, "uuid", "Sin UUID"),
            "product": product,
            "date": date,
            "url": url,
            "lat": lat,
            "lon": lon
        }

    except Exception as e:
        print(f"⚠️ Error al formatear granule: {e}")
        return {"error": "Granule inválido"}
