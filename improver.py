import distancer as dst
import pandas as pd
import numpy as np
import math
from shapely.geometry import Point, LineString, Polygon, \
                             MultiLineString, MultiPoint, \
                             MultiPolygon


def calculate_production_volume(data: pd.DataFrame):
    """Updating production volumes based on capacity.
    Using when merging databases
    """
    recount = data.groupby('name').count()
    count = list(recount['geometry'])
    resum = data[['power', 'name']].groupby('name').sum()
    sum = list(resum['power'])

    for i in range(len(count)):
        # if there is no information at all
        if count[i] != 1 and sum[i] == -count[i]:
            producte_volume = list(data[data.name == resum.index[i]]
                                   ['production_volume'])[0]
            value = producte_volume / count[i]
            data.loc[data.name == resum.index[i], 'power'] = 100 / count[i]
            data.loc[data.name == resum.index[i], 'production_volume'] = value
        # if all or part of the information is available
        elif sum[i] < 101:
            # got all the lines of this object
            lines = data[data.name == resum.index[i]]
            indexes = list(lines.index)
            unknown_indexes = []   # chimneys for which the capacity is unknown
            all_power = 0   # the counter of the share of the recorded power
            # fill in the known ones and save the unknown ones
            for index in indexes:
                if data.iloc[index]['power'] != -1:
                    prd = data.iloc[index]['production_volume']
                    pwr = data.iloc[index]['power']
                    all_power += data.iloc[index]['power']
                    data.loc[index, 'production_volume'] = prd * pwr / 100
                else:
                    unknown_indexes.append(index)

            # filling in the unknown
            for index in unknown_indexes:
                data.loc[data.index == index, 'power'] = (100-all_power) \
                                                         / len(unknown_indexes)
                prd = data.iloc[index]['production_volume']
                pwr = data.iloc[index]['power']
                value = prd * pwr / 100
                data.loc[data.index == index, 'production_volume'] = value

        else:
            index = data[data.name == resum.index[i]].index[0]
            print(f'''Incorrect data: Невозможно посчитать с номера {index}''')

    return data


def clarify_location(buildings: pd.DataFrame, chimneys: pd.DataFrame):
    """Merge the base to industrial buildings and chimney"""
    buildings.sort_values(by=['distance'], ascending=False,
                          inplace=True, ignore_index=True)
    chimneys.sort_values(by=['distance'], ascending=False,
                         inplace=True, ignore_index=True)

    sorted_chimneys = chimneys[[
        'height', 'geometry', 'point_type', 'lat', 'lon', 'distance', 'power',
    ]]

    sorted_buildings = buildings[[
        'element_type', 'geometry', 'name', 'lat', 'lon', 'type',
        'distance', 'production_volume', 'product',
    ]]

    sorted_buildings["height_chimney"] = np.nan
    sorted_buildings["power"] = -1.0

    count_b, len_b = 0, len(sorted_buildings)
    while count_b < len_b:  # go through all the buildings

        count_c = 0
        chimneys_before = len(sorted_chimneys)
        # and through all the chimneys that have not yet been distributed
        while count_c < len(sorted_chimneys) and len(sorted_chimneys) != 0:

            chimney_c = sorted_chimneys.iloc[count_c]
            building_b = sorted_buildings.iloc[count_b]
            size = len(sorted_buildings.index)

            if (building_b.geometry).intersects(chimney_c.geometry):
                sorted_buildings.loc[size] = building_b
                sorted_buildings.loc[size, "lat"] = chimney_c.lat
                sorted_buildings.loc[size, "lon"] = chimney_c.lon
                sorted_buildings.loc[size, "height_chimney"] = chimney_c.height
                sorted_buildings.loc[size, "distance"] = chimney_c.distance
                sorted_buildings.loc[size, "type"] = chimney_c.point_type
                sorted_buildings.loc[size, "power"] = chimney_c.power
                sorted_chimneys = sorted_chimneys.drop([count_c])
                sorted_chimneys.reset_index(drop=True, inplace=True)

            else:
                count_c += 1   # moving on to the next chimney

        chimneys_after = len(sorted_chimneys)
        # delete the line with information about the building
        # if a chimney has been added
        if chimneys_before - chimneys_after > 0:
            sorted_buildings = sorted_buildings.drop([count_b])
            sorted_buildings.reset_index(drop=True, inplace=True)
        else:
            count_b += 1

    sorted_buildings = calculate_production_volume(sorted_buildings)
    sorted_buildings['pue'] = np.nan
    return sorted_buildings, sorted_chimneys


def update_production_volume(data: pd.DataFrame, name: str, value: float):
    """Recalculation of production volumes when
    making changes in production volumes"""
    for index in data[data.name == name].index:
        pwr = data.iloc[index]['power']
        data.loc[index, 'production_volume'] = value * pwr / 100
    return data


def lenght(lnstr):
    """Returns the length of the line
    lnstr - LineString or MultiLineString"""
    ans = 0
    if lnstr.geom_type == 'LineString':
        x1, y1 = lnstr.coords.xy[1][0], lnstr.coords.xy[0][0]
        for x, y in zip(lnstr.coords.xy[1], lnstr.coords.xy[0]):
            ans += dst.nearest2point(x, y, x1, y1)
            x1, y1 = x, y
    else:
        for line in lnstr.geoms:
            x1, y1 = line.coords.xy[1][0], line.coords.xy[0][0]
            for x, y in zip(line.coords.xy[1], line.coords.xy[0]):
                ans += dst.nearest2point(x, y, x1, y1)
                x1, y1 = x, y
    return ans


def create_circle(lat: float, lon: float, radius: float):
    """Returns a ring at a point (lat, lon) with a specified radius"""
    lenght_of_arc = 2*math.pi*radius
    parts = int(lenght_of_arc/50)
    points_of_circle = []
    for i in range(parts+1):
        # the equation of the circle in polar coordinates
        x = lat + radius*0.00000916*math.cos(2*i*math.pi/parts)
        y = lon + radius*0.00000916*math.sin(2*i*math.pi/parts) \
            / math.cos(lat*math.pi/180)
        points_of_circle.append(Point(y, x))
    return Polygon(points_of_circle)


def road_accounting(data: pd.DataFrame, lat: float, lon: float,
                    m1: float, m2: float, m3: float):
    """Parameters:
    lat, lon - geographic latitude and longitude
    m1, m2, m3 - the radius of the small, medium and large circles in meters

    Adds two columns to the DataFrame: the circle into which it enters in
    descending order ("circle") and area of the road that enters it ("area")
    """
    data.dropna(subset=['lanes'], inplace=True)
    data.reset_index(drop=True, inplace=True)
    dst.add_distance2road(lat, lon, data)
    # create a empty DataFrame
    new_data = pd.DataFrame(columns=data.columns)
    # and new columns
    new_data['circle'] = pd.Series(dtype='int')
    new_data['area'] = pd.Series(dtype='float')
    circle1 = create_circle(lat, lon, m1)
    circle2 = create_circle(lat, lon, m2)
    circle3 = create_circle(lat, lon, m3)
    for index in data.index:
        # go through all the lines of the old DataFrame
        lnstr = data.iloc[index]['geometry']
        line1 = lnstr.intersection(circle1)
        line2 = lnstr.intersection(circle2)
        line3 = lnstr.intersection(circle3)
        s1 = data.iloc[index]
        # small radius
        if data.iloc[index]['distance'] < m1:
            area = 4 * int(data.iloc[index]['lanes']) * int(lenght(line1))
            s2 = pd.Series({'circle': 4, 'area': area})
            new_data.loc[len(new_data)] = pd.concat([s1, s2])
        # medium radius
        if data.iloc[index]['distance'] < m2:
            line = line2.difference(line1)
            if not line.is_empty:
                area = 4 * int(data.iloc[index]['lanes']) * int(lenght(line))
                s2 = pd.Series({'circle': 3, 'area': area})
                new_data.loc[len(new_data)] = pd.concat([s1, s2])
        # big radius
        if data.iloc[index]['distance'] < m3:
            line = line3.difference(line2)
            if not line.is_empty:
                area = 4 * int(data.iloc[index]['lanes']) * int(lenght(line))
                s2 = pd.Series({'circle': 2, 'area': area})
                new_data.loc[len(new_data)] = pd.concat([s1, s2])
        # other
        line = lnstr.difference(line3)
        if not line.is_empty:
            area = 4 * int(data.iloc[index]['lanes']) * int(lenght(line))
            s2 = pd.Series({'circle': 1, 'area': area})
            new_data.loc[len(new_data)] = pd.concat([s1, s2])

    new_data.reset_index(drop=True, inplace=True)
    return new_data


def create_lines(lat: float, lon: float, radius: float):
    """Returns a line circle (as a sun) with a specified radius"""
    lines_of_circle = []
    for i in range(36):
        # the equation of the circle in polar coordinates
        x = lat + radius*0.00000916*math.cos(2*i*math.pi/36)
        y = lon + radius*0.00000916*math.sin(2*i*math.pi/36) \
            / math.cos(math.radians(lat))
        lines_of_circle.append(LineString([Point(lon, lat),
                                           Point(y, x)]))
    return MultiLineString(lines_of_circle)


def distance2intersection(latitude: float, longitude: float,
                          intersection: MultiPoint):
    temp_dist = 1000
    for point in intersection.geoms:
        now_dist = dst.nearest2point(point.coords[0][1],
                                     point.coords[0][0],
                                     latitude, longitude)
        if now_dist < temp_dist:
            temp_dist = now_dist
    return temp_dist


def city_accounting(latitude: float, longitude: float, radius: float,
                    data_city: pd.DataFrame, data_road: pd.DataFrame,
                    data_industrial: pd.DataFrame):
    """Сhecks whether the source of pollution is in the urban environment"""
    # number of buildings at the intersection
    data_road['city'] = 0
    data_industrial['city'] = 0
    # number of industrial buildings at the intersection
    data_road['ind'] = 0
    data_industrial['ind'] = 0
    # number of levels in buildings at the intersection
    data_road['levels'] = ''
    data_industrial['levels'] = ''

    lines = create_lines(latitude, longitude, radius)
    for line in lines.geoms:
        # distance to the point of intersection with the line
        dict_road = pd.DataFrame(columns=['index', 'temp_dist', 'type'])
        dict_industrial = pd.DataFrame(columns=['index', 'temp_dist', 'type'])
        dict_city = pd.DataFrame(columns=['index', 'temp_dist', 'type'])

        for index in data_city.index:
            geometry = data_city.iloc[index].geometry
            insct = geometry.boundary.intersection(line)
            if insct.geom_type == 'MultiPoint':
                temp_dist = distance2intersection(latitude, longitude, insct)
                dict_city.loc[len(dict_city)] = [index, temp_dist, 'city']

        for index in data_industrial.index:
            geometry = data_industrial.iloc[index].geometry
            insct = geometry.boundary.intersection(line)
            if insct.geom_type == 'MultiPoint':
                temp_dist = distance2intersection(latitude, longitude, insct)
                dict_industrial.loc[len(dict_industrial)] = [index, temp_dist,
                                                             'industrial']
            elif insct.geom_type == 'Point':
                temp_dist = dst.nearest2point(insct.coords[0][1],
                                              insct.coords[0][0],
                                              latitude, longitude)
                dict_industrial.loc[len(dict_industrial)] = [index, temp_dist,
                                                             'industrial']

        for index in data_road.index:
            geometry = data_road.iloc[index].geometry
            insct = geometry.intersection(line)
            if (not insct.is_empty) and insct.geom_type == 'Point':
                temp_dist = dst.nearest2point(insct.coords[0][1],
                                              insct.coords[0][0],
                                              latitude, longitude)
                dict_road.loc[len(dict_road)] = [index, temp_dist, 'road']

            elif insct.geom_type == 'MultiPoint':
                temp_dist = distance2intersection(latitude, longitude, insct)
                dict_road.loc[len(dict_road)] = [index, temp_dist, 'road']

        dict = pd.concat([dict_road, dict_city, dict_industrial])
        dict.sort_values(by=['temp_dist'], ascending=True,
                         inplace=True, ignore_index=True)

        city, ind, levels = 0, 0, ''
        for index in dict.index:
            i = dict.iloc[index]['index']
            if dict.iloc[index]['type'] == 'industrial':
                data_industrial.loc[i, 'city'] += city
                data_industrial.loc[i, 'ind'] += ind
                data_industrial.loc[i, 'levels'] += levels
                ind += 1
            elif dict.iloc[index]['type'] == 'road':
                data_road.loc[i, 'city'] += city
                data_road.loc[i, 'ind'] += ind
                data_road.loc[i, 'levels'] += levels
            else:
                city += 1
                level = data_city.iloc[i]['building:levels']
                if level is not np.nan:
                    levels += f'{level}_'

    return data_city, data_road, data_industrial


def create_nsew(latitude: float, longitude: float, radius: float = 10000):
    """Returns a line circle (as a sun) for different sides of world"""
    polygons_of_circle = []
    for i in range(16):
        # the equation of the circle in polar coordinates
        # find the points for polygon
        x_old = latitude + radius*0.00000916*math.cos(2*i*math.pi/16)
        y_old = longitude + radius*0.00000916*math.sin(2*i*math.pi/16) \
            / math.cos(math.radians(latitude))
        x_new = latitude + radius*0.00000916*math.cos(2*(i+1)*math.pi/16)
        y_new = longitude + radius*0.00000916*math.sin(2*(i+1)*math.pi/16) \
            / math.cos(math.radians(latitude))

        polygons_of_circle.append(Polygon([Point(longitude, latitude),
                                           Point(y_old, x_old),
                                           Point(y_new, x_new)]))
    return MultiPolygon(polygons_of_circle)


def create_wind_roses(data: pd.DataFrame, index: int):
    """Creates a dictionary from the values of the table row about the winds"""
    dict_wind_rose = {}
    for column, value in zip(data.columns, data.iloc[index]):
        dict_wind_rose[column] = value
    return dict_wind_rose


def wind_accounting(latitude: float, longitude: float, data: pd.DataFrame,
                    dict_wind_rose: dict):
    """Determines the side of the world relative to the source of
    polution for the isolator, specified by coordinates"""
    # correlate the polygon index with the side
    # but these are the sides set in inverted order
    # so that the wind rose can be easily applied.
    # There should N-E-S-W
    dict_nsew = {0: 'S', 1: 'SSW', 2: 'SW', 3: 'WSW',
                 4: 'W', 5: 'WNW', 6: 'NW', 7: 'NNW',
                 8: 'N', 9: 'NNE', 10: 'NE', 11: 'ENE',
                 12: 'E', 13: 'ESE', 14: 'SE', 15: 'SSE'}
    data['nsew'] = np.nan
    data['nsew_factor'] = np.nan
    # go through all the lines in the sources of pollution
    nsew = create_nsew(latitude, longitude)
    for index in data.index:
        geometry = data.iloc[index]['geometry']
        sides, count = [], 0
        for polygon in nsew.geoms:
            if geometry.intersects(polygon):
                sides.append(count)
            count += 1
        # if the object is located in the North
        if 15 in sides and 0 in sides:
            count_after, count_before = 0, 0
            for number in sides:
                count_before += 1 if number < 8 else 0
                count_after += 1 if number > 7 else 0
            sides = list(range(16-count_after, 16)) \
                + list(range(0, count_before))

        # the name of the side of the world
        side_value = dict_nsew[(sides[-1]-len(sides)//2 + 1) % 16]
        data.loc[index, 'nsew'] = side_value
        data.loc[index, 'nsew_factor'] = dict_wind_rose[side_value]

    return data
