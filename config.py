

AM = [8, 9]
PM = [16, 17, 18, 19]


TRIPS_PATH_IN = "trips.csv"
DAYS_PATH_IN = "days_in.csv"
CLUSTERED_DAYS_PATH_OUT = "days_out.csv"

WEATHER_DATA="weather_data.csv"
DECOMPOSED_DAYS_PATH_OUT="days_out.csv"
PREDICTION_MODEL="Prediction.csv"
PREDICTION_MODEL_T="Prediction_with_Temperature.csv"
DAY_TO_PREDICT = "days_to_predict.csv"
PREDICTION_RESULTS = "Results.csv"
FULL_DATABASE='days_all.csv'

URLS = ["https://s3.amazonaws.com/tripdata/2018{}-citibike-tripdata.csv.zip".format(str(i).zfill(2))
        for i in range(1, 11)]
URL = ["https://s3.amazonaws.com/tripdata/201804-citibike-tripdata.csv.zip"]

TIME_FORMAT = "%Y/%m/%d %H:%M:%S"

#INPUTS WEATHER DATA
NW_class=5;                                                                     # How many sub-clusters you want to create based on the weather data

#SEASONS
Spring=['3/1/2016','5/31/2016']
Summer=['6/1/2016','8/31/2016']
Autumn=['9/1/2016','30/11/2016']
Winter=['12/1/2016','28/1/2017']