import geopandas as gpd
import folium
from shapely.geometry import Point
import os
import datetime
import simplekml

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

    mapbox_api_key = 'pk.eyJ1IjoiZW5yaXF1ZXNhbmRvdmFsIiwiYSI6ImNseWhxZmU2NTA3NjkybW9mbWxzZXpmdGQifQ.c1uvRvMYZyEaLaCqYioUmw'
    # Añadir capas de mapas utilizando Mapbox
    folium.TileLayer(
        tiles=f'https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/256/{{z}}/{{x}}/{{y}}@2x?access_token={mapbox_api_key}',
        attr='Map data © <a href="https://www.mapbox.com/">Mapbox</a>',
        name='Mapa Estándar'
    ).add_to(m)
    
    folium.TileLayer(
        tiles=f'https://api.mapbox.com/styles/v1/mapbox/satellite-v9/tiles/256/{{z}}/{{x}}/{{y}}@2x?access_token={mapbox_api_key}',
        attr='Map data © <a href="https://www.mapbox.com/">Mapbox</a>',
        name='Vista Satelital'
    ).add_to(m)
    
    folium.TileLayer(
        tiles=f'https://api.mapbox.com/styles/v1/mapbox/satellite-streets-v11/tiles/256/{{z}}/{{x}}/{{y}}@2x?access_token={mapbox_api_key}',
        attr='Map data © <a href="https://www.mapbox.com/">Mapbox</a>',
        name='Híbrido'
    ).add_to(m)

    folium.GeoJson(
        mapa,name='Sector Estadistico',
        style_function=lambda feature: {
            'fillColor': '#ADD8E6',  # Azul claro
            'weight': 2,             # Grosor del borde
            'fillOpacity': 0.6       # Opacidad del relleno
        }
    ).add_to(m)

    for punto, coord in dicPuntos.items():
        folium.Marker(location=[coord[1], coord[0]], popup=punto, icon=folium.Icon(color='red')).add_to(m)

    # Añadir leyenda
    legend_html = '''
    <div style="position: fixed; 
    top: 468px; left: 7px; width: 300px; height: 100px; 
    background-color: white; z-index:9999; font-size:11px;
    border:2px solid grey; padding: 10px;">
    <div style="background-color: red; font-size:14px;color:white;padding: 5px;">
    <strong>LEYENDA</strong>
    </div>
    <i class="fa fa-map-marker fa-2x" style="color:red"></i> Puntos<br>
    <svg width="24" height="24"><rect width="24" height="24" style="fill:#ADD8E6;stroke-width:1;stroke:rgb(0,0,0)" /></svg> Sector Estadistico<br>
    </div>
     '''
    m.get_root().html.add_child(folium.Element(legend_html))

    # Añadir cuadro "Datos del sector Estadístico"
    datos_sector = f'''
    <div style="position: fixed; 
    top: 80px; left: 7px; width: 300px; height: 120px; 
    background-color: white; z-index:9999; font-size:11px;
    border:2px solid grey; padding: 10px;">
    <div style="background-color: red; font-size:14px;color:white;padding: 5px;">
    <strong>DATOS DEL SECTOR ESTADÍSTICO</strong>
    </div>
    Departamento: {dep}<br>
    Provincia: {prov}<br>
    Distrito: {distr}<br>
    Sector Estadístico: {sect}<br>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(datos_sector))

    # Añadir cuadro "Cuadro de Coordenadas"
    coordenadas = '''
    <div style="position: fixed; top: 200px; left: 7px; width: 300px; height: 268px; 
    background-color: white; z-index: 9999; font-size: 11px; border: 2px solid grey; padding: 10px;">
    <div style="background-color: red; font-size: 14px; color: white; padding: 5px;">
    <strong>CUADRO DE COORDENADAS</strong>
    </div>
    <table style="width: 100%;">
    <tr>
    <th style="text-align: center; padding-right: 10px;">Puntos</th>
    <th style="text-align: center; padding-right: 10px;">Longitud</th>
    <th style="text-align: center;">Latitud</th>
    </tr>
    '''
    # Iterar sobre los puntos y coordenadas
    for punto, coord in dicPuntos.items():
        coordenadas += f'<tr><td>{punto}</td><td>{coord[0]}</td><td>{coord[1]}</td></tr>'
    coordenadas += '</table></div>'
    # Añadir el cuadro de coordenadas al mapa folium
    m.get_root().html.add_child(folium.Element(coordenadas))

    folium.LayerControl().add_to(m)

    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    url_mapa = f"{dep}_{prov}_{distr}_{now}.html"
    filepath = os.path.join("static", url_mapa)
    m.save(filepath)

    # Crear archivo KML
    kml = simplekml.Kml()

    # Añadir puntos al KML
    for punto, coord in dicPuntos.items():
        kml.newpoint(name=punto, coords=[(coord[0], coord[1])])

    # Añadir geometrías del shapefile al KML
    for _, row in mapa.iterrows():
        if row.geometry.geom_type == 'Polygon':
            pol = kml.newpolygon(name=row['NOM_SE'], outerboundaryis=list(row.geometry.exterior.coords))
        elif row.geometry.geom_type == 'MultiPolygon':
            for poly in row.geometry:
                pol = kml.newpolygon(name=row['NOM_SE'], outerboundaryis=list(poly.exterior.coords))

    kml_filepath = os.path.join("static", f"{dep}_{prov}_{distr}_{now}.kml")
    kml.save(kml_filepath)

    return filepath,kml_filepath
