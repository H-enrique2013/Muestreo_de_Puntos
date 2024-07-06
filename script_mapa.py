import geopandas as gpd
import folium
from shapely.geometry import Point
import os
import datetime

def GeneradorHmtl_mapa(dep, prov, distr,sect,dicPuntos):
    nom_dep = dep.replace(" ", "_")
    shapefile_dir = f'shapefiles/{nom_dep}.shp'
    shapefile_path = os.path.join(shapefile_dir)
    
    if not os.path.exists(shapefile_path):
        raise ValueError(f"No se encontraron archivos de shapefile para '{dep}' en '{shapefile_dir}'")
    
    shape_sector = gpd.read_file(shapefile_path)

    # Imprimir los tipos de datos de las columnas para depuración
    print(f"Column types in shapefile: {shape_sector.dtypes}")

    # Convertir cualquier campo de tipo Timestamp a cadena
    for col in shape_sector.columns:
        if 'datetime64' in str(shape_sector[col].dtype):
            shape_sector[col] = shape_sector[col].astype(str)

    # Filtrar el shapefile por departamento, provincia y distrito
    mapa = shape_sector[
        (shape_sector['NOMBDEP'] == dep) &
        (shape_sector['NOMBPROV'] == prov) &
        (shape_sector['NOMBDIST'] == distr) &
        (shape_sector['NOM_SE'] == sect)
    ]

    # Asegurarse de que el filtro no devuelve un NoneType
    if mapa.empty:
        raise ValueError(f"No se encontraron datos para {dep}, {prov}, {distr}")

    puntos = [Point(coords) for coords in dicPuntos.values()]
    gdf_puntos = gpd.GeoDataFrame(list(dicPuntos.keys()), geometry=puntos, crs="EPSG:4326")

    map_center = [gdf_puntos.geometry.y.mean(), gdf_puntos.geometry.x.mean()]
    m = folium.Map(location=map_center, zoom_start=14)

    folium.GeoJson(mapa).add_to(m)

    for punto, coord in dicPuntos.items():
        folium.Marker(location=[coord[1], coord[0]], popup=punto, icon=folium.Icon(color='orange')).add_to(m)

    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    url_mapa = f"{dep}_{prov}_{distr}_{now}.html"
    filepath = os.path.join("static", url_mapa)
    m.save(filepath)

    return filepath
