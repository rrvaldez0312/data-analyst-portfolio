import pandas as pd
import numpy as np
import datetime as dt

#reading csv files

file_list=[r'C:\Users\rrval\Desktop\CyclisticTripData\tripdata_csv\202207-divvy-tripdata.csv',
           r'C:\Users\rrval\Desktop\CyclisticTripData\tripdata_csv\202208-divvy-tripdata.csv',
           r'C:\Users\rrval\Desktop\CyclisticTripData\tripdata_csv\202209-divvy-publictripdata.csv',
           r'C:\Users\rrval\Desktop\CyclisticTripData\tripdata_csv\202210-divvy-tripdata.csv',
           r'C:\Users\rrval\Desktop\CyclisticTripData\tripdata_csv\202211-divvy-tripdata.csv',
           r'C:\Users\rrval\Desktop\CyclisticTripData\tripdata_csv\202212-divvy-tripdata.csv',
           r'C:\Users\rrval\Desktop\CyclisticTripData\tripdata_csv\202301-divvy-tripdata.csv',
           r'C:\Users\rrval\Desktop\CyclisticTripData\tripdata_csv\202302-divvy-tripdata.csv',
           r'C:\Users\rrval\Desktop\CyclisticTripData\tripdata_csv\202303-divvy-tripdata.csv',
           r'C:\Users\rrval\Desktop\CyclisticTripData\tripdata_csv\202304-divvy-tripdata.csv',
           r'C:\Users\rrval\Desktop\CyclisticTripData\tripdata_csv\202305-divvy-tripdata.csv',
           r'C:\Users\rrval\Desktop\CyclisticTripData\tripdata_csv\202306-divvy-tripdata.csv']


whole_tripdata = pd.DataFrame(pd.read_csv(file_list[0]))

for i in range(1, len(file_list)):
    data = pd.read_csv(file_list[i])
    df = pd.DataFrame(data)
    whole_tripdata = pd.concat([whole_tripdata, df])

# 
main_tripdata = pd.DataFrame(whole_tripdata, columns=['ride_id','started_at','ended_at','member_casual','ride_length','day_of_week','ride_length_seconds'])

# data transformations

# convert days to readable days

weekday_dict = {
    '1' : 'Sunday',
    '2' : 'Monday',
    '3' : 'Tuesday',
    '4' : 'Wednesday',
    '5' : 'Thursday',
    '6' : 'Friday',
    '7' : 'Saturday'
}

main_tripdata.day_of_week = main_tripdata.day_of_week.astype('str')
main_tripdata.day_of_week = main_tripdata.day_of_week.map(weekday_dict)

# split up start time from start date
main_tripdata.started_at = main_tripdata.started_at.astype('str')
main_tripdata[['start_date', 'start_time']] = main_tripdata.started_at.str.split(" ", expand=True)

# split up end time from end date
# (is there a bike trip that started on one date and ended on another?)

main_tripdata.ended_at = main_tripdata.ended_at.astype('str')
main_tripdata[['end_date', 'end_time']] = main_tripdata.ended_at.str.split(" ", expand=True)

# extract month of trips

month_dict = {
    '1' : 'January',
    '2' : 'February',
    '3' : 'March',
    '4' : 'April',
    '5' : 'May',
    '6' : 'June',
    '7' : 'July',
    '8' : 'August',
    '9' : 'September',
    '10' : 'October',
    '11' : 'November',
    '12' : 'December'
}

date_tripdata = main_tripdata.copy()
date_tripdata[["month","day","year"]] = date_tripdata["start_date"].str.extract("(\d+)/(\d+)/(\d+)").astype(int)
date_tripdata.month = date_tripdata.month.astype('str')
date_tripdata.month = date_tripdata.month.map(month_dict)

# drop any columns that were made unecessary

date_tripdata = date_tripdata.drop(columns=['started_at', 'ended_at', 'day', 'year'])
main_tripdata = date_tripdata.copy()
# print(main_tripdata.sample(5))


main_tripdata.to_csv('202207-to-202306-main-tripdata.csv')
