# проектирование всех баз данных

import pandas as pd
from shapely.geometry import Point, LineString, Polygon, MultiPolygon

import osmapi
import numpy as np
import overpy 

def get_lat_lon(geometry):
    """Enter the object and get the coordinates of the centroid."""    
    lon = geometry.apply(lambda x: x.x if x.geom_type == 'Point' else x.centroid.x)
    lat = geometry.apply(lambda x: x.y if x.geom_type == 'Point' else x.centroid.y)
    return lat, lon

def get_roads_query(latitude: float = 55.75222, longitude: float = 37.61556, radius: float = 10000, tag: str = 'motorway'):
    '''Get a request for roads.'''
    prefix = f"""[out:json][timeout:50];(way[highway={tag}](around:""" 
    suffix = """););out body;>;out skel qt;"""	
	
    q = str(radius) + ',' + str(latitude) + ',' + str(longitude)      
    built_query = prefix + q + suffix                             
	
    return built_query    

def get_industrials_query(latitude: float = 55.75222, longitude: float = 37.61556, radius: float = 5000):
    '''Get a request for industrial buildings.'''
    prefix = """[out:json][timeout:50];(wr[landuse=industrial](around:""" 
    suffix = """););out body;>;out skel qt;"""	
	
    q = str(radius) + ',' + str(latitude) + ',' + str(longitude)      
    built_query = prefix + q + suffix                             
	
    return built_query

def get_chimney_query(latitude: float = 55.75222, longitude: float = 37.61556, radius: float = 5000):
    '''Get a request for chimneys.'''
    prefix = """[out:json][timeout:50];(nw[man_made=chimney](around:""" 
    suffix = """););out body;>;out skel qt;"""	
	
    q = str(radius) + ',' + str(latitude) + ',' + str(longitude)      
    built_query = prefix + q + suffix                             
	
    return built_query  

def get_nature_query(latitude: float = 55.75222, longitude: float = 37.61556, radius: float = 1000):
    '''Get a request for forests and farmland.'''
    prefix = """[out:json][timeout:50];("""
    farmland = """wr[landuse=farmland](around:"""
    wood = """wr[natural=wood](around:"""
    forest = """wr[landuse=forest](around:"""
    suffix = """););out body;>;out skel qt;"""	
	
    q = str(radius) + ',' + str(latitude) + ',' + str(longitude)      
    built_query = prefix + wood + q +');'+ farmland + q + ');'+ forest + q + suffix                            
    return built_query  

def get_quarry_query(latitude: float = 55.75222, longitude: float = 37.61556, radius: float = 1000):
    '''Get a request for quarry.'''
    prefix = """[out:json][timeout:50];(wr[landuse=quarry](around:"""
    suffix = """););out body;>;out skel qt;"""	
	
    q = str(radius) + ',' + str(latitude) + ',' + str(longitude)      
    built_query = prefix + q + suffix                            
	
    return built_query    

def get_tbo_query(latitude: float = 55.75222, longitude: float = 37.61556, radius: float = 1000):
    '''Get a request for landfill.'''
    prefix = """[out:json][timeout:50];(wr[landuse=landfill](around:"""
    suffix = """););out body;>;out skel qt;"""	
	
    q = str(radius) + ',' + str(latitude) + ',' + str(longitude)      
    built_query = prefix + q + suffix                            
	
    return built_query    

def road_table(latitude: float = 55.75222, longitude: float = 37.61556, big_radius: float = 5000, small_radius: float = 1000):
    '''Enter the coordinates in decimal degrees and radius for big and small roads and get a dataframe of the nearest roads.'''
    api = overpy.Overpass()                       
    
    result = api.query(get_roads_query(latitude, longitude, big_radius, tag = 'motorway'))   
    data1 = osmapi.extract_ways_data_from_OSM(result)
    result = api.query(get_roads_query(latitude, longitude, big_radius, tag = 'trunk'))
    data2 = osmapi.extract_ways_data_from_OSM(result)
    result = api.query(get_roads_query(latitude, longitude, big_radius, tag = 'primary'))
    data3 = osmapi.extract_ways_data_from_OSM(result)
    result = api.query(get_roads_query(latitude, longitude, small_radius, tag = 'secondary'))
    data4 = osmapi.extract_ways_data_from_OSM(result)
    result = api.query(get_roads_query(latitude, longitude, small_radius, tag = 'tertiary'))
    data5 = osmapi.extract_ways_data_from_OSM(result)

    data = pd.concat([
        data1, data2, data3, data4, data5,
    ])
    
    data = data.copy()

    data['highway'] = np.nan if 'highway' not in data.columns else data['highway']
    data['geometry'] = np.nan if 'geometry' not in data.columns else data['geometry']
    data['name'] = np.nan if 'name' not in data.columns else data['name']
    data['ref'] = np.nan if 'ref' not in data.columns else data['ref']
    data['maxspeed'] = np.nan if 'maxspeed' not in data.columns else data['maxspeed']
    data['lanes'] = np.nan if 'lanes' not in data.columns else data['lanes']
    data['element_type'] = "way"
    data['pue'] = 0
    data['rank'] = 0

    data = data[[
        'element_type', 'highway', 'geometry', 'name', 'maxspeed', 'lanes', 'ref', 'pue', 'rank',
    ]]

    return data

def industrial_table(latitude: float = 55.75222, longitude: float = 37.61556, radius: float = 5000):
    '''Enter the coordinates in decimal degrees and radius and get a dataframe of the nearest industrial buildings.'''
    api = overpy.Overpass()                       
    result = api.query(get_industrials_query(latitude, longitude, radius))  
    
    data1 = osmapi.extract_polygons_data_from_OSM(result)
    data1['element_type'] = "way"
    data2 = osmapi.extract_relations_data_from_OSM(result)
    data2['element_type'] = "relation"
    
    data = pd.concat([
        data1, data2,
    ])
    
    data = data.copy()

    data['geometry'] = np.nan if 'geometry' not in data.columns else data['geometry']
    data['name'] = np.nan if 'name' not in data.columns else data['name']
    data['type'] = data['landuse']
    data['product'] = np.nan if 'product' not in data.columns else data['product']
    data['production_volume'] = 0
    data['pue'] = np.nan
    
    data = data[[
        'element_type', 'type', 'geometry', 'name', 'pue', 'production_volume', 'product',
    ]]
    
    # можно добавить центроиды
    lat, lon = get_lat_lon(data['geometry'])
    data['lat'] = lat
    data['lon'] = lon

    data = data.dropna(subset=['name'])
    return data

def chimney_table(latitude: float = 55.75222, longitude: float = 37.61556, radius: float = 5000):
    """Enter the coordinates in decimal degrees and radius and get a dataframe of the nearest chimney."""
    api = overpy.Overpass()                       
    result = api.query(get_chimney_query(latitude, longitude, radius)) 
    
    data = extract_polygons_data_from_OSM(result)
    data['element_type'] = "way"
    
    data.reset_index(drop = True , inplace = True)
    data['geometry'] = np.nan if 'geometry' not in data.columns else data['geometry']
    data['height'] = np.nan if 'height' not in data.columns else data['height']
    data['point_type'] = 'chimney'
    data['power'] = -1
    
    data = data[[
        'point_type', 'geometry', 'height', 'power', 
    ]]
    
    # можно добавить центроиды
    lat, lon = get_lat_lon(data['geometry'])
    data['lat'] = lat
    data['lon'] = lon
    
    return data

def nature_table(latitude: float = 55.75222, longitude: float = 37.61556, radius: float = 5000):
    """Enter the coordinates in decimal degrees and radius and get a dataframe of the nearest forests and farmland."""
    api = overpy.Overpass()                       
    result = api.query(get_nature_query(latitude, longitude, radius))
    
    data1 = osmapi.extract_polygons_data_from_OSM(result)
    data1['element_type'] = "way"
    data2 = osmapi.extract_relations_data_from_OSM(result)
    data2['element_type'] = "relation"

    data = pd.concat([
        data1, data2,
    ])
    
    data = data.copy()

    data['geometry'] = np.nan if 'geometry' not in data.columns else data['geometry']
    data['name'] = np.nan if 'name' not in data.columns else data['name']
    data['pue'] = np.nan

    data['type'] = np.nan
    for index in data.index:
        if data.iloc[index]['natural'] == "wood":
            data.loc[index, 'type'] = 'wood'
        elif data.iloc[index]['landuse'] == "forest":
            data.loc[index,'type'] = 'forest'
        else:
            data.loc[index,'type'] = 'farmland'
    
    data = data[[
        'element_type', 'type', 'geometry', 'name', 'pue',
    ]]
    
    # можно добавить центроиды
    lat, lon = get_lat_lon(data['geometry'])
    data['lat'] = lat
    data['lon'] = lon
    
    return data 

def quarry_table(latitude: float = 55.75222, longitude: float = 37.61556, radius: float = 5000):
    """Enter the coordinates in decimal degrees and radius and get a dataframe of the nearest quarry."""
    api = overpy.Overpass()                       
    result = api.query(get_quarry_query(latitude, longitude, radius))
    
    data1 = osmapi.extract_polygons_data_from_OSM(result)
    data1['element_type'] = "way"
    data2 = osmapi.extract_relations_data_from_OSM(result)
    data2['element_type'] = "relation"

    data = pd.concat([
        data1, data2, 
    ])

    data = data.copy()

    data['geometry'] = np.nan if 'geometry' not in data.columns else data['geometry']
    data['name'] = np.nan if 'name' not in data.columns else data['name']
    data['type'] = 'quarry'
    data['pue'] = np.nan

    data = data[[
        'element_type', 'type', 'geometry', 'name', 'pue',
    ]]
    
    # можно добавить центроиды
    lat, lon = get_lat_lon(data['geometry'])
    data['lat'] = lat
    data['lon'] = lon

    return data

def tbo_table(latitude: float = 55.75222, longitude: float = 37.61556, radius: float = 5000):
    """Enter the coordinates in decimal degrees and radius and get a dataframe of the nearest landfill."""
    api = overpy.Overpass()                       
    result = api.query(get_tbo_query(latitude, longitude, radius))
    
    data1 = osmapi.extract_polygons_data_from_OSM(result)
    data1['element_type'] = "way"
    data2 = osmapi.extract_relations_data_from_OSM(result)
    data2['element_type'] = "relation"
    
    data = pd.concat([
        data1, data2,
    ])
    
    data = data.copy()

    data['geometry'] = np.nan if 'geometry' not in data.columns else data['geometry']
    data['name'] = np.nan if 'name' not in data.columns else data['name']
    data['type'] = 'landfill'
    data['pue'] = np.nan
    
    data = data[[
        'element_type', 'type', 'geometry', 'name', 'pue',
    ]]
    
    # можно добавить центроиды
    lat, lon = get_lat_lon(data['geometry'])
    data['lat'] = lat
    data['lon'] = lon
    
    return data

def choose_roads(data: pd.DataFrame):
    '''Enter all the data and get a data from the pilot zone.'''

    data1 = data[data.ref == 'М-4']
    data2 = data[data.ref == 'М-2']
    data3 = data[data.ref == 'М-5']
    data4 = data[data.ref == 'А-107']
    data5 = data[data.ref == 'А-113']
    data6 = data[data.name == 'Новорязанское шоссе']
    data7 = data[data['name'].str.contains('МКАД', na = False)]
    data8 = data[data.name == 'Каширское шоссе']
    data9 = data[data.name == 'Рязанское шоссе']
    data10 = data[data.name == 'Симферопольское шоссе']
    new_data = pd.concat([
        data1, data2, data3, data4, data5, data6, data7, data8, data9, data10,
    ])
    new_data.reset_index(drop = True , inplace = True)
    return new_data     

def choose_industrial(data: pd.DataFrame):
    '''Enter all the data and get a data from the pilot zone.'''
    data1 = data[data['name'].str.contains('Ступин', na = False)]
    data2 = data[data['name'].str.contains('Кашир', na = False)]
    data3 = data[data['name'].str.contains('ТЭЦ', na = False)]
    data4 = data[data['name'].str.contains('Домодед', na = False)]
    new_data = pd.concat([
        data1, data2, data3, data4,
    ])
    new_data.reset_index(drop = True , inplace = True)
    return new_data

# достать базу всех источников для конкретной координаты
def choose_source(lat: float, lon: float, distance: float = 5000):

    data1 = industrial_table(lat, lon, distance)
    data1 = data1.dropna(subset=['name'])
    data2 = nature_table(lat, lon, distance)
    data3 = quarry_table(lat, lon, distance)
    data4 = tbo_table(lat, lon, distance)
    
    data = pd.concat([
        data2, data3, data4,
    ])
    
    data['production_volume'] = np.nan
    data['product'] = np.nan

    data = pd.concat([
        data1, data,
    ])
    
    data.reset_index(inplace=True, drop=True)
    
    return data