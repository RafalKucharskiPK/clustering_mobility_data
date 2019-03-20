import pandas as pd
import numpy as np
from config import *

def Prediction_Model(Cv2=False):
    if Cv2==False:
        days = pd.read_csv(DECOMPOSED_DAYS_PATH_OUT)
    else:        
        days = pd.read_csv(DECOMPOSED_DAYS_PATH_OUT)
        days['cluster_id']=days['Cv2']
            
    # results
    cls = days.cluster_id.unique()
    # Perpare prediction model
    y = [str(i) for i in range(28)]
    y[24]='Temperature'
    y[25]='Season'
    y[26]='cluster_id'
    y[27]='cluster_size'
    x=np.arange(0,len(cls))
    prediction_model=pd.DataFrame(index=x, columns=y)
    # prepare rows
    cols = [str(i) for i in range(24)]
    k=0
    for cl in cls:
        prediction_model.loc[k][cols]=np.mean(days[cols][days.cluster_id == cl])
        prediction_model.loc[k]['Temperature']=np.mean(days['Temperature'][days.cluster_id == cl])
        prediction_model.loc[k]['Season']=np.mean(days['Season'][days.cluster_id == cl])
        prediction_model.loc[k]['cluster_id']=np.mean(days['cluster_id'][days.cluster_id == cl])
        prediction_model.loc[k]['cluster_size']=len(days[cols][days.cluster_id == cl])
        k=k+1

    if Cv2==False:
        prediction_model.to_csv(PREDICTION_MODEL)
    else:
        prediction_model.to_csv(PREDICTION_MODEL_T)
        
        
def Prediction_Error(DAYDATA, Cv2=False, S=1):
    if Cv2==False:
        prediction=pd.read_csv(PREDICTION_MODEL)
    else:
        prediction=pd.read_csv(PREDICTION_MODEL_T)
    days = pd.read_csv(DECOMPOSED_DAYS_PATH_OUT)        
    
    prediction_cluster=round(np.mean(days.cluster_id[days.holidays==DAYDATA.holidays]))
    cols = [str(i) for i in range(24)]
    observed_demand=DAYDATA[cols]
    if Cv2==False:
        predicted_demand=prediction[cols][prediction.cluster_id==prediction_cluster]
    else:
        #prediction_cluster_tmp=np.mean(days.Cv2[days.Temperature==DAYDATA.Temperature][days.Season==S][days.cluster_id==prediction_cluster])
        prediction_cluster_tmp=np.mean(days.Cv2[days.Temperature==DAYDATA.Temperature][days.cluster_id==prediction_cluster])
        predicted_demand=prediction[cols][prediction.cluster_id==prediction_cluster_tmp]
        prediction_cluster=prediction_cluster_tmp
    
    predicted_demand=np.array(predicted_demand)
    observed_demand=np.array(observed_demand)
    if np.isnan(prediction_cluster)==False:
        error=(predicted_demand[0]-observed_demand)*(predicted_demand[0]-observed_demand)
        RMSE=np.sqrt(sum(error)/error.size);
    else:
        RMSE=1000
    return RMSE, predicted_demand,observed_demand,prediction_cluster

def ResultsAnalysis(PATH='NO',Cv2=False):
    
    day_to_predict = pd.read_csv(DAY_TO_PREDICT)
    # Create a dataframe for the results:
    x=np.arange(0,len(day_to_predict))
    y = [str(i) for i in range(26)]
    y[24]='cluster_id'
    y[25]='RMSE'
    results=pd.DataFrame(index=x, columns=y)
    cols = [str(i) for i in range(24)]
    for i in range (len(day_to_predict)):
        DAYDATA=day_to_predict.loc[i]
        [RMSE,Est,real,CL]=Prediction_Error(DAYDATA, Cv2, DAYDATA.Season)
        results.loc[i][cols]=real
        results.loc[i]['RMSE']=RMSE
        results.loc[i]['cluster_id']=CL
    if PATH=='NO':
        results.to_csv(PREDICTION_RESULTS)
    else:
        results.to_csv(PATH)