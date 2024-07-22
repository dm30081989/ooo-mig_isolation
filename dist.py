
# функции поиска расстояний
import math
import pandas as pd
from shapely.ops import nearest_points
from shapely.geometry import Point, LineString, Polygon, MultiPolygon

def nearest2point(lat1: float, lon1: float, lat2: float, lon2: float):
    
    R = 6371 # Radius of the earth in km
    lat_dif = deg2rad(lat2-lat1)
    lon_dif = deg2rad(lon2-lon1)
  
    a = math.sin(lat_dif/2) * math.sin(lat_dif/2) + \
        math.cos(deg2rad(lat1)) * math.cos(deg2rad(lat2)) * \
        math.sin(lon_dif/2) * math.sin(lon_dif/2)
     
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c * 1000
    
    return distance

def deg2rad(deg):
    return deg * math.pi/180

def meteres2degree(metre):
    return metre/(2*math.pi*6371)

def nearest2polygon(lat: float, lon: float, building: Polygon):
    building_lat, building_lon = building.centroid.y, building.centroid.x
    return nearest2point(lat, lon, building_lat, building_lon)

# интерполция по двум точкам
def koef(lat1: float, lon1: float, lat2: float, lon2: float):
    ''' a_x - коэф при x
        b_y - коэф при y
        с - свободный коэф
    '''
    if lat2 == lat1:
        return 1, 0, -lat1
    elif lon2 == lon1:
        return 0, 1, -lon1
        
    a_x = 1/(lat2-lat1)
    b_y = -1/(lon2-lon1)
    c = -lat1/(lat2-lat1) + lon1/(lon2-lon1)
    return a_x, b_y, c

# одна секунда вдоль меридиана соответствует примерно 31 м. будем работать с 1/3 секунды = 0.0000916 (10 метров)
def nearest2line(lat: float, lon: float, line):

    min_dist, min_coord = 21000, 0
    xs, ys = [], []
    
    for x,y in zip(line.coords.xy[1], line.coords.xy[0]):
                xs.append(x)
                ys.append(y)

    count = 0
    
    while count < len(xs)-1: # идем по всем участкам
        
        a_x, b_y, c = koef(xs[count], ys[count], xs[count+1], ys[count+1]) # каждый участок аппроксимируем 
        temp_x = xs[count] # начинаем с нулевого
        
        while abs(temp_x - xs[count+1]) >= 0.0000916: # пока следующая точка находится на расстоянии от последней > 50 метров 
            temp_y = (-a_x*temp_x - c)/b_y # вычисляем широту
            dist = nearest2point(lat, lon, temp_x, temp_y) #считаем расстояние от точки до точки 

            if dist < min_dist:
                min_dist = dist
                min_coord = Point(temp_x, temp_y)

            # переходим к следующей точке
            if temp_x < xs[count+1]: 
                temp_x += 0.0000916
            else:
                temp_x -= 0.0000916
        
        count += 1

    return min_dist, min_coord

# проверка на итерируемость
def is_iterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False

def nearest2road(lat: float, lon: float, road):

    min_dist, min_coord = 5000, 0
    
    if is_iterable(road):
        for line in road:
            
            dist, coord = nearest2line(lat, lon, line)
            
            if dist < min_dist:
                min_dist = dist
                min_coord = coord
                
    else:
        return nearest2line(lat, lon, road)

    return min_dist, min_coord

def add_distance2polygon(lat: float, lon: float, data):
    '''Add a column to the data with the distance to the support, which is set in coordinates. For buildings.'''
    data['distance'] = 0
    data = data.reset_index()
    
    for index in data.index:
        data.loc[index, 'distance'] = int(nearest2polygon(lat, lon, data.iloc[index]['geometry']))
        
    return data

def add_distance2road(lat: float, lon: float, data):
    '''Add a column to the data with the distance to the support, which is set in coordinates. For roads.'''
    data['distance'] = 0
    data = data.reset_index()
    
    for index in data.index:
        data.loc[index, 'distance'] = int(nearest2road(lat, lon, data.iloc[index]['geometry']))
        
    return data