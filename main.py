# import geopandas as gpdpi
import pandas as pd
import creator


# gdata = gpd.GeoDataFrame(data_industrial, crs="EPSG:4326",
#                         geometry='geometry')
# d = gdata.explore()
# d.save("map.html")

d = creator.create_all_data('list_pylons.xlsx')
print('i am Dima')