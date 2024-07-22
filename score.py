# ��������� ������ � �������

import pue
import dist
import pandas as pd

# tags:
# chemistry - ���������� ����������� � ������������
# cellulose - ������������ ���������
# paper - ������������ ������
# cast_iron - �������� ������ � �����
# mount - ������������������� ���������
# coke_chemical - ��������������������
# aluminum - ������������ ��������
# rera_metal - ������������ ������ ��������
# color_metal - ������������ � ��������� ������� ��������
# cement - ������������ �������
# asbestos - ������������ ������� � ��
# concrete - ������������ �������� ������� � ��.
# car - ������������������ ����������� ��� ������������
# iron_mining - ������ �������� ����
# coal_mining - ������ ����
# boiler_slate - ��� � ��������� �� ������� (����� ������ �����)
# boiler_�oal - ��� � ��������� �� ����� (����� ������ �����)
# tbo - ������ ������� ����������, ��������� ������ � ����������, �������������-�������� ����������
# road - ���������� � ����������� �������������� � ������ ����� ���������� �������

def add_pue_roads(lat: float, lon: float, roads: pd.DataFrame):
    for index in roads.index:
        distance = dist.nearest2road(lat, lon, roads.iloc[index]['geometry'])[0]
        roads.loc[index, 'pue'] = pue.pue_road(distance)
    return roads

def add_pue_tbo(lat: float, lon: float, tbo: pd.DataFrame):
    for index in tbo.index:
        distance = dist.nearest2polygon(lat, lon, tbo.iloc[index]['geometry'])
        tbo.loc[index, 'pue'] = pue.pue_tbo(distance)
    return tbo

def add_pue_industrial(lat: float, lon: float, industrials: pd.DataFrame):

    dict_for_pue = {'chemistry':  pue_chemistry, 'cellulose': pue_cellulose,
                'paper': pue_paper, 'cast_iron': pue_ferrous_metallurgy_1,
                'mount': pue_ferrous_metallurgy_2, 'aluminum': pue_aluminum,
                'coke_chemical': pue_ferrous_metallurgy_3, 'rera_metal': pue_rare_metals,
                'color_metal': pue_color_metals, 'cement': pue_cement,
                'asbestos': pue_asbestos, 'concrete': pue_other_materials,
                'car': pue_�ar, 'iron_mining': pue_iron_mining,
                'coal_mining': pue_coal_mining, 'boiler_slate': pue_tes_slate, 
                'boiler_�oal': pue_tes_coal, 'tbo': pue_tbo, 
               }
    
    for index in industrials.index:
        distance = dist.nearest2polygon(lat, lon, industrials.iloc[index]['geometry'])
        product = industrials.iloc[index]['product']
        
        if pd.isnull(product):
            rank = 0
        else:
            func = dict_for_pue[product]
            rank = pue.func(industrials.iloc[index]['production_volume'], distance, industrials.iloc[index]['height'])
        
        industrials.loc[index, 'pue'] = rank

    return industrials

### ����� ��� �����
def road_score(data: pd.DataFrame, month: int):
    lat, lon = 55.7522, 37.6156
    
    # ���� - ��� : 20 �� - 5.5
    score_big = [4.6, 4.5, 4.7, 4.7, 4.5, 4.3, 3.7, 4, 4.6, 4.8, 5, 5.4]
    # ��� - ������� 5.5 - 2.5
    score_midlle = [4.5, 4.9, 5.1, 5.6, 5.6, 6.1, 5.1, 4.9, 4.9, 5.4, 5.7, 6]
    # ������ ��������
    score_small = [4.8, 5.6, 6.4, 7.4, 7.7, 8, 7.6, 7.3, 6.2, 6.5, 6.1, 6.8]

    for index in data.index:
        distance = dist.nearest2road(lat, lon, data.iloc[index]['geometry'])[0]
        print(distance)
        if distance < 2500:
            data.loc[index, 'rank'] = score_small[month-1]
        elif distance < 5500:
            data.loc[index, 'rank'] = score_midlle[month-1]
        elif distance < 20000:
            data.loc[index, 'rank'] = score_big[month-1]
    
    return data
