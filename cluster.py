'''
# cl: 3
# 2016-07-08 https://www.wunderground.com/history/airport/KNYC/2016/7/8/DailyHistory.html?req_city=New+York&req_state=NY&req_statename=New+York&reqdb.zip=10001&reqdb.magic=8&reqdb.wmo=99999

# cl: 2
# 2016-06-22 https://www.wunderground.com/history/airport/KNYC/2016/6/22/DailyHistory.html?req_city=New+York&req_state=NY&req_statename=New+York&reqdb.zip=10001&reqdb.magic=8&reqdb.wmo=99999
'''


import numpy as np

from scipy.stats.stats import pearsonr

from sklearn import metrics
from sklearn.cluster import AgglomerativeClustering
from scipy.spatial.distance import cosine


def cl_metrics(df_mtx, clusters):
    labels = clusters.labels_
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

    metric = dict()
    metric['nclusters'] = n_clusters_
    metric['silhouette'] = metrics.silhouette_score(df_mtx, labels)
    metric['calinski_harabaz'] = metrics.calinski_harabaz_score(df_mtx, labels)

    print(metric)

    # print('Estimated number of clusters: %d' % n_clusters_)
    # print("Silhouette Coefficient: %0.3f"
    #       % metrics.silhouette_score(df_mtx, labels))




#CLUSTERING METHODS
def cluster_agglomeration(df, n_clusters):
    df_mtx = df.as_matrix()
    # metric = metrics.pairwise.pairwise_kernels(days, metric=my_dist)
    clusters = AgglomerativeClustering(n_clusters=n_clusters, affinity=custom_affinity, linkage = 'average')
    clusters = clusters.fit(df_mtx)
    cl_metrics(df_mtx,clusters)
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
    # w.append(1.0)module 'holidays' has no attribute 'UnitedStates'

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

