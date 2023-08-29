# transforming dataset using python

import pandas as pd

from kaggle.api.kaggle_api_extended import KaggleApi

api = KaggleApi()
api.authenticate()

# downloading dataset from kaggle using the Kaggle API
api.dataset_download_file('hmavrodiev/london-bike-sharing-dataset',
                          file_name='london_merged.csv')

# read csv file as a pandas dataframe
bikes = pd.read_csv("london_merged.csv")

# rename the columns to make readability easier
new_cols_dict ={
    'timestamp' : 'time',
    'cnt' : 'count',
    't1' : 'temp_real_C',
    't2' : 'temp_feels_like_C',
    'hum' : 'humidity_percent',
    'wind_speed' : 'wind_speed_kph',
    'weather_code' : 'weather',
    'is_holiday' : 'is_holiday',
    'is_weekend' : 'is_weekend',
    'season' : 'season'
}

bikes.rename(new_cols_dict, axis=1, inplace=True)

# convert humidity_percent to an actual percent
bikes.humidity_percent = bikes.humidity_percent / 100

# define season values
season_dict = {
    '0.0' : 'spring',
    '1.0' : 'summer',
    '2.0' : 'autumn',
    '3.0' : 'winter'
}

# define weather values
weather_dict = {
    '1.0' : 'Clear',
    '2.0' : 'Scattered clouds',
    '3.0' : 'Broken clouds',
    '4.0' : 'Cloudy',
    '7.0' : 'Rain',
    '10.0' : 'Rain with thunderstorm',
    '26.0' : 'Snowfall'
}

# rename season values using dictionary
bikes.season = bikes.season.astype('str')
bikes.season = bikes.season.map(season_dict)

# rename weather values using dictionary
bikes.weather = bikes.weather.astype('str')
bikes.weather = bikes.weather.map(weather_dict)

# export transformed data to an excel file
bikes.to_excel('london_bikes_final.xlsx', sheet_name='Data')
