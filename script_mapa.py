import geopandas as gpd
import folium
from shapely.geometry import Point
import os
import datetime

def GeneradorHmtl_mapa(dep, prov, distr, sect, dicPuntos):
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

    # Añadir control de capas con atribución
    folium.TileLayer(
        tiles='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        attr='Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors',
        name='Mapa Estándar'
    ).add_to(m)
    
    folium.TileLayer(
        tiles='https://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}.jpg',
        attr='Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under ODbL.',
        name='Vista Satelital'
    ).add_to(m)
    
    folium.TileLayer(
        tiles='https://stamen-tiles-{s}.a.ssl.fastly.net/toner/{z}/{x}/{y}.png',
        attr='Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under ODbL.',
        name='Híbrido'
    ).add_to(m)

    folium.GeoJson(mapa, name='GeoJson').add_to(m)

    for punto, coord in dicPuntos.items():
        folium.Marker(location=[coord[1], coord[0]], popup=punto, icon=folium.Icon(color='orange')).add_to(m)

    # Añadir leyenda
    legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 200px; height: 120px; 
     background-color: white; z-index:9999; font-size:14px;
     border:2px solid grey; padding: 10px;">
     <strong>Leyenda</strong><br>
     <i class="fa fa-map-marker fa-2x" style="color:orange"></i> Puntos<br>
     <i class="fa fa-map fa-2x" style="color:blue"></i> Sector<br>
     </div>
     '''
    m.get_root().html.add_child(folium.Element(legend_html))

    folium.LayerControl().add_to(m)

    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    url_mapa = f"{dep}_{prov}_{distr}_{now}.html"
    filepath = os.path.join("static", url_mapa)
    m.save(filepath)

    return filepath
