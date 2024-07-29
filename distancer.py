import math
from shapely.geometry import Point, LineString, MultiLineString, Polygon, MultiPolygon


def deg2rad(deg):
    return deg * math.pi/180


def koef(lat1: float, lon1: float, lat2: float, lon2: float):
    """ Two-point interpolation.

    Parameters
    _____________
    a_x - coefficient at x
    b_y - coefficient at y
    c - free coefficient
    """
    if lat2 == lat1:
        return 1, 0, -lat1
    if lon2 == lon1:
        return 0, 1, -lon1

    a_x = 1/(lat2-lat1)
    b_y = -1/(lon2-lon1)
    c = -lat1/(lat2-lat1) + lon1/(lon2-lon1)
    return a_x, b_y, c


def is_iterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False


def nearest2point(lat1: float, lon1: float, lat2: float, lon2: float):
    """Finds the distance between two points on the earth's surface"""
    R = 6371000  # radius of the earth in m
    lat_dif = deg2rad(lat2-lat1)
    lon_dif = deg2rad(lon2-lon1)
    a = math.sin(lat_dif/2) * math.sin(lat_dif/2) + \
        math.cos(deg2rad(lat1)) * math.cos(deg2rad(lat2)) * \
        math.sin(lon_dif/2) * math.sin(lon_dif/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c
    return distance


def nearest2line(lat: float, lon: float, line: LineString):
    """Finds the minimum distance between a point and a line
    and returns the coordinate of the intersection point"""
    min_dist, min_coord = 5000, 0
    xs, ys = [], []

    for x, y in zip(line.coords.xy[1], line.coords.xy[0]):
        xs.append(x)
        ys.append(y)

    count = 0

    while count < len(xs)-1:   # go through all the sections
        # approximate each section
        a_x, b_y, c = koef(xs[count], ys[count], xs[count+1], ys[count+1])
        temp_x = xs[count]
        # as long as the next point is at a distance of > 10 meters
        # from the last one
        while abs(temp_x - xs[count+1]) >= 0.0000916:
            temp_y = (-a_x*temp_x - c)/b_y
            dist = nearest2point(lat, lon, temp_x, temp_y)

            if dist < min_dist:
                min_dist = dist
                min_coord = Point(temp_x, temp_y)
            # moving on to the next point
            if temp_x < xs[count+1]:
                temp_x += 0.0000916
            else:
                temp_x -= 0.0000916

        count += 1

    return min_dist, min_coord


def nearest2road(lat: float, lon: float, road):
    """Finds the minimum distance between a point and a linestring
    and returns the coordinate of the intersection point"""
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


def nearest2polygon(lat: float, lon: float, building):
    building_lat, building_lon = building.centroid.y, building.centroid.x
    return nearest2point(lat, lon, building_lat, building_lon)


def add_distance2polygon(lat: float, lon: float, data):
    '''Add a column to the data with the distance to the support,
    which is set in coordinates. For buildings.'''
    data['distance'] = 0
    data = data.reset_index()

    for index in data.index:
        geometry = data.iloc[index]['geometry']
        data.loc[index, 'distance'] = int(nearest2polygon(lat, lon, geometry))
    return None


def add_distance2road(lat: float, lon: float, data):
    '''Add a column to the data with the distance to the support,
    which is set in coordinates. For roads.'''
    data['distance'] = 0
    data = data.reset_index()

    for index in data.index:
        geometry = data.iloc[index]['geometry']
        data.loc[index, 'distance'] = int(nearest2road(lat, lon, geometry))
    return None
