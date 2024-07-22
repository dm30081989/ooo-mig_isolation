# обработка информации из api osm и ее приведение к удобному формату

import pandas as pd            							
from shapely.geometry import Point, LineString, Polygon, MultiPolygon
# import requests
# import json

def reverse(x: list):
    return [item for item in x[::-1]]

def nodes2line(result, nodes: list): # список узлов -> список точек 
    list_of_linepoint = []
    for node_id in nodes:
        node = result.get_node(node_id)
        list_of_linepoint.append(Point(node.lon, node.lat)) 
    return list_of_linepoint

def create_polygon(list_of_lines: list):
    list_of_points = []
    for line in list_of_lines:
        list_of_points += line
    return Polygon(list_of_points)

def arrange_nodes(result, list_of_nodes: list):
    list_of_lines = [] # список точек для каждой линии
    list_of_polygons = [] # cписок полигонов, которые будут возвращены
    for nodes in list_of_nodes:
        list_of_lines.append(nodes2line(result, nodes))

    ans = [list_of_lines[0]] # берем первый список 
    size = len(list_of_lines)
    i = list_of_lines.pop(0)

    while len(ans) < size:
        for j in list_of_lines: 
            coincidences = len(set(i)&set(j))
            if coincidences ==  1 or coincidences == 2:
                
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
                else: #i[0] == j[-1]
                    ans.remove(i)
                    ans.append(j)
                    ans.append(i)
                    
                list_of_lines.remove(j)
                break

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
        
        node.tags['geometry'] = Point(node.lon, node.lat)
        list_of_node_tags.append(node.tags)

    data_frame_nodes = pd.DataFrame(list_of_node_tags)
    #data_frame_nodes.to_csv('output_node_data.csv')
    return data_frame_nodes

def extract_ways_data_from_OSM(result):  
    list_of_way_tags = []
    for way in result.ways:
        
        list_of_points = []
        for node_id in way._node_ids:
            node = result.get_node(node_id)
            list_of_points.append(Point(node.lon, node.lat))     
        
        way.tags['geometry'] = LineString(list_of_points)
        list_of_way_tags.append(way.tags)

    data_frame_ways = pd.DataFrame(list_of_way_tags)
    #data_frame_ways.to_csv('output_way_data.csv')
    return data_frame_ways

def extract_polygons_data_from_OSM(result):  
    list_of_polygons_tags = []
    for way in result.ways:
        
        list_of_points = []
        for node_id in way._node_ids:
            node = result.get_node(node_id)
            list_of_points.append(Point(node.lon, node.lat))     
        
        way.tags['geometry'] = Polygon(list_of_points) if len(list_of_points) > 2 else LineString(list_of_points)
        list_of_polygons_tags.append(way.tags)

    data_frame_polygons = pd.DataFrame(list_of_polygons_tags)
    #data_frame_polygons.to_csv('output_polygons_data.csv')
    return data_frame_polygons

def extract_relations_data_from_OSM(result):
    list_of_relation_tags = []
    for relation in result.relations: # заходим в каждое отношение 
        
        members = relation.members # достаем всех участников данного отношения
        list_of_nodes = [] # список узлов учатсников конкретного отношения
        for member in members: # достаем айди путей
            #if member.__class__ == overpy.RelationWay:
            way = result.get_ways(member.ref)
            list_of_nodes.append(way[0]._node_ids)

        # теперь сортируем и достаем списки координат для каждой линии
        list_of_polygons = arrange_nodes(result, list_of_nodes)
        
        relation.tags['geometry'] = MultiPolygon(list_of_polygons)
        list_of_relation_tags.append(relation.tags)
                
    data_frame_relations = pd.DataFrame(list_of_relation_tags)
    #data_frame_relations.to_csv('output_relation_data.csv')
    return data_frame_relations
                    
# def extract_raw_data_from_OSM(built_query):
#     overpass_url = "http://overpass-api.de/api/interpreter"
#     response = requests.get(overpass_url,params = {'data': built_query})
#     json_data = response.json()
#     with open("output_data.json", "w") as outfile: 
#         json.dump(json_data, outfile)
#     print("Raw Data extraction successfull!  check 'output_data.json' file.")
#     return json_data
