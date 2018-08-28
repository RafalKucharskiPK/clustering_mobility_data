from plot import *
from holidays import *
from cluster import *

from config import *
from analyzer import prepare, describe_trip_groups


def visualize(_plotly=False,_plot=True):
    days = pd.read_csv(CLUSTERED_DAYS_PATH_OUT)

    # results
    cls = days.cluster_id.unique()

    # prepare rows
    cols = [str(i) for i in range(24)]

    # prepare figures
    fig, axes = plt.subplots(nrows=len(cls), ncols=1)
    pyplot_data = list()
    if _plotly:
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
    if _plot:
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
    days = pd.read_csv(CLUSTERED_DAYS_PATH_OUT)
    config_plotly()
    plot_vectors(days, peak="AM")  # plot vectors