# ��������� ������/��������� ������ � ����
import pandas as pd
import numpy as np
from shapely.geometry import Point, LineString, Polygon, MultiPolygon

def add_production_volume_name(data: pd.DataFrame, value: float, name: str):
    data.loc[data['name'].str.contains(name, na = False), 'production_volume'] = value
    return data

def add_production_volume_name_user(data):
    '''Set the production capacity using its name.'''
    name = input('������� �������� ������������� ������: ')
    while name not in data['name'].values:
        name = input('������ ������ ��� � ��. ���������� �����: ')
    value = float(input('������� ����� ���������: '))
    return add_production_volume_name(data, value, name)

def add_production_volume_index(data: pd.DataFrame, value: float, index: int):
    data.loc[data.index == index, 'production_volume'] = value
    return data

def add_production_volume_index_user(data):
    '''Set the production capacity using its index.'''
    index = int(input('������� ������ ������������� ������: '))
    while int(index) >= len(data):
        index = int(input('������ ������� ��� � ��. ���������� �����: '))
    value = float(input('������� ����� ���������: '))
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
    lat = input('������� ���������� ������ ������������� ������: ')
    lon = input('������� ���������� ������� ������������� ������: ')
    
    lat_len = abs(lat.find('.') - len(lat)) - 1
    lon_len = abs(lon.find('.') - len(lon)) - 1
        
    while data[(round(data['lat'], lat_len) == float(lat))
                & (round(data['lon'], lon_len) == float(lon))].empty:
        lat = input('����� ��������� ��� � ��. ������� ������ �����: ')
        lon = input('������� ���������� ������� ������������� ������: ')
        lat_len = abs(lat.find('.') - len(lat)) - 1
        lon_len = abs(lon.find('.') - len(lon)) - 1
    
    value = float(input('������� ����� ���������: '))
    
    return add_production_volume_geo(data, value, float(lat), float(lon))

def add_power_index(data: pd.DataFrame, value: float, index: int):
    data.loc[data.index == index, 'power'] = value
    return data

def add_power_index_user(data):
    '''Set the production capacity using its index.'''
    index = int(input('������� ������ �����: '))
    while int(index) >= len(data):
        index = int(input('������ ������� ��� � ��. ���������� �����: '))

    value = input('������� �������� ���� �������: ')
    while value > 100 or value < 0:
        value = input('�������� ������ ���� ������������� � ������ 100. ������� �������� ��� ���: ')

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
    lat = input('������� ���������� ������ �����: ')
    lon = input('������� ���������� ������� �����: ')
    
    lat_len = abs(lat.find('.') - len(lat)) - 1
    lon_len = abs(lon.find('.') - len(lon)) - 1
        
    while data[(round(data['lat'], lat_len) == float(lat))
                & (round(data['lon'], lon_len) == float(lon))].empty:
        lat = input('����� ��������� ��� � ��. ������� ������ �����: ')
        lon = input('������� ���������� ������� �����: ')
        lat_len = abs(lat.find('.') - len(lat)) - 1
        lon_len = abs(lon.find('.') - len(lon)) - 1
    
    value = input('������� �������� ���� �������: ')
    while value > 100 or value < 0:
        value = input('�������� ������ ���� ������������� � ������ 100. ������� �������� ��� ���: ')
    
    return add_power_geo(data, float(value), float(lat), float(lon))

def add_road(data: pd.DataFrame):
    '''Add a road.'''
    name = input('������� �������� ������: ')
    count = int(input('������� ���������� �����: '))
    points = []
    
    for i in range(count):
        latitude = float(input(f'������� ���������� ������ {i+1}-� �����: '))
        longitude = float(input(f'������� ���������� ������ {i+1}-� �����: '))
        points.append(Point(longitude, latitude))
        
    maxspeed = input('������� ������������ ��������, ���� ��� ��������. ����� ����������: ')
    lanes =  input('������� ���������� �����, ���� ��� ��������. ����� ����������: ')

    if maxspeed == '':
        maxspeed = np.nan

    if lanes == '':
        lanes = np.nan

    data.loc[len(data.index)] = ['input', 'input', LineString(points), name, float(maxspeed), float(lanes), np.nan, 0, 0]
    return data

def add_polygon(data: pd.DataFrame):
    '''Add a dirty building or nature object.'''
    type = input('������� ��� �������: ')
    name = input('������� �������� ������������� ������, ���� ��� ����: ')
    count = int(input('������� ���������� �����: '))
    points = []
    
    for i in range(count):
        latitude = float(input(f'������� ���������� ������ {i+1}-� �����: '))
        longitude = float(input(f'������� ���������� ������ {i+1}-� �����: '))
        points.append(Point(longitude, latitude))
        
    production_volume = input('������� ����� �����������, ���� �� ��������. ����� ����������: ')
    product =  input('������� ��� ���������, ���� �� ��������. ����� ����������: ')

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
    point_type = input('������� �������� ���� �����. ��������, �����: ')
    latitude = float(input('������� ���������� ������: '))
    longitude = float(input('������� ���������� ������: '))
    height = input('������� ������ �����, ���� ��� �������. ����� ����������: ')
    power =  input('������� ���� ������� �����, ���� ��� �������. ����� ����������: ')

    if height == '':
        height = np.nan

    if power == '':
        power = -1
    
    data.loc[len(data.index)] = [point_type, Point(longitude,  latitude), float(height), float(power), latitude, longitude]
    return data

def add_chimney_polygon(data: pd.DataFrame):
    '''Add a dot to some dirty building.'''
    point_type = input('������� �������� ���� �����. ��������, �����: ')
    count = int(input('������� ���������� �����: '))
    points = []
    
    for i in range(count):
        latitude = float(input(f'������� ���������� ������ {i+1}-� �����: '))
        longitude = float(input(f'������� ���������� ������ {i+1}-� �����: '))
        points.append(Point(longitude, latitude))
        
    height = input('������� ������ �����, ���� ��� �������. ����� ����������: ')
    power =  input('������� ���� ������� �����, ���� ��� �������. ����� ����������: ')

    if height == '':
        height = np.nan

    if power == '':
        power = -1

    data.loc[len(data.index)] = [point_type, Polygon(points), float(height), float(power), Polygon(points).centroid.x, Polygon(points).centroid.x]
    return data

# data.to_excel('output_data.xlsx') # ������� ������ � ���� 'output_data.xlsx' � ������� ����������
# ��� ����� �������� ������!
# data = pd.read_excel('output_data.xlsx') # �������� ������ ������ 