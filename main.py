import geopandas as gpd
import pandas as pd
import osmapi
import improver
import distancer
import scorer


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

# data = pd.read_excel('wind_roses.xlsx')
# dict = improver.create_wind_roses(data, 5)
# data_industrial = osmapi.choose_source(54.90404, 38.08035, 5000)
# print(dict)
# improver.determine_direction(54.90404, 38.08035, data_industrial, dict)
# gdata = gpd.GeoDataFrame(data_industrial, crs="EPSG:4326", geometry='geometry')
# d = gdata.explore()
# d.save("wind_roses_map.html")

data = pd.read_excel('list_pylons.xlsx')
new_data = data.drop_duplicates(subset=['latitude', 'longitude'],
                                ignore_index=True)

count = 0
print(new_data)
for index in new_data.index:
    count += 1
    lat = new_data.iloc[index]['latitude']
    lon = new_data.iloc[index]['longitude']
    data_industrial = osmapi.choose_source(lat, lon, 5000)
    data_chimney = osmapi.chimney_table(lat, lon, 5000)
    data_road = osmapi.road_table(lat, lon, 2500, 1000)
    data_city = osmapi.city_table(lat, lon, 3000)

    data_industrial = distancer.add_distance2polygon(lat, lon, data_industrial)
    data_chimney = distancer.add_distance2polygon(lat, lon, data_chimney)
    data_road = distancer.add_distance2road(lat, lon, data_road)
    print(data_road)

    data_industrial, data_chimney = improver.clarify_location(data_industrial,
                                                              data_chimney)

    improver.road_accounting(data_road, lat, lon, 200, 500, 1000)
    improver.city_accounting(lat, lon, 5000, data_city,
                             data_road, data_industrial)

    #print(data_industrial)
    # data_industrial.to_excel(f'industrial_{count}.xlsx')
    # data_road.to_excel(f'road_{count}.xlsx')

    #dict_wind = improver.create_wind_roses(data_wind, n*4)
    #improver.wind_accounting(lat, lon, data_road, dict_wind)
    #improver.wind_accounting(lat, lon, data_industrial, dict_wind)

    scorer.road_score(data_road, 5)
    scorer.add_pue_industrial(lat, lon, data_industrial)
    scorer.add_pue_road(lat, lon, data_road)
