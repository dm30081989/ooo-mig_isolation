# �������� ������ �� ����������
import pandas as pd
from shapely.geometry import Point, LineString, Polygon, MultiPolygon

# ������� ��� ���������� ������� ���������. ������������ ��� ������� ���. ����������
def calculate_production_volume(data: pd.DataFrame):
    # ���������� �� ������� 
    recount = data.groupby('name').count()
    count = list(recount['geometry'])
    
    resum = data[['power', 'name']].groupby('name').sum()
    sum = list(resum['power'])

    for i in range(len(count)):
        if count[i] != 1 and sum[i] == -count[i]: # ������ ��� ����

            producte_volume = list(data[data.name == resum.index[i]]['production_volume'])[0]
            data.loc[data.name == resum.index[i], 'power'] = 100 / count[i]
            data.loc[data.name == resum.index[i], 'production_volume'] = producte_volume / count[i]
        
        elif sum[i] < 101: # ������ ���� ��� �����
            
            lines = data[data.name == resum.index[i]] # ������� ��� ������� ����� �������
            indexes = list(lines.index) # � ��� ������� � �������
            
            unknown_indexes = [] # ������ ���� ��� ������� ���������� 
            all_power = 0 # ������� ���� �������� ��������

            # ��������� ��������� � ��������� �����������
            for index in indexes:
                if data.iloc[index]['power'] != -1:
                    all_power += data.iloc[index]['power']
                    data.loc[index, 'production_volume'] = data.iloc[index]['production_volume'] * data.iloc[index]['power'] / 100
                else:
                    unknown_indexes.append(index) 
            
            # ��������� ����������� 
            for index in unknown_indexes:
                data.loc[data.index == index, 'power'] = (100-all_power)/len(unknown_indexes)
                data.loc[data.index == index, 'production_volume'] = data.iloc[index]['production_volume'] * data.iloc[index]['power'] / 100

        else:
            print(f'Incorrect data: ����������� ��������� ��� ����� � ������ {data[data.name == resum.index[i]].index[0]} ')
    
    return data

def clarify_location(buildings, chimneys):
    
    buildings.sort_values(by = ['distance'], ascending = False, inplace = True, ignore_index = True)
    chimneys.sort_values(by = ['distance'], ascending = False, inplace = True, ignore_index = True)
    
    sorted_chimneys = chimneys[[
        'height', 'geometry', 'point_type', 'lat', 'lon', 'distance', 'power',
    ]]

    sorted_buildings = buildings[[
        'element_type', 'geometry', 'name', 'lat', 'lon', 'type', 'distance', 'production_volume', 'product',
    ]]

    # ������� ����� �������
    sorted_buildings["height_chimney"] = np.nan
    sorted_buildings["power"] = -1.0
    
    count_b, len_b = 0, len(sorted_buildings)
    
    while count_b < len_b:  # ���� �� ���� �������

        count_c = 0
        chimneys_before = len(sorted_chimneys)
      
        while count_c < len(sorted_chimneys) and len(sorted_chimneys) != 0: # � �� ���� ������, ������� ��� �� ������������
            
            # ���� ����� ������ � �������
            if sorted_buildings.iloc[count_b]['geometry'].intersects(sorted_chimneys.iloc[count_c]['geometry']): 
                #print(sorted_buildings.iloc[count_b]['name'], sorted_chimneys.iloc[count_c]['geometry'])
                
                sorted_buildings.loc[len(sorted_buildings.index)] = sorted_buildings.iloc[count_b]
                sorted_buildings.loc[len(sorted_buildings.index)-1, "lat"] = sorted_chimneys.iloc[count_c]['lat']
                sorted_buildings.loc[len(sorted_buildings.index)-1, "lon"] = sorted_chimneys.iloc[count_c]['lon']
                sorted_buildings.loc[len(sorted_buildings.index)-1, "height_chimney"] = sorted_chimneys.iloc[count_c]['height']
                sorted_buildings.loc[len(sorted_buildings.index)-1, "distance"] = sorted_chimneys.iloc[count_c]['distance']
                sorted_buildings.loc[len(sorted_buildings.index)-1, "type"] = sorted_chimneys.iloc[count_c]['point_type']
                sorted_buildings.loc[len(sorted_buildings.index)-1, "power"] = sorted_chimneys.iloc[count_c]['power']

                sorted_chimneys = sorted_chimneys.drop([count_c]) 
                sorted_chimneys.reset_index(drop = True , inplace = True)
            
            else:
                count_c += 1 # ��������� � ��������� ����� 

        chimneys_after = len(sorted_chimneys)
        
        # ������� ������� � ����� ��� ������ ���� ���������� �����
        if chimneys_before - chimneys_after > 0:
            sorted_buildings = sorted_buildings.drop([count_b]) 
            sorted_buildings.reset_index(drop = True, inplace = True)
        else:
            count_b += 1

    sorted_buildings = calculate_production_volume(sorted_buildings)
    sorted_buildings['pue'] = np.nan
    
    return sorted_buildings, sorted_chimneys

# ������� ��� ��������� ������� ��������� ��� �������� ��������� � ���������� ��� ������� ������������. ���������������� 
def update_production_volume(data: pd.DataFrame, name:str, value: float):
    # ���������� �� ������� 
    recount = data.groupby('name').count()
    count = recount[recount.index == name].element_type[0]

    for index in data1[data1.name == name].index:
        data.loc[index, 'production_volume'] = value * data.iloc[index]['power'] / 100     

    return data