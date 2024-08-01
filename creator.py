import pandas as pd
import distancer as dst
import osmapi
import improver
import scorer


def take_coord(list_pylons_name: str):
    """Create DataFrame from list of pylons table.
    Return two DataFrames:
    1) full_data - all data from table
    2) new_data - data grouped by coordinates. Each pylon is present once
    """
    full_data = pd.read_excel(list_pylons_name)
    new_data = full_data.drop_duplicates(subset=['latitude', 'longitude'],
                                         ignore_index=True)
    return full_data, new_data


def take_industrials(data: pd.DataFrame) -> None:
    """Use pylons DataFrame to create industrial tables.
    You can change this data before proceeding.
    All tables are saved in the current directory
    with the name "industrial_*.xlsx"
    """
    count = 0
    for index in data.index:
        count += 1
        lat = data.iloc[index]['latitude']
        lon = data.iloc[index]['longitude']
        data_industrial = osmapi.industrial_table(lat, lon, 5000)
        data_industrial.to_excel(f'industrial_{count}.xlsx')

    return None


def create_data(data: pd.DataFrame):
    """Use pylons DataFrame to create tables of pollution sources.
    All tables are saved in the current directory
    with the name "full_industrial_*.xlsx" and "road_*.xlsx".
    You can enter the product volumes first
    """
    data_wind = pd.read_excel('wind_roses.xlsx')
    dict_wind = improver.create_wind_roses(data_wind, 6)

    count = 0   # counter only for table name
    for index in data.index:
        count += 1
        lat = data.iloc[index]['latitude']
        lon = data.iloc[index]['longitude']

        # you cannot read 'geometry' from excel. so it is necessary
        # to correlate the data with the osm and the entered data
        your_industrial = pd.read_excel(f'industrial_{count}.xlsx')
        osm_industrial = osmapi.industrial_table(lat, lon, 5000)
        for index in your_industrial.index:
            value_product = your_industrial.loc[index, 'production_volume']
            osm_industrial.loc[index, 'production_volume'] = value_product
            name_product = your_industrial.loc[index, 'product']
            osm_industrial.loc[index, 'product'] = name_product

        # join other sources with your entered data
        data_other = osmapi.choose_source(lat, lon, 5000)
        data_indust = pd.concat([osm_industrial, data_other])

        # add DataFrames about chimney, road and city
        data_chimney = osmapi.chimney_table(lat, lon, 5000)
        data_road = osmapi.road_table(lat, lon, 2500, 1000)
        data_city = osmapi.city_table(lat, lon, 3000)

        # add distance to objects
        data_indust = dst.add_distance2polygon(lat, lon, data_indust)
        data_chimney = dst.add_distance2polygon(lat, lon, data_chimney)
        data_road = dst.add_distance2road(lat, lon, data_road)

        # add clarifying points to buildings
        data_indust, data_chimney = improver.clarify_location(data_indust,
                                                              data_chimney)

        # add information about road area
        data_road = improver.road_accounting(data_road, lat, lon,
                                             200, 500, 1000)

        # add information about the nearest city and industrial buildings
        _,  data_road, data_indust = improver.city_accounting(lat, lon,
                                                              5000,
                                                              data_city,
                                                              data_road,
                                                              data_indust)

        # add pue score
        data_road = scorer.road_score(data_road, 5)
        data_road = scorer.add_pue_road(lat, lon, data_road)
        data_indust = scorer.add_pue_industrial(lat, lon, data_indust)

        # add information about wind
        data_road = improver.wind_accounting(lat, lon, data_road, dict_wind)
        data_indust = improver.wind_accounting(lat, lon, data_indust,
                                               dict_wind)

        # sort for easy viewing
        data_road.sort_values(by=['distance'], inplace=True,
                              ignore_index=True,)
        data_indust.sort_values(by=['type'], inplace=True,
                                ignore_index=True,)

        # create excel files
        data_indust.to_excel(f'full_industrial_{count}.xlsx')
        data_road.to_excel(f'road_{count}.xlsx')

    return data_indust, data_road


def create_all_data(list_pylons_name: str):
    """Use pylons DataFrame to create tables of pollution sources.
    All tables are saved in the current directory
    with the name "full_industrial_*.xlsx" and "road_*.xlsx".
    You cannot enter the product volumes first
    """
    data_wind = pd.read_excel('wind_roses.xlsx')
    dict_wind = improver.create_wind_roses(data_wind, 6)

    full_data = pd.read_excel(list_pylons_name)
    data = full_data.drop_duplicates(subset=['latitude', 'longitude'],
                                     ignore_index=True)
    count = 0
    for index in data.index:
        count += 1
        lat = data.iloc[index]['latitude']
        lon = data.iloc[index]['longitude']

        # add DataFrame about dirty polygons (without roads)
        data_industrial = osmapi.industrial_table(lat, lon, 5000)
        data_other = osmapi.choose_source(lat, lon, 5000)
        data_indust = pd.concat([data_industrial, data_other])

        # add DataFrames about chimney, road and city
        data_chimney = osmapi.chimney_table(lat, lon, 5000)
        data_road = osmapi.road_table(lat, lon, 2500, 1000)
        data_city = osmapi.city_table(lat, lon, 3000)

        # add distance to objects
        data_indust = dst.add_distance2polygon(lat, lon, data_indust)
        data_chimney = dst.add_distance2polygon(lat, lon, data_chimney)
        data_road = dst.add_distance2road(lat, lon, data_road)

        # add clarifying points to buildings
        data_indust, data_chimney = improver.clarify_location(data_indust,
                                                              data_chimney)

        # add information about road area
        data_road = improver.road_accounting(data_road, lat, lon,
                                             200, 500, 1000)

        # add information about the nearest city and industrial buildings
        _,  data_road, data_indust = improver.city_accounting(lat, lon,
                                                              5000,
                                                              data_city,
                                                              data_road,
                                                              data_indust)

        # add pue score
        data_road = scorer.road_score(data_road, 5)
        data_road = scorer.add_pue_road(lat, lon, data_road)
        data_indust = scorer.add_pue_industrial(lat, lon, data_indust)

        # add information about wind
        data_road = improver.wind_accounting(lat, lon, data_road, dict_wind)
        data_indust = improver.wind_accounting(lat, lon, data_indust,
                                               dict_wind)

        # sort for easy viewing
        data_road.sort_values(by=['distance'], inplace=True,
                              ignore_index=True,)
        data_indust.sort_values(by=['type'], inplace=True,
                                ignore_index=True,)

        # create excel files
        data_indust.to_excel(f'full_industrial_{count}.xlsx')
        data_road.to_excel(f'road_{count}.xlsx')

    return data_indust, data_road
