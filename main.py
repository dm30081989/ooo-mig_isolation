# import geopandas as gpd
import pandas as pd
import creator


# gdata = gpd.GeoDataFrame(data_industrial, crs="EPSG:4326",
#                          geometry='geometry')
# d = gdata.explore()
# d.save("map.html")


d = creator.create_all_data('list_pylons.xlsx')
d.to_excel('data.xlsx')
# ааааааааааааааааа
# ЗАМЕЧАНИЯ ПО ПУЭ:
# scorer - ранги присваиваются после деления. должно быть наоборот