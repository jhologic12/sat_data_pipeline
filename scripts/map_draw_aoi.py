import folium
from folium.plugins import Draw

# 🌍 Punto inicial (Colombia)
map_center = [11.0, -74.0]
m = folium.Map(location=map_center, zoom_start=7, tiles="OpenStreetMap")

# 🛠️ Herramientas de dibujo
draw = Draw(
    export=True,
    filename='aoi.geojson',
    position='topleft',
    draw_options={
        'polyline': False,
        'rectangle': True,
        'polygon': True,
        'circle': False,
        'marker': False,
        'circlemarker': False
    },
    edit_options={'edit': True}
)
draw.add_to(m)

#  Guardar como HTML
m.save("config/aoi_map.html")
print("Mapa guardado en config/aoi_map.html. Ábrelo en tu navegador para dibujar tu AOI.")
