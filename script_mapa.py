import geopandas as gpd
import folium
from shapely.geometry import Point
import os
import datetime
import glob

def GeneradorHmtl_mapa(dep, prov, distr, dicPuntos):
    shapefile_dir = f'Shape/{dep.capitalize()}'
    shapefile_paths = glob.glob(os.path.join(shapefile_dir, '*.shp'))
    
    if not shapefile_paths:
        raise ValueError(f"No se encontraron archivos de shapefile para '{dep}' en '{shapefile_dir}'")
    
    # Seleccionar el primer archivo .shp encontrado
    shapefile_path = shapefile_paths[0]
    
    shape_sector = gpd.read_file(shapefile_path)
    
    mapa = shape_sector[
        (shape_sector['NOMBDEP'] == dep) &
        (shape_sector['NOMBPROV'] == prov) &
        (shape_sector['NOMBDIST'] == distr)
    ]

    # Convertir los puntos en un GeoDataFrame
    puntos = [Point(coords) for coords in dicPuntos.values()]
    gdf_puntos = gpd.GeoDataFrame(list(dicPuntos.keys()), geometry=puntos, crs="EPSG:4326")

    # Crear un mapa centrado en la ubicación de los puntos
    map_center = [gdf_puntos.geometry.y.mean(), gdf_puntos.geometry.x.mean()]
    m = folium.Map(location=map_center, zoom_start=14)

    # Agregar el sector estadístico al mapa
    folium.GeoJson(mapa).add_to(m)

    # Agregar los puntos al mapa
    for punto, coord in dicPuntos.items():
        folium.Marker(location=[coord[1], coord[0]], popup=punto, icon=folium.Icon(color='orange')).add_to(m)

    # Generar el nombre del archivo con la combinación de departamento, provincia, distrito y hora actual
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    url_mapa = f"{dep}_{prov}_{distr}_{now}.html"
    filepath = os.path.join("static", url_mapa)  # Guardar en la carpeta 'static' de Flask
    m.save(filepath)

    return filepath  # Devolver la ruta al archivo generado
