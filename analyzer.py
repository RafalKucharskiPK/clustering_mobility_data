import pandas as pd
import os
import matplotlib as plt
import requests
import ssl
import zipfile


AM = [8, 9]
PM = [16, 17, 18, 19]


def zip_url_to_df(url):
    """
    downloads the data from a given url (ssl needed)
    save it and unzip
    load csv to pandas dataframe
    :param url:
    :return: pandas DataFrame with jodi data from csv
    """
    req = requests.get(url, auth=ssl.CERT_NONE)  # the url is under https so we need empty ssl certificate
    file_name = "temp.zip"  # we get zipped file
    file = open(file_name, 'wb')  # we save the http response to file
    for chunk in req.iter_content(100000):
        file.write(chunk)
    file.close()

    zip_ref = zipfile.ZipFile(file_name, 'r')  # and unzip it
    csv_file_name = zip_ref.filelist[0].filename  # we assume only one csv per .zip

    zip_ref.extractall()
    zip_ref.close()
    os.remove(file_name)  # we delete the .zip file (the csv remains on disk)
    df = index_by_datetime(pd.read_csv(csv_file_name),  date_col="starttime",format="%m/%d/%Y %H:%M:%S")
    os.remove(csv_file_name)
    return df


def index_by_datetime(_df, date_col=None,format = None):
    """
    changes a given column data type to datetime
    and overwrites this as an index.
    :param _df:
    :param date_col: column where date is stored
    :return: transformed data frame
    :param format: optional format if known, makes the prcess way faster
    :return:
    """
    if date_col is None:
        _df.index = pd.to_datetime(_df.index, format=format)
    else:
        _df[date_col] = pd.to_datetime(_df[date_col], format=format)
        _df.index = _df[date_col]
        del _df[date_col]
    return _df


def read_urls(urls, plot = False):
    _df = list()
    x = list()
    y = list()
    for url in urls:
        _df.append(zip_url_to_df(url))
        x.append(url)
        y.append(_df[-1].shape[0])
        print("Reading  {:,} trips recorded on {}".format(
            _df[-1].shape[0],
            url))
    _df = pd.concat(_df)

    if plot:
        plt.bar([i for i, x in enumerate(y)], y)
        plt.xticks([i for i, x in enumerate(y)], x)
        plt.ylabel('number of bike rents')
        plt.ylabel('months')
        plt.show()

    del _df['stoptime']
    del _df['start station name']
    del _df['end station name']
    return _df

def describe_trip_groups(_trips, groups='days'):
    """
    Here we descripbe the days from the trips table
    :param _trips: pd.DataFrame
    :return: pd.DataFrame
    """
    if groups == 'days':
        by1 = [_trips.index.date, _trips.index.hour]
        by2 = [_trips.index.date]
        pivot_index = "date"
    elif groups == 'clusters':
        by1 = [_trips.cluster_id, _trips.index.hour]
        by2 = [_trips.cluster_id]
        pivot_index = "cluster_id"
    else:
        raise KeyError

    hours = _trips[['bikeid']].groupby(by=by1).count()  # total trips per day,  hour
    hours = hours.reset_index()  # flatten the multiindex pandas data frame
    hours.columns = [pivot_index, "hour", "trips"]  # make understandable index names
    days = hours.pivot(index=pivot_index, columns='hour', values='trips')  # use hours as columns (fields)
    days['totals'] = _trips[['bikeid']].groupby(by=by2).count()  # add totals

    if groups == 'days':
        days.index = pd.to_datetime(days.index)
        days["weekday"] = days.index.dayofweek

    cols = ["Start_Lon", "Start_Lat", "End_Lon", "End_Lat"]
    if groups == "days":
        _trip_pos = _trips[['start station longitude',
                            'start station latitude',
                            'end station longitude',
                            'end station latitude']]  # filter only of od LonLat's
    else:
        _trip_pos = _trips[[pivot_index,
                            'start station longitude',
                            'start station latitude',
                            'end station longitude',
                            'end station latitude']]  # filter only of od LonLat's

    prefix = ""
    # for daily ; AM and PM peaks
    for s in [_trip_pos,
              _trip_pos[(AM[0] <= _trip_pos.index.hour) & (_trip_pos.index.hour <= AM[-1])],
              _trip_pos[(PM[0] <= _trip_pos.index.hour) & (_trip_pos.index.hour <= PM[-1])]]:
        if groups == "days":
            group = s.groupby(by=s.index.date)
        else:
            group = s.groupby(by='cluster_id')
        # calc center of gravity and moment of inertia per origin and destination
        for a in ["_mean", "_std"]:
            if a == "_mean":
                p = group.mean().reset_index()
            else:
                p = group.std().reset_index()
            if groups == 'days':
                p.index = pd.to_datetime(p["index"])
                del p["index"]
            else:
                p.index = p.cluster_id
                del p["cluster_id"]
            p.columns = [c + a + prefix for c in cols]

            days = pd.concat([days, p], axis=1)
        if prefix == "":
            prefix = "AM"
        else:
            prefix = "PM"

    col_dict = dict()
    for i, col in enumerate(days.columns):
        col_dict[i] = col
    col_dict_invert = {v: k for k, v in col_dict.items()}

    return days, col_dict, col_dict_invert

if __name__ == "__main__":
    urls = [ "https://s3.amazonaws.com/tripdata/2017{}-citibike-tripdata.csv.zip".format(str(i).zfill(2)) for i in range(1,13)]
    df = read_urls(["https://s3.amazonaws.com/tripdata/201804-citibike-tripdata.csv.zip"])
    #df = read_urls(urls)
    print(df.head())
    print(df.shape)