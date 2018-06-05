from plot import *
from holidays import *
from cluster import *


DAYS_PATH_IN = "days_in.csv"
CLUSTERED_DAYS_PATH_OUT = "days_out.csv"


#MAIN PROCEDURE
def main():
    # read
    df = pd.read_csv(DAYS_PATH_IN)
    df = df.set_index(df['index'])
    del df['index']

    col_dict = dict()
    for i, col in enumerate(df.columns):
        col_dict[i] = col
    col_dict_invert = {v: k for k, v in col_dict.items()}
    print(col_dict)
    print(col_dict_invert)
    quit()

    # cluster
    days = cluster_agglomeration(df, 5)[0]
    days['holidays'] = make_holidays(days)

    # save
    days.to_csv(CLUSTERED_DAYS_PATH_OUT)

    # results
    cls = days.cluster_id.unique()
    print(cls)

    # prepare rows
    cols = [str(i) for i in range(24)]

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
    pyplot_data = list()
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





if __name__ == "__main__":
    main()

