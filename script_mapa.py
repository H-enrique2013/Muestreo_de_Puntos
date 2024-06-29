import geopandas as gpd
import folium
from shapely.geometry import Point
import random



dir_shape={"AYACUCHO":"Shape/Ayacucho/05_AYACUCHO_SectoresEstadisticos.shp",
           "APURIMAC":"Shape/Apurimac/03_APURIMAC_SectoresEstadisticos.shp",
           "HUANCAVELICA":"Shape/Huancavelica/09_HUANCAVELICA_SectoresEstadisticos.shp",
           "MADRE DE DIOS":"Shape/Madre de Dios/17_MADRE_DE_DIOS_SectoresEstadisticos.shp",
           "MOQUEGUA":"Shape/Moquegua/18_MOQUEGUA_SectoresEstadisticos.shp",
           "PUNO":"Shape/Puno/21_PUNO_SectoresEstadisticos.shp",
           "TACNA":"Shape/Tacna/23_TACNA_SectoresEstadisticos.shp",
           "TUMBES":"Shape/Tumbes/24_TUMBES_SectoresEstadisticos.shp",
           }

# Generar los 11 puntos
def generar_puntos():
    dicPuntos = {}
    for i in range(1, 12):
        indice = "Punto " + str(i)
        random_longitud = random.uniform(-74.216694960800000, -74.22389061599995)
        random_latitud = random.uniform(-12.966311839999946, -12.999319500999945)
        dicPuntos[indice] = [random_longitud, random_latitud]
    return dicPuntos

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


