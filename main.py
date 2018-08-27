from plot import *
from holidays import *
from cluster import *
from visualizer import *

from config import *
from analyzer import prepare, describe_trip_groups


#MAIN PROCEDURE
def make_clusters(_n=6):
    # read
    df = pd.read_csv(DAYS_PATH_IN)
    df = df.set_index(df['index'])
    df.drop('2018-03-21', axis = 0, inplace=True)
    df.drop('2018-03-22', axis = 0, inplace = True)
    df.fillna(0, inplace = True)
    del df['index']
    null_columns = df.columns[df.isnull().any()]
    #print(null_columns)
    #print(df[df.isnull().any(axis=1)][null_columns].head())
    for null_column in null_columns:
        print("Missing value of \t{}\t on \t{}".format(null_column,df[df[null_column].isnull()].index.values[0]))

    # cluster
    # for i in range(3,9):
    #     days = cluster_agglomeration(df, i)[0]
    # quit()
    days = cluster_agglomeration(df, _n)[0]
    days['holidays'] = make_holidays(days)

    # save
    days.to_csv(CLUSTERED_DAYS_PATH_OUT)

    cls = days.cluster_id.unique()
    print(cls)
    return days




if __name__ == "__main__":
    #prepare()
    describe_trip_groups()
    make_clusters(6)
    visualize()

