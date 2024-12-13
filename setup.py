from setuptools import setup, find_packages

setup(
    name='Muestreo Puntos',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'geopandas',
        'folium',
        'shapely',
        'flask',
        'simplekml',
    ],
)
