import geopandas as gpd
import folium
from shapely.geometry import Point
import random
import os

dir_shape={"AYACUCHO":os.path.join('Shape','Ayacucho','05_AYACUCHO_SectoresEstadisticos.shp'),
           "APURIMAC":os.path.join('Shape','Apurimac','03_APURIMAC_SectoresEstadisticos.shp'),
           "HUANCAVELICA":os.path.join('Shape','Huancavelica','09_HUANCAVELICA_SectoresEstadisticos.shp'),
           "MADRE DE DIOS":os.path.join('Shape','Madre de Dios','17_MADRE_DE_DIOS_SectoresEstadisticos.shp'),
           "MOQUEGUA":os.path.join('Shape','Moquegua','18_MOQUEGUA_SectoresEstadisticos.shp'),
           "PUNO":os.path.join('Shape','Puno','21_PUNO_SectoresEstadisticos.shp'),
           "TACNA":os.path.join('Shape','Tacna','23_TACNA_SectoresEstadisticos.shp'),
           "TUMBES":os.path.join('Shape','Tumbes','24_TUMBES_SectoresEstadisticos.shp')
           }

def GeneradorHmtl_mapa(dep,prov,distr,dicPuntos):
    file_shape=dir_shape[dep]
    shape_sector = gpd.read_file(file_shape)
    mapa = shape_sector[
        (shape_sector['NOMBDEP'] == dep) &
        (shape_sector['NOMBPROV'] == prov) &
        (shape_sector['NOMBDIST'] == distr)
    ]

    # Convertir los puntos en un GeoDataFrame
    puntos = [Point(coords) for coords in dicPuntos.values()]
    gdf_puntos = gpd.GeoDataFrame(dicPuntos.keys(), geometry=puntos, crs="EPSG:4326")

    # Crear un mapa centrado en la ubicación de los puntos
    map_center = [gdf_puntos.geometry.y.mean(), gdf_puntos.geometry.x.mean()]
    m = folium.Map(location=map_center, zoom_start=14)

    # Agregar el sector estadístico al mapa
    folium.GeoJson(mapa).add_to(m)

    # Agregar los puntos al mapa
    for punto, coord in dicPuntos.items():
        folium.Marker(location=[coord[1], coord[0]], popup=punto, icon=folium.Icon(color='yellow')).add_to(m)

    # Mostrar el mapa
    m.save("mapa.html")


#GeneradorHmtl_mapa('AYACUCHO','HUANTA','IGUAIN',generar_puntos())
