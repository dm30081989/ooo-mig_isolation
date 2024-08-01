import pandas as pd
import distancer as dst


# 1.9.15 highways in winter
def pue_road(distance: float):
    if distance < 25:
        return 3
    elif distance < 100:
        return 2
    return 1


# 1.9.3 chemical production
def pue_chemistry(volume: float, distance: float, height: float):
    chemistry_table = [[1, 1, 1, 1, 1, 1, 1, 1,],
                       [2, 1, 1, 1, 1, 1, 1, 1,],
                       [3, 2, 1, 1, 1, 1, 1, 1,],
                       [3, 3, 2, 1, 1, 1, 1, 1,],
                       [4, 3, 3, 2, 2, 1, 1, 1,],
                       [4, 4, 3, 3, 3, 2, 2, 1,],]

    row, column = 0, 0

    if 9 < volume < 500:
        row = 1
    elif 0 < volume // 500 < 7:
        row = (3 + volume // 500) // 2
    elif volume > 3499:
        row = 5

    if distance // 500 < 6:
        column = distance // 500
    elif distance < 5000:
        column = 6
    else:
        column = 7

    return chemistry_table[int(row)][int(column)]


# 1.9.6 cellulose and paper production
def pue_paper(volume: float, distance: float, height: float):
    return 1


def pue_cellulose(volume: float, distance: float, height: float):
    if 74 < volume < 150 and distance < 500:
        return 2
    elif 149 < volume < 500 and distance < 500:
        return 3
    elif 149 < volume < 500 and distance < 1000:
        return 2
    elif 499 < volume < 1000 and distance < 500:
        return 4
    elif 499 < volume < 1000 and distance < 1000:
        return 3
    elif 499 < volume < 1000 and distance < 1500:
        return 2
    return 1


# 1.9.7 cast iron and steel
def pue_ferrous_metallurgy_1(volume: float, distance: float, height: float):
    if distance < 500 and volume < 7500:
        return 2
    elif distance < 500:
        return 3
    elif distance < 1500 and volume < 1500:
        return 1
    elif distance < 1500:
        return 2
    elif 1499 < distance < 2000 and volume > 7499:
        return 2
    return 1


# mining and processing plants
def pue_ferrous_metallurgy_2(volume: float, distance: float, height: float):
    if distance < 500 and volume > 5499:
        return 3
    elif distance < 500 and volume > 1999:
        return 2
    elif distance < 500:
        return 1
    elif distance < 1000 and volume > 5499:
        return 2
    elif distance < 1000 and volume > 9999:
        return 3
    elif 999 < distance < 1500 and volume > 9999:
        return 2
    return 1


# coke chemical production
def pue_ferrous_metallurgy_3(volume: float, distance: float, height: float):
    if distance > 2499:
        return 1
    elif 5000 < volume < 12000 and distance < 500:
        return 3
    return 2


# 1.9.8 non-ferrous metallurgy
def pue_aluminum(volume: float, distance: float, height: float):
    if volume > 499 and distance < 1000:
        return 3
    elif 2000 > volume > 999 and 1500 > distance > 999:
        return 3
    elif 500 > volume > 99 and distance < 1000:
        return 2
    elif 1000 > volume > 499 and 2000 > distance > 999:
        return 2
    elif 2000 > volume > 999 and 2500 > distance > 1499:
        return 2
    return 1


def pue_rare_metals(volume: float, distance: float, height: float):
    if distance < 1000:
        return 4
    elif distance < 2000:
        return 3
    elif distance < 3500:
        return 2
    return 1


def pue_color_metals(volume: float, distance: float, height: float):
    if distance < 500:
        return 2
    return 1


# 1.9.9 building materials production
def pue_cement(volume: float, distance: float, height: float):
    cement_table = [[1, 1, 1, 1, 1, 1, 1,],
                    [2, 2, 1, 1, 1, 1, 1,],
                    [3, 3, 2, 1, 1, 1, 1,],
                    [3, 3, 3, 2, 1, 1, 1,],
                    [4, 4, 3, 3, 2, 1, 1,],
                    [4, 4, 4, 3, 3, 2, 1,],]

    row, column = 0, 0

    if 99 < volume < 500:
        row = 1
    elif 0 < volume // 500 < 7:
        row = (3 + volume // 500) // 2
    elif volume > 3499:
        row = 5

    if 249 < distance and distance // 500 < 5:
        column = 1 + distance // 500
    elif distance > 2999:
        column = 6

    return cement_table[int(row)][int(column)]


def pue_asbestos(volume: float, distance: float, height: float):
    if distance < 250:
        return 3
    elif distance < 500:
        return 2
    return 1


def pue_other_materials(volume: float, distance: float, height: float):
    if distance < 250:
        return 2
    return 1


# 1.9.10 mechanical engineering
def pue_car(volume: float, distance: float, height: float):
    if distance < 500:
        return 2
    return 1


# 1.9.12 mining of ores and non-metallic minerals
def pue_iron_mining(volume: float, distance: float, height: float):
    if distance < 250:
        return 2
    return 1


def pue_coal_mining(volume: float, distance: float, height: float):
    if distance < 250:
        return 3
    elif distance < 500:
        return 2
    return 1


# 1.9.13 thermal power plants and boiler houses
def pue_tes_coal(volume: float, distance: float, height: float):
    if volume > 999 and distance < 500:
        return 2
    elif volume > 999 and distance < 1000 and height < 180:
        return 2
    return 1


def pue_tes_slate(volume: float, distance: float, height: float):
    if volume < 500:
        if distance < 250:
            return 3
        elif distance < 1500:
            return 2
        return 1

    if distance > 2999:
        return 1
    elif distance > 499:
        return 2
    elif distance > 249:
        return 3
    elif height < 180:
        return 4
    return 3


# 1.9.14 landfills, warehouses
def pue_tbo(distance: float):
    if distance < 200:
        return 3
    elif distance < 600:
        return 2
    return 1


# add


def add_pue_road(lat: float, lon: float, roads: pd.DataFrame):
    """Add values to the 'pue' column"""
    for index in roads.index:
        distance = dst.nearest2road(lat, lon, roads.iloc[index]['geometry'])[0]
        roads.loc[index, 'pue'] = pue_road(distance)
    return roads


def add_pue_industrial(lat: float, lon: float, industrials: pd.DataFrame):
    """Add values to the 'pue' column"""
    dict_pue = {'chemistry':  pue_chemistry, 'cellulose': pue_cellulose,
                'paper': pue_paper, 'steel': pue_ferrous_metallurgy_1,
                'mount': pue_ferrous_metallurgy_2, 'aluminum': pue_aluminum,
                'coke_chemical': pue_ferrous_metallurgy_3, 'tbo': pue_tbo,
                'color_metal': pue_color_metals, 'cement': pue_cement,
                'asbestos': pue_asbestos, 'concrete': pue_other_materials,
                'car': pue_car, 'iron_mining': pue_iron_mining,
                'coal_mining': pue_coal_mining, 'boiler_slate': pue_tes_slate,
                'boiler_coal': pue_tes_coal, 'rera_metal': pue_rare_metals,
                'bricks': pue_other_materials,
                }

    for index in industrials.index:
        geometry = industrials.iloc[index]['geometry']
        distance = dst.nearest2polygon(lat, lon, geometry)
        product = industrials.iloc[index]['product']

        if pd.isnull(product) or product == '':
            rank = 0
        else:
            func = dict_pue[product]
            rank = func(industrials.iloc[index]['production_volume'], distance,
                        industrials.iloc[index]['height_chimney'])

        industrials.loc[index, 'pue'] = rank

    return industrials


def road_score(data: pd.DataFrame, month: int):
    """Add values to the 'rank' column based on traffic congestion.
    For Moscow
    """
    lat, lon = 55.7522, 37.6156
    # MKAD - TTK : 20 km - 5.5
    score_big = [4.6, 4.5, 4.7, 4.7, 4.5, 4.3, 3.7, 4, 4.6, 4.8, 5, 5.4]
    # TTK - Sadovoye 5.5 - 2.5
    score_midlle = [4.5, 4.9, 5.1, 5.6, 5.6, 6.1, 5.1, 4.9, 4.9, 5.4, 5.7, 6]
    # Inside the Sadovoye
    score_small = [4.8, 5.6, 6.4, 7.4, 7.7, 8, 7.6, 7.3, 6.2, 6.5, 6.1, 6.8]

    for index in data.index:
        distance = dst.nearest2road(lat, lon, data.iloc[index]['geometry'])[0]
        if distance < 2500:
            data.loc[index, 'rank'] = score_small[month-1]
        elif distance < 5500:
            data.loc[index, 'rank'] = score_midlle[month-1]
        elif distance < 20000:
            data.loc[index, 'rank'] = score_big[month-1]

    return data
