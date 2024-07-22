# позволяет менять/добавлять данные в базы
import pandas as pd
import numpy as np
from shapely.geometry import Point, LineString, Polygon, MultiPolygon

def add_production_volume_name(data: pd.DataFrame, value: float, name: str):
    data.loc[data['name'].str.contains(name, na = False), 'production_volume'] = value
    return data

def add_production_volume_name_user(data):
    '''Set the production capacity using its name.'''
    name = input('Введите название промышленного здания: ')
    while name not in data['name'].values:
        name = input('Такого здания нет в БД. Попробуйте снова: ')
    value = float(input('Введите объем продукции: '))
    return add_production_volume_name(data, value, name)

def add_production_volume_index(data: pd.DataFrame, value: float, index: int):
    data.loc[data.index == index, 'production_volume'] = value
    return data

def add_production_volume_index_user(data):
    '''Set the production capacity using its index.'''
    index = int(input('Введите индекс промышленного здания: '))
    while int(index) >= len(data):
        index = int(input('Такого индекса нет в БД. Попробуйте снова: '))
    value = float(input('Введите объем продукции: '))
    return add_production_volume_index(data, value, index)

def add_production_volume_geo(data: pd.DataFrame, value: float, latitude: float, longitude: float):
    lat, lon = str(latitude), str(longitude)
    
    lat_len = abs(lat.find('.') - len(lat)) - 1
    lon_len = abs(lon.find('.') - len(lon)) - 1

    data.loc[(round(data['lat'], lat_len) == latitude) 
            & (round(data['lon'], lon_len) == longitude), 'production_volume'] = value
    
    return data

def add_production_volume_geo_user(data):
    '''Set the production capacity using its coordinates.'''
    lat = input('Введите координату широты промышленного здания: ')
    lon = input('Введите координату долготы промышленного здания: ')
    
    lat_len = abs(lat.find('.') - len(lat)) - 1
    lon_len = abs(lon.find('.') - len(lon)) - 1
        
    while data[(round(data['lat'], lat_len) == float(lat))
                & (round(data['lon'], lon_len) == float(lon))].empty:
        lat = input('Таких координат нет в БД. Введите широту снова: ')
        lon = input('Введите координату долготы промышленного здания: ')
        lat_len = abs(lat.find('.') - len(lat)) - 1
        lon_len = abs(lon.find('.') - len(lon)) - 1
    
    value = float(input('Введите объем продукции: '))
    
    return add_production_volume_geo(data, value, float(lat), float(lon))

def add_power_index(data: pd.DataFrame, value: float, index: int):
    data.loc[data.index == index, 'power'] = value
    return data

def add_power_index_user(data):
    '''Set the production capacity using its index.'''
    index = int(input('Введите индекс трубы: '))
    while int(index) >= len(data):
        index = int(input('Такого индекса нет в БД. Попробуйте снова: '))

    value = input('Введите значение доли отходов: ')
    while value > 100 or value < 0:
        value = input('Значение должно быть положительным и меньше 100. Введите значение еще раз: ')

    return add_power_index(data, float(value), index)

def add_power_geo(data: pd.DataFrame, value: float, latitude: float, longitude: float):
    lat, lon = str(latitude), str(longitude)
    
    lat_len = abs(lat.find('.') - len(lat)) - 1
    lon_len = abs(lon.find('.') - len(lon)) - 1

    data.loc[(round(data['lat'], lat_len) == latitude) 
            & (round(data['lon'], lon_len) == longitude), 'power'] = value
    
    return data

def add_power_geo_user(data):
    '''Set the production capacity using its coordinates.'''
    lat = input('Введите координату широты трубы: ')
    lon = input('Введите координату долготы трубы: ')
    
    lat_len = abs(lat.find('.') - len(lat)) - 1
    lon_len = abs(lon.find('.') - len(lon)) - 1
        
    while data[(round(data['lat'], lat_len) == float(lat))
                & (round(data['lon'], lon_len) == float(lon))].empty:
        lat = input('Таких координат нет в БД. Введите широту снова: ')
        lon = input('Введите координату долготы трубы: ')
        lat_len = abs(lat.find('.') - len(lat)) - 1
        lon_len = abs(lon.find('.') - len(lon)) - 1
    
    value = input('Введите значение доли отходов: ')
    while value > 100 or value < 0:
        value = input('Значение должно быть положительным и меньше 100. Введите значение еще раз: ')
    
    return add_power_geo(data, float(value), float(lat), float(lon))

def add_road(data: pd.DataFrame):
    '''Add a road.'''
    name = input('Введите название дороги: ')
    count = int(input('Введите количество точек: '))
    points = []
    
    for i in range(count):
        latitude = float(input(f'Введите координату широты {i+1}-й точки: '))
        longitude = float(input(f'Введите координату высоты {i+1}-й точки: '))
        points.append(Point(longitude, latitude))
        
    maxspeed = input('Введите максимальную скорость, если она известна. Иначе пропустите: ')
    lanes =  input('Введите количество линий, если оно известно. Иначе пропустите: ')

    if maxspeed == '':
        maxspeed = np.nan

    if lanes == '':
        lanes = np.nan

    data.loc[len(data.index)] = ['input', 'input', LineString(points), name, float(maxspeed), float(lanes), np.nan, 0, 0]
    return data

def add_polygon(data: pd.DataFrame):
    '''Add a dirty building or nature object.'''
    type = input('Введите тип обьекта: ')
    name = input('Введите название промышленного здания, если оно есть: ')
    count = int(input('Введите количество точек: '))
    points = []
    
    for i in range(count):
        latitude = float(input(f'Введите координату широты {i+1}-й точки: '))
        longitude = float(input(f'Введите координату высоты {i+1}-й точки: '))
        points.append(Point(longitude, latitude))
        
    production_volume = input('Введите объем производств, если он известен. Иначе пропустите: ')
    product =  input('Введите тег продукции, если он известен. Иначе пропустите: ')

    if production_volume == '':
        production_volume = 0

    if product == '':
        product = np.nan

    if name == '':
        name = np.nan

    data.loc[len(data.index)] = ['input', type, Polygon(points), name, 0, float(production_volume), product, Polygon(points).centroid.x, Polygon(points).centroid.x]
    return data

def add_chimney_point(data: pd.DataFrame):
    '''Add a dot to some dirty building.'''
    point_type = input('Введите название типа точки. Например, труба: ')
    latitude = float(input('Введите координату широты: '))
    longitude = float(input('Введите координату высоты: '))
    height = input('Введите высоту точки, если она известа. Иначе пропустите: ')
    power =  input('Введите долю отходов точки, если она известа. Иначе пропустите: ')

    if height == '':
        height = np.nan

    if power == '':
        power = -1
    
    data.loc[len(data.index)] = [point_type, Point(longitude,  latitude), float(height), float(power), latitude, longitude]
    return data

def add_chimney_polygon(data: pd.DataFrame):
    '''Add a dot to some dirty building.'''
    point_type = input('Введите название типа точки. Например, труба: ')
    count = int(input('Введите количество точек: '))
    points = []
    
    for i in range(count):
        latitude = float(input(f'Введите координату широты {i+1}-й точки: '))
        longitude = float(input(f'Введите координату высоты {i+1}-й точки: '))
        points.append(Point(longitude, latitude))
        
    height = input('Введите высоту точки, если она известа. Иначе пропустите: ')
    power =  input('Введите долю отходов точки, если она известа. Иначе пропустите: ')

    if height == '':
        height = np.nan

    if power == '':
        power = -1

    data.loc[len(data.index)] = [point_type, Polygon(points), float(height), float(power), Polygon(points).centroid.x, Polygon(points).centroid.x]
    return data

# data.to_excel('output_data.xlsx') # добавит данные в файл 'output_data.xlsx' в текущей директории
# тут можно изменять данные!
# data = pd.read_excel('output_data.xlsx') # выгрузит свежие данные 