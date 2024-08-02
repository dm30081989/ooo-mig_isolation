import pandas as pd


def det_index(data: pd.DataFrame, row: str, col: str) -> int:
    series = data[data.index == row]
    if len(series):
        return round(series.iloc[0][col], 2)
    return 0


def det_type(data: pd.DataFrame, row: str, col: str) -> int:
    series = data[data.type == row]
    if not series.empty:
        return round(series.iloc[0][col], 2)
    return 0


def det_road(data: pd.DataFrame, col: str) -> int:
    if not data.empty:
        return round(data.iloc[0][col], 2)
    return 0


def indust2series(data: pd.DataFrame) -> pd.Series:
    data.sort_values(by=['distance'], inplace=True, ignore_index=True)
    type = data.groupby(by=['type'], sort=False)
    mean = type.mean(numeric_only=True)
    sum = type.sum(numeric_only=True)
    count = type.count()

    dict_series = {'industrial': det_index(count, 'industrial', 'geometry') \
                   + det_index(count, 'chimney', 'geometry'),
                   'farmland': det_index(count, 'farmland', 'geometry'),
                   'forest': det_index(count, 'forest', 'geometry') \
                   + det_index(count, 'wood', 'geometry'),
                   'landfill': det_index(count, 'landfill', 'geometry'),
                   'query': det_index(count, 'query', 'geometry'),

                   'ind_dist_mn': det_index(mean, 'industrial', 'distance') \
                   + det_index(mean, 'chimney', 'distance'),
                   'farm_dist_mn': det_index(mean, 'farmland', 'distance'),
                   'for_dist_mn': det_index(mean, 'forest', 'distance') \
                   + det_index(mean, 'wood', 'distance'),
                   'land_dist_mn': det_index(mean, 'landfill', 'distance'),
                   'que_dist_mn': det_index(mean, 'query', 'distance'),

                   'ind_area_s': det_index(sum, 'industrial', 'area') \
                   + det_index(sum, 'chimney', 'area'),
                   'farm_area_s': det_index(sum, 'farmland', 'area'),
                   'for_area_s': det_index(sum, 'forest', 'area') \
                   + det_index(sum, 'wood', 'area'),
                   'land_area_s': det_index(sum, 'landfill', 'area'),
                   'que_area_s': det_index(sum, 'query', 'area'),

                   'ind_wind_mn': det_index(mean, 'industrial', 'nsew_factor') \
                   + det_index(mean, 'chimney', 'nsew_factor'),
                   'farm_wind_mn': det_index(mean, 'farmland', 'nsew_factor'),
                   'for_wind_mn': det_index(mean, 'forest', 'nsew_factor') \
                   + det_index(mean, 'wood', 'nsew_factor'),
                   'land_wind_mn': det_index(mean, 'landfill', 'nsew_factor'),
                   'que_wind_mn': det_index(mean, 'query', 'nsew_factor'),

                   'ind_city_mn': det_index(mean, 'industrial', 'city') \
                   + det_index(mean, 'chimney', 'city'),
                   'farm_city_mn': det_index(mean, 'farmland', 'city'),
                   'for_city_mn': det_index(mean, 'forest', 'city') \
                   + det_index(mean, 'wood', 'city'),
                   'land_city_mn': det_index(mean, 'landfill', 'city'),
                   'que_city_mn': det_index(mean, 'query', 'city'),

                   'ind_dirty_mn': det_index(mean, 'industrial', 'ind') \
                   + det_index(mean, 'chimney', 'ind'),
                   'farm_dirty_mn': det_index(mean, 'farmland', 'ind'),
                   'for_dirty_mn': det_index(mean, 'forest', 'ind') \
                   + det_index(mean, 'wood', 'ind'),
                   'land_dirty_mn': det_index(mean, 'landfill', 'ind'),
                   'que_dirty_mn': det_index(mean, 'query', 'ind'),

                   'ind_level_mn': det_index(mean, 'industrial', 'mean_level') \
                   + det_index(mean, 'chimney', 'mean_level'),
                   'farm_level_mn': det_index(mean, 'farmland', 'mean_level'),
                   'for_level_mn': det_index(mean, 'forest', 'mean_level') \
                   + det_index(mean, 'wood', 'mean_level'),
                   'land_level_mn': det_index(mean, 'landfill', 'mean_level'),
                   'que_level_mn': det_index(mean, 'query', 'mean_level'),

                   'ind_pue_mn': det_index(mean, 'industrial', 'pue') \
                   + det_index(mean, 'chimney', 'pue'),
                   'farm_pue_mn': det_index(mean, 'farmland', 'pue'),
                   'for_pue_mn': det_index(mean, 'forest', 'pue') \
                   + det_index(mean, 'wood', 'pue'),
                   'land_pue_mn': det_index(mean, 'landfill', 'pue'),
                   'que_pue_mn': det_index(mean, 'query', 'pue'),

                    # top-1 distance
                   'ind_dist_min': det_type(data, 'industrial', 'distance'),
                   'land_dist_min': det_type(data, 'landfill', 'distance'),
                   'que_dist_min': det_type(data, 'query', 'distance'),
                   'ind_wind_min': det_type(data, 'industrial', 'nsew_factor'),
                   'land_wind_min': det_type(data, 'landfill', 'nsew_factor'),
                   'que_wind_min': det_type(data, 'query', 'nsew_factor'),

                   '': '',
                   '': '',
                   '': '',
                   '': '',
                   '': '',
                   }

    return pd.Series(dict_series)


def road2series(data: pd.DataFrame) -> pd.Series:

    type = data.groupby(by=['circle'], sort=False)
    mean = type.mean(numeric_only=True)
    sum = type.sum(numeric_only=True)

    dict_series = {'road1_area_s': det_index(sum, 4, 'area'),
                   'road2_area_s': det_index(sum, 3, 'area'),
                   'road3_area_s': det_index(sum, 2, 'area'),
                   'road4_area_s': det_index(sum, 1, 'area'),

                   'road1_dist_mn': det_index(mean, 4, 'distance'),
                   'road2_dist_mn': det_index(mean, 3, 'distance'),
                   'road3_dist_mn': det_index(mean, 2, 'distance'),
                   'road4_dist_mn': det_index(mean, 1, 'distance'),

                   'road1_rank_mn': det_index(mean, 4, 'rank'),
                   'road2_rank_mn': det_index(mean, 3, 'rank'),
                   'road3_rank_mn': det_index(mean, 2, 'rank'),
                   'road4_rank_mn': det_index(mean, 1, 'rank'),

                   'road1_city_mn': det_index(mean, 4, 'city'),
                   'road2_city_mn': det_index(mean, 3, 'city'),
                   'road3_city_mn': det_index(mean, 2, 'city'),
                   'road4_city_mn': det_index(mean, 1, 'city'),

                   'road1_ind_mn': det_index(mean, 4, 'ind'),
                   'road2_ind_mn': det_index(mean, 3, 'ind'),
                   'road3_ind_mn': det_index(mean, 2, 'ind'),
                   'road4_ind_mn': det_index(mean, 1, 'ind'),

                   'road1_level_mn': det_index(mean, 4, 'mean_level'),
                   'road2_level_mn': det_index(mean, 3, 'mean_level'),
                   'road3_level_mn': det_index(mean, 2, 'mean_level'),
                   'road4_level_mn': det_index(mean, 1, 'mean_level'),

                   'road1_wind_mn': det_index(mean, 4, 'nsew_factor'),
                   'road2_wind_mn': det_index(mean, 3, 'nsew_factor'),
                   'road3_wind_mn': det_index(mean, 2, 'nsew_factor'),
                   'road4_wind_mn': det_index(mean, 1, 'nsew_factor'),

                    # top-1 distance
                   'road_dist_min': det_road(data, 'distance'),
                   'road_wind_min': det_road(data, 'nsew_factor'),

                   '': '',
                   '': '',
                   '': '',
                   '': '',
                   '': '',
                }

    return pd.Series(dict_series)
