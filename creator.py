import pandas as pd
import distancer as dst
import osmapi
import improver
import scorer


def take_coord(list_pylons_name: str) -> pd.DataFrame:
    full_data = pd.read_excel(list_pylons_name)
    new_data = full_data.drop_duplicates(subset=['latitude', 'longitude'],
                                         ignore_index=True)
    return full_data, new_data


def take_industrials(data: pd.DataFrame) -> None:
    count = 0
    for index in data.index:
        count += 1
        lat = data.iloc[index]['latitude']
        lon = data.iloc[index]['longitude']
        data_industrial = osmapi.industrial_table(lat, lon, 5000)
        data_industrial.to_excel(f'industrial_{count}.xlsx')

    return None


def create_data(data: pd.DataFrame) -> None:
    data_wind = pd.read_excel('wind_roses.xlsx')
    dict_wind = improver.create_wind_roses(data_wind, 6)

    count = 0
    for index in data.index:
        count += 1
        lat = data.iloc[index]['latitude']
        lon = data.iloc[index]['longitude']

        your_data_industrial = pd.read_excel(f'industrial_{count}.xlsx')
        osm_data_industrial = osmapi.industrial_table(lat, lon, 5000)
        for index in your_data_industrial.index:
            value_product = your_data_industrial.loc[index, 'production_volume']
            osm_data_industrial.loc[index, 'production_volume'] = value_product
            name_product = your_data_industrial.loc[index, 'product']
            osm_data_industrial.loc[index, 'product'] = name_product

        data_other = osmapi.choose_source(lat, lon, 5000)
        data_indust = pd.concat([osm_data_industrial, data_other])

        data_chimney = osmapi.chimney_table(lat, lon, 5000)
        data_road = osmapi.road_table(lat, lon, 2500, 1000)
        data_city = osmapi.city_table(lat, lon, 3000)

        data_indust = dst.add_distance2polygon(lat, lon, data_indust)
        data_chimney = dst.add_distance2polygon(lat, lon, data_chimney)
        data_road = dst.add_distance2road(lat, lon, data_road)

        data_indust, data_chimney = improver.clarify_location(data_indust,
                                                              data_chimney)

        data_road = improver.road_accounting(data_road, lat, lon,
                                             200, 500, 1000)

        _,  data_road, data_indust = improver.city_accounting(lat, lon,
                                                              5000,
                                                              data_city,
                                                              data_road,
                                                              data_indust)

        data_road = scorer.road_score(data_road, 5)
        data_road = scorer.add_pue_road(lat, lon, data_road)
        data_indust = scorer.add_pue_industrial(lat, lon, data_indust)

        data_road = improver.wind_accounting(lat, lon, data_road, dict_wind)
        data_indust = improver.wind_accounting(lat, lon, data_indust,
                                               dict_wind)

        data_road.sort_values(by=['distance'], inplace=True,
                              ignore_index=True,)
        data_indust.sort_values(by=['type'], inplace=True,
                                ignore_index=True,)

        data_indust.to_excel(f'full_industrial_{count}.xlsx')
        data_road.to_excel(f'road_{count}.xlsx')

    return None


def create_all_data(list_pylons_name: str) -> None:
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

        data_industrial = osmapi.industrial_table(lat, lon, 5000)
        data_other = osmapi.choose_source(lat, lon, 5000)
        data_indust = pd.concat([data_industrial, data_other])

        data_chimney = osmapi.chimney_table(lat, lon, 5000)
        data_road = osmapi.road_table(lat, lon, 2500, 1000)
        data_city = osmapi.city_table(lat, lon, 3000)

        data_indust = dst.add_distance2polygon(lat, lon, data_indust)
        data_chimney = dst.add_distance2polygon(lat, lon, data_chimney)
        data_road = dst.add_distance2road(lat, lon, data_road)

        data_indust, data_chimney = improver.clarify_location(data_indust,
                                                              data_chimney)

        data_road = improver.road_accounting(data_road, lat, lon,
                                             200, 500, 1000)

        _,  data_road, data_indust = improver.city_accounting(lat, lon,
                                                              5000,
                                                              data_city,
                                                              data_road,
                                                              data_indust)

        data_road = scorer.road_score(data_road, 5)
        data_road = scorer.add_pue_road(lat, lon, data_road)
        data_indust = scorer.add_pue_industrial(lat, lon, data_indust)

        data_road = improver.wind_accounting(lat, lon, data_road, dict_wind)
        data_indust = improver.wind_accounting(lat, lon, data_indust,
                                               dict_wind)

        data_road.sort_values(by=['distance'], inplace=True,
                              ignore_index=True,)
        data_indust.sort_values(by=['type'], inplace=True,
                                ignore_index=True,)

        data_indust.to_excel(f'full_industrial_{count}.xlsx')
        data_road.to_excel(f'road_{count}.xlsx')

    return None
