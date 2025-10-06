from earthaccess import search_data, DataGranules
import os
import logging

def download_granules(short_name, bbox, limit, download_dir):
    """
    Descarga granules MODIS usando bounding box y guarda en el directorio especificado.
    """
    os.makedirs(download_dir, exist_ok=True)

    try:
        # Buscar granules con filtro espacial y límite
        results = search_data(
            short_name=short_name,
            bounding_box=bbox,
            cloud_hosted=True,
            limit=limit
        )

        granules = DataGranules(results)

        if not granules:
            logging.warning("No se encontraron granules para los parámetros dados.")
            return

        for granule in granules:
            links = granule.data_links()
            if not links:
                logging.warning(f"Granule sin enlaces de descarga: {granule.title}")
                continue

            filename = os.path.basename(links[0])
            filepath = os.path.join(download_dir, filename)

            if os.path.exists(filepath):
                logging.info(f"Granule ya existe, omitido: {filename}")
                continue

            try:
                granule.download(download_dir)
                logging.info(f"Granule descargado: {filename}")
            except Exception as e:
                logging.error(f"Error al descargar {filename}: {e}")

    except Exception as e:
        logging.error(f"Error en la búsqueda o descarga de granules: {e}")
