

AM = [8, 9]
PM = [16, 17, 18, 19]


TRIPS_PATH_IN = "trips.csv"
DAYS_PATH_IN = "days_in.csv"
CLUSTERED_DAYS_PATH_OUT = "days_out.csv"

URLS = ["https://s3.amazonaws.com/tripdata/2018{}-citibike-tripdata.csv.zip".format(str(i).zfill(2)) for i in range(1, 7)]
URL = ["https://s3.amazonaws.com/tripdata/201804-citibike-tripdata.csv.zip"]

TIME_FORMAT = "%Y/%m/%d %H:%M:%S"