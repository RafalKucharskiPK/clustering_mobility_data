'''
# cl: 3
# 2016-07-08 https://www.wunderground.com/history/airport/KNYC/2016/7/8/DailyHistory.html?req_city=New+York&req_state=NY&req_statename=New+York&reqdb.zip=10001&reqdb.magic=8&reqdb.wmo=99999

# cl: 2
# 2016-06-22 https://www.wunderground.com/history/airport/KNYC/2016/6/22/DailyHistory.html?req_city=New+York&req_state=NY&req_statename=New+York&reqdb.zip=10001&reqdb.magic=8&reqdb.wmo=99999
'''


import matplotlib.pyplot as plt
import plotly.graph_objs as go
import holidays
import numpy as np
import plotly
from plotly.graph_objs import Data, Scattermapbox, Marker, Layout, Line
import plotly.plotly as py
import pandas as pd
import colorlover
from scipy.stats.stats import pearsonr

from sklearn import metrics
from sklearn.cluster import AgglomerativeClustering
from scipy.spatial.distance import cosine


PLOTLY_API_KEY = "w1LROCX3bYA8amfuLA4g"
DB_PATH = "/Users/rafal/Google Drive/data/store.h5"


# UTILS
def config_plotly():
    plotly.tools.set_config_file(world_readable=True,
                                 sharing='public')
    plotly.tools.set_credentials_file(username='rkucharski',
                                      api_key=PLOTLY_API_KEY)


def read_from_hdf():
    return pd.HDFStore(DB_PATH)


# PLOTS
def plot_vectors(days, peak="PM"):
    _scaler = 6
    config_plotly()

    color_scale = colorlover.scales['5']['qual']['Dark2']

    data = list()
    top_size = days[7].max()
    for index, row in days.iterrows():
        desc = str(index) + " cluster_id" + str(row['cluster_id'])
        data.append(Scattermapbox(
            lat=[row["Start_Lat_mean" + peak], row["End_Lat_mean" + peak]],
            lon=[row["Start_Lon_mean" + peak], row["End_Lon_mean" + peak]],
            mode='lines',
            text=desc,
            name=desc,
            opacity = 0.7,
            line=Line(width=int(_scaler * row[7]/top_size),
                      color=color_scale[int(row['cluster_id'])])))

    data = Data(data)

    layout = Layout(
        showlegend=False,
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken=PLOTLY_API_KEY,
            bearing=0,
            center=dict(
                lat=row["Start_Lat_mean" + peak],
                lon=row["Start_Lon_mean" + peak]
            ),
            pitch=0,
            zoom=11
        ),
    )

    fig = dict(data=data, layout=layout)
    py.plot(fig, filename='Vectors ' + peak)


def plot_cluster(days, param="End", peak="AM", marker_size_scale=30):
    config_plotly()

    color_scale = colorlover.scales['5']['qual']['Set1']

    data = list()
    top_size = days[7].max()
    for cluster in days.cluster_id.unique():
        data.append(Scattermapbox(
            lat=days[days.cluster_id == cluster][param + "_Lat_mean" + peak],
            lon=days[days.cluster_id == cluster][param + "_Lon_mean" + peak],
            mode='markers',
            marker=Marker(
                size=days[days.cluster_id == cluster][7] / top_size * marker_size_scale,
                color=color_scale[cluster]
            ),
            text="CL: "+str(cluster),
            hoverinfo='text'
        ))

    data = Data(data)

    layout = Layout(
        title='Clusters centres of gravity:' + param + peak,
        autosize=True,
        hovermode='closest',
        showlegend=False,
        mapbox=dict(
            accesstoken=PLOTLY_API_KEY,
            bearing=0,
            center=dict(
                lat=40,
                lon=-73
            ),
            pitch=0,
            zoom=7,
            style='light'
        ),
    )
    fig = dict(data=data, layout=layout)
    py.plot(fig, filename='Clusters:' + param + peak)

#CLUSTERING METHODS
def cluster_agglomeration(df, n_clusters):
    df_mtx = df.as_matrix()
    # metric = metrics.pairwise.pairwise_kernels(days, metric=my_dist)
    clusters = AgglomerativeClustering(n_clusters=n_clusters, affinity=custom_affinity, linkage = 'average')
    clusters = clusters.fit(df_mtx)
    labels = clusters.labels_
    df["cluster_id"] = labels

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

    print('Estimated number of clusters: %d' % n_clusters_)
    print("Silhouette Coefficient: %0.3f"
          % metrics.silhouette_score(df_mtx, labels))
    return df, metrics.silhouette_score(df_mtx, labels)


def custom_affinity(M):
    return np.array([[custom_distance_function(o,d) for o in M] for d in M])

def custom_distance_function(o, d):
    """
    24      'totals',
    25      'Start_Lon_mean', 'Start_Lat_mean',
    27      'End_Lon_mean', 'End_Lat_mean',
    29      'Start_Lon_std', 'Start_Lat_std',
    31      'End_Lon_std', 'End_Lat_std',
    33      'Start_Lon_meanAM', 'Start_Lat_meanAM',
    35      'End_Lon_meanAM','End_Lat_meanAM',
    37      'Start_Lon_stdAM', 'Start_Lat_stdAM',
    39      'End_Lon_stdAM', 'End_Lat_stdAM',
    41      'Start_Lon_meanPM', 'Start_Lat_meanPM',
    43      'End_Lon_meanPM', 'End_Lat_meanPM',
    45      'Start_Lon_stdPM', 'Start_Lat_stdPM',
    47      'End_Lon_stdPM','End_Lat_stdPM'
    :param o:
    :param d:
    :return:
    """
    x = list()  # values
    w = list()  # weights
    x.append(pearsonr(o[:24], d[:24])[0])  # r2 between time profiles
    w.append(0)  # weight

    x.append(abs((o[24] - d[24])) / float(d[24]))  # relative distance between totals
    w.append(0)  # weight

    # x.append(cosine_vect(o, d))
    # w.append(0.5)

    x.append(cosine_vect(o, d, 35))
    w.append(1)

    x.append(cosine_vect(o, d, 43))
    w.append(1)

    # x.append(day_type_distance(o[49], d[49]))
    # w.append(0.0)

    # # Start AM Lon Lat
    # x.append(geo_distance(o, d, 33))
    # w.append(1.0)
    #
    # # End AM Lon Lat
    # x.append(geo_distance(o, d, 35))
    # w.append(1.0)
    #
    # # Start PM Lon Lat
    # x.append(geo_distance(o, d, 45))
    # w.append(1.0)
    #
    # # End PM Lon Lat
    # x.append(geo_distance(o, d, 47))
    # w.append(1.0)

    return np.dot(x, w)


def cosine_vect(o, d, index):
    # compute cosine similarity between two vectors
    deltaLonAM = o[index] - o[index-2]
    deltaLatAM = o[index+1] - o[index-1]

    day1_vect = [deltaLonAM, deltaLatAM]
    deltaLonAM = d[index] - d[index-2]
    deltaLatAM = d[index+1] - d[index-1]

    day2_vect = [deltaLonAM, deltaLatAM]
    return cosine(day1_vect, day2_vect)


#MAIN PROCEDURE
def main():
    days = cluster_agglomeration(dfs['days'], 5)[0]

    days['holidays'] = make_holidays(days)
    days.to_csv("clustered_days.csv")
    ssw

    # resulting clusters
    cls = days.cluster_id.unique()
    print(cls)

    # prepare rows
    cols = [i for i in range(24)]

    # prepare figures
    fig, axes = plt.subplots(nrows=len(cls), ncols=1)
    pyplot_data = list()
    config_plotly()

    # plotly holidays.
    for cl in cls:
        cld = days['holidays'][days.cluster_id == cl]
        pyplot_data.append(go.Box(y=cld,
                                  name=cl,
                                  jitter=0.3,
                                  pointpos=-1.8,
                                  boxpoints='all'
                                  )
                           )
    py.plot(pyplot_data, filename="Clusters holidays")

    #plotly days of week
    for cl in cls:
         cld = days['weekday'][days.cluster_id == cl]
         pyplot_data.append(go.Box(y=cld,
                                   name=cl,
                                   jitter=0.3,
                                   pointpos=-1.8,
                                   boxpoints='all'
                                   )
                            )
    py.plot(pyplot_data, filename="Clusters days of week")


    #plotly totals
    pyplot_data = list()
    config_plotly()
    for cl in cls:
        cld = days['totals'][days.cluster_id == cl]
        pyplot_data.append(go.Box(y=cld,
                                  name=cl,
                                  jitter=0.3,
                                  pointpos=-1.8,
                                  boxpoints='all'
                                  )
                           )
    py.plot(pyplot_data, filename="Clusters total trips")

    plot_vectors(days, peak = "AM")  # plot vectors
    plot_vectors(days, peak = "PM")  # plot vectors
    plot_cluster(days, param="Start", peak = "AM")  # plot clusters
    plot_cluster(days, param="Start", peak = "PM")  # plot clusters
    plot_cluster(days, param="End", peak = "AM")  # plot clusters
    plot_cluster(days, param="End", peak = "PM")  # plot clusters

    i = 0
    # cld = days['totals'][days.cluster_id == cl]
    for cl in cls:
        days[cols][days.cluster_id == cl].T.plot(ax=axes[i], c='black', legend=False, lw=0.2)
        axes[i].set_ylabel("trips", fontsize=8)
        axes[i].set_title("cluster " + str(cl), fontsize=8)
        i += 1
    axes[-1].set_xlabel("h", fontsize=8)

    plt.show()
    dfs.close()


def make_holidays(days):
    us_holidays = holidays.UnitedStates()

    def assign_holiday(row):
        if row.name in us_holidays or row.weekday == 6:
            return "Holiday, Sunday"
        if row.weekday == 5:
            return "Saturday"
        else:
            return "Working Day"

    return days.apply(lambda x: assign_holiday(x), axis = 1)


if __name__ == "__main__":
    # read hdf
    dfs = read_from_hdf()
    main()

