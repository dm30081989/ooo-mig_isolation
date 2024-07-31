# coding=windows-1251

import pandas as pd
import numpy as np
import overpy
# import requests
# import json
from shapely.geometry import Point, LineString, \
                             Polygon, MultiPolygon


def reverse(x: list):
    return [item for item in x[::-1]]


def nodes2line(result, nodes: list):
    """List of nodes -> list of coordinates"""
    list_of_linepoint = []
    for node_id in nodes:
        node = result.get_node(node_id)
        list_of_linepoint.append(Point(node.lon, node.lat))
    return list_of_linepoint


def create_polygon(list_of_lines: list):
    """List of lines -> polygon"""
    list_of_points = []
    for line in list_of_lines:
        list_of_points += line
    return Polygon(list_of_points)


def arrange_nodes(result, list_of_nodes: list):
    """Arrange the points in relation in the correct order"""
    list_of_lines = []   # points for each line
    list_of_polygons = []   # polygons to be returned
    for nodes in list_of_nodes:
        list_of_lines.append(nodes2line(result, nodes))
    # you need to specify ans, size and i-th element for polygon
    ans = [list_of_lines[0]]
    size = len(list_of_lines)
    i = list_of_lines.pop(0)
    # build the sequence by comparing the points in the lines
    while len(ans) < size:
        for j in list_of_lines:
            coincidences = len(set(i) & set(j))
            if coincidences == 1 or coincidences == 2:
                if i[-1] == j[0]:
                    ans.append(j)
                    i = j
                elif i[0] == j[0]:
                    ans.remove(i)
                    ans.append(reverse(i))
                    ans.append(j)
                    i = j
                elif i[-1] == j[-1]:
                    ans.append(reverse(j))
                    i = reverse(j)
                else:   # i[0] == j[-1]
                    ans.remove(i)
                    ans.append(j)
                    ans.append(i)
                list_of_lines.remove(j)
                break
        # defining a new polygon
        if coincidences == 0:
            list_of_polygons.append(create_polygon(ans))
            i = list_of_lines.pop(0)
            size = len(list_of_lines)
            ans = [i]
    list_of_polygons.append(create_polygon(ans))
    return list_of_polygons


def extract_nodes_data_from_OSM(result):
    list_of_node_tags = []
    for node in result.nodes:
        # get the geographical coordinates, add a tag
        node.tags['geometry'] = Point(node.lon, node.lat)
        list_of_node_tags.append(node.tags)
    data_frame_nodes = pd.DataFrame(list_of_node_tags)
    # data_frame_nodes.to_csv('output_node_data.csv')
    return data_frame_nodes


def extract_ways_data_from_OSM(result):
    list_of_way_tags = []
    for way in result.ways:
        # get the geographical coordinates
        list_of_points = []
        for node_id in way._node_ids:
            node = result.get_node(node_id)
            list_of_points.append(Point(node.lon, node.lat))
        # add a tag
        way.tags['geometry'] = LineString(list_of_points)
        list_of_way_tags.append(way.tags)
    data_frame_ways = pd.DataFrame(list_of_way_tags)
    # data_frame_ways.to_csv('output_way_data.csv')
    return data_frame_ways


def extract_polygons_data_from_OSM(result):
    list_of_polygons_tags = []
    for way in result.ways:
        # get the geographical coordinates
        list_of_points = []
        for node_id in way._node_ids:
            node = result.get_node(node_id)
            list_of_points.append(Point(node.lon, node.lat))
        # add a tag
        if len(list_of_points) > 1:
            way.tags['geometry'] = Polygon(list_of_points)
        else:
            way.tags['geometry'] = LineString(list_of_points)
        list_of_polygons_tags.append(way.tags)
    data_frame_polygons = pd.DataFrame(list_of_polygons_tags)
    # data_frame_polygons.to_csv('output_polygons_data.csv')
    return data_frame_polygons


def extract_relations_data_from_OSM(result):
    list_of_relation_tags = []
    for relation in result.relations:
        members = relation.members  # extract the participants of each relation
        list_of_nodes = []   # nodes of a particular relation
        for member in members:   # extract the ID of the ways
            if member.__class__ == overpy.RelationWay:
                way = result.get_ways(member.ref)
                list_of_nodes.append(way[0]._node_ids)
        # sort and get lists of coordinates for each way
        list_of_polygons = arrange_nodes(result, list_of_nodes)
        # add a tag
        relation.tags['geometry'] = MultiPolygon(list_of_polygons)
        list_of_relation_tags.append(relation.tags)
    data_frame_relations = pd.DataFrame(list_of_relation_tags)
    # data_frame_relations.to_csv('output_relation_data.csv')
    return data_frame_relations


# def extract_raw_data_from_OSM(built_query):
#     overpass_url = "http://overpass-api.de/api/interpreter"
#     response = requests.get(overpass_url,params = {'data': built_query})
#     json_data = response.json()
#     with open("output_data.json", "w") as outfile:
#         json.dump(json_data, outfile)
#     print("Raw Data extraction successfull!  check 'output_data.json' file.")
#     return json_data


# queries


def get_roads_query(latitude: float = 55.75222,
                    longitude: float = 37.61556,
                    radius: float = 10000, tag: str = 'motorway'):
    '''Get a request for roads'''
    prefix = f"""[out:json][timeout:50];(way[highway={tag}](around:"""
    suffix = """););out body;>;out skel qt;"""
    q = str(radius) + ',' + str(latitude) + ',' + str(longitude)
    built_query = prefix + q + suffix
    return built_query


def get_industrials_way_query(latitude: float = 55.75222,
                              longitude: float = 37.61556,
                              radius: float = 5000):
    '''Get a request for industrial buildings'''
    prefix = """[out:json][timeout:50];(way[landuse=industrial](around:"""
    suffix = """););out body;>;out skel qt;"""
    q = str(radius) + ',' + str(latitude) + ',' + str(longitude)
    built_query = prefix + q + suffix
    return built_query


def get_industrials_relation_query(latitude: float = 55.75222,
                                   longitude: float = 37.61556,
                                   radius: float = 5000):
    '''Get a request for industrial buildings'''
    prefix = """[out:json][timeout:50];(relation[landuse=industrial](around:"""
    suffix = """););out body;>;out skel qt;"""
    q = str(radius) + ',' + str(latitude) + ',' + str(longitude)
    built_query = prefix + q + suffix
    return built_query


def get_chimney_query(latitude: float = 55.75222,
                      longitude: float = 37.61556,
                      radius: float = 5000):
    '''Get a request for chimneys'''
    prefix = """[out:json][timeout:50];(nw[man_made=chimney](around:"""
    suffix = """););out body;>;out skel qt;"""
    q = str(radius) + ',' + str(latitude) + ',' + str(longitude)
    built_query = prefix + q + suffix
    return built_query


def get_nature_relation_query(latitude: float = 55.75222,
                              longitude: float = 37.61556,
                              radius: float = 5000):
    '''Get a request for forests and farmland'''
    prefix = """[out:json][timeout:50];("""
    farmland = """relation[landuse=farmland](around:"""
    wood = """relation[natural=wood](around:"""
    forest = """relation[landuse=forest](around:"""
    suffix = """););out body;>;out skel qt;"""
    q = str(radius) + ',' + str(latitude) + ',' + str(longitude)
    built_query = prefix + wood + q + ');' + farmland + q + ');' \
                         + forest + q + suffix
    return built_query


def get_nature_way_query(latitude: float = 55.75222,
                         longitude: float = 37.61556,
                         radius: float = 5000):
    '''Get a request for forests and farmland'''
    prefix = """[out:json][timeout:50];("""
    farmland = """way[landuse=farmland](around:"""
    wood = """way[natural=wood](around:"""
    forest = """way[landuse=forest](around:"""
    suffix = """););out body;>;out skel qt;"""
    q = str(radius) + ',' + str(latitude) + ',' + str(longitude)
    built_query = prefix + wood + q + ');' + farmland + q + ');' \
                         + forest + q + suffix
    return built_query


def get_quarry_relation_query(latitude: float = 55.75222,
                              longitude: float = 37.61556,
                              radius: float = 5000):
    '''Get a request for quarry'''
    prefix = """[out:json][timeout:50];(relation[landuse=quarry](around:"""
    suffix = """););out body;>;out skel qt;"""
    q = str(radius) + ',' + str(latitude) + ',' + str(longitude)
    built_query = prefix + q + suffix
    return built_query


def get_quarry_way_query(latitude: float = 55.75222,
                         longitude: float = 37.61556,
                         radius: float = 5000):
    '''Get a request for quarry'''
    prefix = """[out:json][timeout:50];(way[landuse=quarry](around:"""
    suffix = """););out body;>;out skel qt;"""
    q = str(radius) + ',' + str(latitude) + ',' + str(longitude)
    built_query = prefix + q + suffix
    return built_query


def get_tbo_relation_query(latitude: float = 55.75222,
                           longitude: float = 37.61556,
                           radius: float = 5000):
    '''Get a request for landfill'''
    prefix = """[out:json][timeout:50];(relation[landuse=landfill](around:"""
    suffix = """););out body;>;out skel qt;"""
    q = str(radius) + ',' + str(latitude) + ',' + str(longitude)
    built_query = prefix + q + suffix
    return built_query


def get_tbo_way_query(latitude: float = 55.75222,
                      longitude: float = 37.61556,
                      radius: float = 5000):
    '''Get a request for landfill'''
    prefix = """[out:json][timeout:50];(way[landuse=landfill](around:"""
    suffix = """););out body;>;out skel qt;"""
    q = str(radius) + ',' + str(latitude) + ',' + str(longitude)
    built_query = prefix + q + suffix
    return built_query


def get_shop_relation_query(latitude: float = 55.75222,
                            longitude: float = 37.61556,
                            radius: float = 5000):
    """Get a request for shops"""
    prefix = """[out:json][timeout:50];("""
    mall = """relation[shop=mall](around:"""
    department_store = """relation[shop=department_store](around:"""
    suffix = """););out body;>;out skel qt;"""
    q = str(radius) + ',' + str(latitude) + ',' + str(longitude)
    built_query = prefix + mall + q + ');' + department_store + q + suffix
    return built_query


def get_shop_way_query(latitude: float = 55.75222,
                       longitude: float = 37.61556,
                       radius: float = 5000):
    """Get a request for shops"""
    prefix = """[out:json][timeout:50];("""
    mall = """way[shop=mall](around:"""
    department_store = """way[shop=department_store](around:"""
    suffix = """););out body;>;out skel qt;"""
    q = str(radius) + ',' + str(latitude) + ',' + str(longitude)
    built_query = prefix + mall + q + ');' + department_store + q + suffix
    return built_query


def get_city_relation_query(latitude: float = 55.75222,
                            longitude: float = 37.61556,
                            radius: float = 5000):
    """Get a request for shops"""
    prefix = """[out:json][timeout:50];("""
    apartments = """relation[building=apartments](around:"""
    commercial = """relation[building=commercial](around:"""
    office = """relation[building=office](around:"""
    public = """relation[building=public](around:"""
    civic = """relation[building=civic](around:"""
    hotel = """relation[building=hotel](around:"""
    suffix = """););out body;>;out skel qt;"""
    q = str(radius) + ',' + str(latitude) + ',' + str(longitude)
    built_query = prefix + apartments + q + ');' + commercial + q + ');' \
                         + office + q + ');' + public + q + ');' \
                         + civic + q + ');' + hotel + q + suffix
    return built_query


def get_city_way_query(latitude: float = 55.75222,
                       longitude: float = 37.61556,
                       radius: float = 5000):
    """Get a request for shops"""
    prefix = """[out:json][timeout:50];("""
    apartments = """way[building=apartments](around:"""
    commercial = """way[building=commercial](around:"""
    office = """way[building=office](around:"""
    public = """way[building=public](around:"""
    civic = """way[building=civic](around:"""
    hotel = """way[building=hotel](around:"""
    suffix = """););out body;>;out skel qt;"""
    q = str(radius) + ',' + str(latitude) + ',' + str(longitude)
    built_query = prefix + apartments + q + ');' + commercial + q + ');' \
                         + office + q + ');' + public + q + ');' \
                         + civic + q + ');' + hotel + q + suffix
    return built_query


# tables


def get_lat_lon(geometry):
    """Enter the object and get the coordinates of the centroid"""
    lon = geometry.apply(lambda x: x.x if x.geom_type == 'Point'
                         else x.centroid.x)
    lat = geometry.apply(lambda x: x.y if x.geom_type == 'Point'
                         else x.centroid.y)
    return lat, lon


def road_table(latitude: float = 55.75222,
               longitude: float = 37.61556,
               big_radius: float = 2000,
               small_radius: float = 1000):
    '''Enter the coordinates in decimal degrees and radius for big
    and small roads and get a dataframe of the nearest roads'''
    api = overpy.Overpass()

    result = api.query(get_roads_query(latitude, longitude,
                                       big_radius, tag='motorway'))
    data1 = extract_ways_data_from_OSM(result)
    result = api.query(get_roads_query(latitude, longitude,
                                       big_radius, tag='trunk'))
    data2 = extract_ways_data_from_OSM(result)
    result = api.query(get_roads_query(latitude, longitude,
                                       big_radius, tag='primary'))
    data3 = extract_ways_data_from_OSM(result)
    result = api.query(get_roads_query(latitude, longitude,
                                       small_radius, tag='secondary'))
    data4 = extract_ways_data_from_OSM(result)
    result = api.query(get_roads_query(latitude, longitude,
                                       small_radius, tag='tertiary'))
    data5 = extract_ways_data_from_OSM(result)

    data = pd.concat([
        data1, data2, data3, data4, data5,
    ])

    if 'geometry' not in data.columns:
        data['geometry'] = np.nan
    if 'name' not in data.columns:
        data['name'] = np.nan
    if 'highway' not in data.columns:
        data['highway'] = np.nan
    if 'ref' not in data.columns:
        data['ref'] = np.nan
    if 'maxspeed' not in data.columns:
        data['maxspeed'] = np.nan
    if 'lanes' not in data.columns:
        data['lanes'] = np.nan
    data['element_type'] = "way"
    data['pue'] = 0
    data['rank'] = 0

    data = data[[
        'element_type', 'highway', 'geometry', 'name', 'maxspeed',
        'lanes', 'ref', 'pue', 'rank',
    ]]

    data.reset_index(inplace=True, drop=True)
    return data


def industrial_table(latitude: float = 55.75222,
                     longitude: float = 37.61556,
                     radius: float = 5000):
    '''Enter the coordinates in decimal degrees and radius
    and get a dataframe of the nearest industrial buildings'''
    api = overpy.Overpass()

    result = api.query(get_industrials_way_query(latitude, longitude, radius))
    data1 = extract_polygons_data_from_OSM(result)
    data1['element_type'] = "way"
    result = api.query(get_industrials_relation_query(latitude, longitude,
                                                      radius))
    data2 = extract_relations_data_from_OSM(result)
    data2['element_type'] = "relation"

    data = pd.concat([
        data1, data2,
    ])

    if 'geometry' not in data.columns:
        data['geometry'] = np.nan
    if 'name' not in data.columns:
        data['name'] = np.nan
    if 'product' not in data.columns:
        data['product'] = np.nan
    data['type'] = data['landuse']
    data['production_volume'] = 0
    data['pue'] = np.nan

    data = data[[
        'element_type', 'type', 'geometry', 'name', 'pue',
        'production_volume', 'product',
    ]]
    # add centroids
    lat, lon = get_lat_lon(data['geometry'])
    data['lat'] = lat
    data['lon'] = lon

    data = data.dropna(subset=['name'])
    data.reset_index(inplace=True, drop=True)
    return data


def chimney_table(latitude: float = 55.75222,
                  longitude: float = 37.61556,
                  radius: float = 5000):
    """Enter the coordinates in decimal degrees and radius
    and get a dataframe of the nearest chimney"""
    api = overpy.Overpass()

    result = api.query(get_chimney_query(latitude, longitude, radius))
    data = extract_polygons_data_from_OSM(result)

    if 'geometry' not in data.columns:
        data['geometry'] = np.nan
    if 'height' not in data.columns:
        data['height'] = np.nan
    data['point_type'] = 'chimney'
    data['power'] = -1

    data = data[[
        'point_type', 'geometry', 'height', 'power',
    ]]
    # add centroids
    lat, lon = get_lat_lon(data['geometry'])
    data['lat'] = lat
    data['lon'] = lon

    data.reset_index(inplace=True, drop=True)
    return data


def nature_table(latitude: float = 55.75222,
                 longitude: float = 37.61556,
                 radius: float = 5000):
    """Enter the coordinates in decimal degrees and radius
    and get a dataframe of the nearest forests and farmland"""
    api = overpy.Overpass()

    result = api.query(get_nature_way_query(latitude, longitude, radius))
    data1 = extract_polygons_data_from_OSM(result)
    data1['element_type'] = "way"
    result = api.query(get_nature_relation_query(latitude, longitude, radius))
    data2 = extract_relations_data_from_OSM(result)
    data2['element_type'] = "relation"

    data = pd.concat([
        data1, data2,
    ])

    if 'geometry' not in data.columns:
        data['geometry'] = np.nan
    if 'name' not in data.columns:
        data['name'] = np.nan
    data['pue'] = np.nan
    data['type'] = np.nan
    for index in data.index:
        if data.iloc[index]['natural'] == "wood":
            data.loc[index, 'type'] = 'wood'
        elif data.iloc[index]['landuse'] == "forest":
            data.loc[index, 'type'] = 'forest'
        else:
            data.loc[index, 'type'] = 'farmland'

    data = data[[
        'element_type', 'type', 'geometry', 'name', 'pue',
    ]]
    # add centroids
    lat, lon = get_lat_lon(data['geometry'])
    data['lat'] = lat
    data['lon'] = lon

    data.reset_index(inplace=True, drop=True)
    return data


def quarry_table(latitude: float = 55.75222,
                 longitude: float = 37.61556,
                 radius: float = 5000):
    """Enter the coordinates in decimal degrees and radius
    and get a dataframe of the nearest quarry"""
    api = overpy.Overpass()

    result = api.query(get_quarry_way_query(latitude, longitude, radius))
    data1 = extract_polygons_data_from_OSM(result)
    data1['element_type'] = "way"
    result = api.query(get_quarry_relation_query(latitude, longitude, radius))
    data2 = extract_relations_data_from_OSM(result)
    data2['element_type'] = "relation"

    data = pd.concat([
        data1, data2,
    ])

    data['type'] = 'quarry'
    if 'geometry' not in data.columns:
        data['geometry'] = np.nan
    if 'name' not in data.columns:
        data['name'] = np.nan
    data['pue'] = np.nan

    data = data[[
        'element_type', 'type', 'geometry', 'name', 'pue',
    ]]
    # add centroids
    lat, lon = get_lat_lon(data['geometry'])
    data['lat'] = lat
    data['lon'] = lon

    data.reset_index(inplace=True, drop=True)
    return data


def tbo_table(latitude: float = 55.75222,
              longitude: float = 37.61556,
              radius: float = 5000):
    """Enter the coordinates in decimal degrees and radius
    and get a dataframe of the nearest landfill"""
    api = overpy.Overpass()

    result = api.query(get_tbo_way_query(latitude, longitude, radius))
    data1 = extract_polygons_data_from_OSM(result)
    data1['element_type'] = "way"
    result = api.query(get_tbo_relation_query(latitude, longitude, radius))
    data2 = extract_relations_data_from_OSM(result)
    data2['element_type'] = "relation"

    data = pd.concat([
        data1, data2,
    ])

    data['type'] = 'landfill'
    if 'geometry' not in data.columns:
        data['geometry'] = np.nan
    if 'name' not in data.columns:
        data['name'] = np.nan
    data['pue'] = np.nan

    data = data[[
        'element_type', 'type', 'geometry', 'name', 'pue',
    ]]
    # add centroids
    lat, lon = get_lat_lon(data['geometry'])
    data['lat'] = lat
    data['lon'] = lon

    data.reset_index(inplace=True, drop=True)
    return data


def city_table(latitude: float = 55.75222,
               longitude: float = 37.61556,
               radius: float = 5000):
    '''Enter the coordinates in decimal degrees and radius
    and get a dataframe of the nearest city buildings.'''
    api = overpy.Overpass()

    result = api.query(get_shop_way_query(latitude, longitude, radius))
    data1 = extract_polygons_data_from_OSM(result)
    data1['element_type'] = "way"
    result = api.query(get_shop_relation_query(latitude, longitude, radius))
    data2 = extract_relations_data_from_OSM(result)
    data2['element_type'] = "relation"
    result = api.query(get_city_way_query(latitude, longitude, radius))
    data3 = extract_polygons_data_from_OSM(result)
    data3['element_type'] = "way"
    result = api.query(get_city_relation_query(latitude, longitude, radius))
    data4 = extract_relations_data_from_OSM(result)
    data4['element_type'] = "relation"

    data = pd.concat([
        data1, data2, data3, data4,
    ])

    data['type'] = data['building']
    if 'geometry' not in data.columns:
        data['geometry'] = np.nan
    if 'name' not in data.columns:
        data['name'] = np.nan
    if 'building:levels' not in data.columns:
        data['building:levels'] = np.nan
    if 'height' not in data.columns:
        data['height'] = np.nan

    data = data[[
        'element_type', 'type', 'geometry', 'name',
        'building:levels', 'height',
    ]]

    # add centroids
    lat, lon = get_lat_lon(data['geometry'])
    data['lat'] = lat
    data['lon'] = lon

    data.reset_index(inplace=True, drop=True)
    return data


# choice


def choose_roads(data: pd.DataFrame):
    """Enter all the data and get a data from the pilot zone"""
    data1 = data[data.ref == '�-4']
    data2 = data[data.ref == '�-2']
    data3 = data[data.ref == '�-5']
    data4 = data[data.ref == '�-107']
    data5 = data[data.ref == '�-113']
    data6 = data[data.name == '������������� �����']
    data7 = data[data['name'].str.contains('����', na=False)]
    data8 = data[data.name == '��������� �����']
    data9 = data[data.name == '��������� �����']
    data10 = data[data.name == '��������������� �����']

    new_data = pd.concat([
        data1, data2, data3, data4, data5, data6, data7, data8, data9, data10,
    ])

    new_data.reset_index(drop=True, inplace=True)
    return new_data


def choose_industrial(data: pd.DataFrame):
    """Enter all the data and get a data from the pilot zone"""
    data1 = data[data['name'].str.contains('������', na=False)]
    data2 = data[data['name'].str.contains('�����', na=False)]
    data3 = data[data['name'].str.contains('���', na=False)]
    data4 = data[data['name'].str.contains('�������', na=False)]

    new_data = pd.concat([
        data1, data2, data3, data4,
    ])

    new_data.reset_index(drop=True, inplace=True)
    return new_data


def choose_source(latitude: float, longitude: float, distance: float = 5000):
    """Get a database of all sources for a specific coordinate"""
    data1 = industrial_table(latitude, longitude, distance)
    data2 = nature_table(latitude, longitude, distance)
    data3 = quarry_table(latitude, longitude, distance)
    data4 = tbo_table(latitude, longitude, distance)

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
