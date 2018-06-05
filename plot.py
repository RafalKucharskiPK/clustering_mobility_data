
PLOTLY_API_KEY = "w1LROCX3bYA8amfuLA4g"

import matplotlib.pyplot as plt
import plotly.graph_objs as go

import plotly
from plotly.graph_objs import Data, Scattermapbox, Marker, Layout, Line
import plotly.plotly as py
import pandas as pd
import colorlover


# UTILS
def config_plotly():
    plotly.tools.set_config_file(world_readable=True,
                                 sharing='public')
    plotly.tools.set_credentials_file(username='rkucharski',
                                      api_key=PLOTLY_API_KEY)



# PLOTS
def plot_vectors(days, peak="PM"):
    _scaler = 6
    config_plotly()

    color_scale = colorlover.scales['5']['qual']['Dark2']

    data = list()
    top_size = days['7'].max()
    for index, row in days.iterrows():
        desc = str(index) + " cluster_id" + str(row['cluster_id'])
        data.append(Scattermapbox(
            lat=[row["Start_Lat_mean" + peak], row["End_Lat_mean" + peak]],
            lon=[row["Start_Lon_mean" + peak], row["End_Lon_mean" + peak]],
            mode='lines',
            text=desc,
            name=desc,
            opacity = 0.7,
            line=Line(width=int(_scaler * row['7']/top_size),
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
    top_size = days['7'].max()
    for cluster in days.cluster_id.unique():
        data.append(Scattermapbox(
            lat=days[days.cluster_id == cluster][param + "_Lat_mean" + peak],
            lon=days[days.cluster_id == cluster][param + "_Lon_mean" + peak],
            mode='markers',
            marker=Marker(
                size=days[days.cluster_id == cluster]['7'] / top_size * marker_size_scale,
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
