import pandas as pd
import numpy as np
from config import *


def AVG_temperature(PATH='NO'):
    N_temp_class=NW_class;
    wd=pd.read_csv(WEATHER_DATA)
    test=1
    if PATH=='NO':
        clusters=pd.read_csv(CLUSTERED_DAYS_PATH_OUT)
    else:
        clusters=pd.read_csv(PATH)
        if not 'cluster_id' in clusters:
            clusters['cluster_id']=1
            test=0
    # Here we create two new colomns for season and temperature
    clusters['Temperature']=0
    #Code: Identify classes of temperature
    Temp=wd['Average']
    rg=np.linspace(min(Temp),max(Temp),N_temp_class)
    rg_class=range(1,len(rg)+1);
    
    for i in range(0, max(clusters['cluster_id'])+1):
        tmp=clusters['cluster_id']
        index=(tmp==i)
        tmp_cl=clusters.loc[index]
        tmp_T=wd.loc[index]
        tmp=tmp_T['Average']
        k=0
        for T in rg:
            index_tmp=(tmp<=T)            
            tmp_cl.loc[index_tmp,'Temperature']=rg_class[k]
            tmp[index_tmp]=10000
            k=k+1
        clusters.loc[index,'Temperature']=tmp_cl.loc[:,'Temperature']
    if test==0:
        clusters=clusters.drop(columns=['cluster_id'])
    if PATH=='NO':
        clusters.to_csv(DECOMPOSED_DAYS_PATH_OUT, index=False)
    else:
        clusters.to_csv(PATH, index=False)
def Seasond_class(PATH='NO'):
    N_temp_class=NW_class;
    wd=pd.read_csv(WEATHER_DATA)
    if PATH=='NO':
        clusters=pd.read_csv(DECOMPOSED_DAYS_PATH_OUT)
    else:
        clusters=pd.read_csv(PATH)
    clusters['Season']=0
    #Code: Identify Season    
    for i in range(0, 3):
        if i==0:
            S=Spring
        elif i==1:
            S=Summer
        elif i==2:
            S=Autumn       
        else:
            S=Winter    
        tmp=clusters['index']
        
        Si=np.where(tmp==S[0])
        Se=np.where(tmp==S[1])
        
        # Check if both days are into the database, if not set Si=1 or Se=end
        if (np.size(Si)==1 and np.size(Se)==0):
            Se=np.where(tmp==tmp[len(tmp)-1])        
        if (np.size(Si)==0 and np.size(Se)==1):
            Si=np.where(tmp==tmp[0])
            
        # Assign Information 
        if (np.size(Si)==1 and np.size(Se)==1):   
            clusters.loc[Si[0][0]:Se[0][0],'Season']=i
    if PATH=='NO':
        clusters.to_csv(DECOMPOSED_DAYS_PATH_OUT, index=False)
    else:
        clusters.to_csv(PATH, index=False)
    
def Decompose_Clusters():
    N_temp_class=NW_class;
    wd=pd.read_csv(WEATHER_DATA)
    clusters=pd.read_csv(DECOMPOSED_DAYS_PATH_OUT)
    clusters['Cv2']=0
    #Code: Create new Clustering
    cl=1        
    for i in range(0, max(clusters['cluster_id'])+1):
        tmp=clusters['cluster_id']
        index=(tmp==i)
        tmp_cl=clusters.loc[index]
        k=0
        Stop=0
        while Stop==0:
            x=tmp_cl.iloc[k]   
            if x['Cv2']==0:
                y1=tmp_cl['Temperature']==x['Temperature']
                y2=tmp_cl['Season']==x['Season']
                index_tmp=np.logical_and(y1, y2);
                tmp_cl.loc[index_tmp,'Cv2']=cl
            if k==len(tmp_cl)-1:
                Stop=1
            cl=cl+1
            k=k+1
        clusters.loc[index,'Cv2']=tmp_cl.loc[:,'Cv2']
    clusters.to_csv(DECOMPOSED_DAYS_PATH_OUT, index=False)