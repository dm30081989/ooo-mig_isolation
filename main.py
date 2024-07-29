import geopandas as gpd
import pandas as pd
import osmapi
import improver
import webbrowser

# data_city = osmapi.city_table(54.90404, 38.08035, radius=5000)
# data_industrial = osmapi.choose_source(54.90404, 38.08035, 5000)
# data_road = osmapi.road_table(54.90404, 38.08035, small_radius=5000,
#                               big_radius=5000)

# data_city, data_road, data_industrial = improver.score_of_city(54.90404, 38.08035, 5000, data_city, data_road, data_industrial)

# lines = improver.create_lines(54.90404, 38.08035, 5000)
# print(data_industrial.shape)
# for line in lines.geoms:
#     data_industrial.loc[len(data_industrial)] = [0, 0, line, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# gdata = gpd.GeoDataFrame(data_industrial, crs="EPSG:4326", geometry='geometry')
# d = gdata.explore()
# d.save("map.html")
# webbrowser.open("map.html")

data = pd.read_excel('wind_roses.xlsx')
dict = improver.create_wind_roses(data, 5)
data_industrial = osmapi.choose_source(54.90404, 38.08035, 5000)
print(dict)
improver.determine_direction(54.90404, 38.08035, data_industrial, dict)
gdata = gpd.GeoDataFrame(data_industrial, crs="EPSG:4326", geometry='geometry')
d = gdata.explore()
d.save("wind_roses_map.html")
