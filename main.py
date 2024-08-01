# import geopandas as gpd
import pandas as pd
import creator


# gdata = gpd.GeoDataFrame(data_industrial, crs="EPSG:4326",
#                          geometry='geometry')
# d = gdata.explore()
# d.save("map.html")


# creator.take_industrials(data)
creator.create_all_data("list_pylons.xlsx")
