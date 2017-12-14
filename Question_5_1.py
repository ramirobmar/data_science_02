import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import time
import sys

NAME_OF_FILE1 = "./sanfrancisco_incidents_summer_2014.csv"
NAME_OF_FILE2 = "./seattle_incidents_summer_2014.csv"

def graphics_trends(table_1,table_2,title_1,title_2,nameoffile):
    try:    
        color_cycle = plt.rcParams['axes.prop_cycle']
        fig, ax = plt.subplots(2, 1, figsize=(16, 8), sharex=True, sharey=True)
        table_1.iloc[:, :5].plot(ax=ax[0],title=title_1);
        table_2.iloc[:, :5].plot(ax=ax[1],title=title_2);
        fig.savefig(nameoffile, bbox_inches='tight')    
    
    except Exception as exception1:
        print("Graphical plot exception: {0}".format(exception1))
    finally:
        print("Analysis completed ....")

def read_data_analysis(namefile_1,namedataindex,nametimeindex):
    analysis_1 = pd.read_csv(namefile_1,  sep=',')
    try:   
        ind = pd.DatetimeIndex(analysis_1[namedataindex])
        analysis_1[namedataindex] = ind.date.astype('datetime64')
        analysis_1[nametimeindex] = ind.hour
    except Exception as exc:
        print("Excepcion reading data: {0} {1}".format(exc,namedataindex))
    finally:
        print("Data readed ......")
        return analysis_1
		
analysis_1 = read_data_analysis(NAME_OF_FILE1,'Date','Time')
by_date1 = analysis_1.pivot_table(values = 'IncidntNum', aggfunc='count',index = 'Date',  columns=['Category'],)
cols= by_date1.columns
for col in range(len(cols)):
    by_date1[cols[col]] = np.int16( by_date1[cols[col]])
analysis_2 = read_data_analysis(NAME_OF_FILE2,'Date Reported','Time')
by_date2 = analysis_2.pivot_table(values = 'RMS CDW ID', aggfunc='count',index = 'Date Reported',  columns=['Summarized Offense Description'],)
cols= by_date2.columns
for col in range(len(cols)):
    by_date2[cols[col]] = np.int16( by_date2[cols[col]])
    
by_date2_final = by_date2['06-2014':'09-2014']
by_date1_final = by_date1['06-2014':'09-2014']

try:
    colsnames = ['06-2014','07-2014','08-2014']
    table_1 = pd.DataFrame(columns=by_date1_final.columns)
    table_2 = pd.DataFrame(columns=by_date2_final.columns)
    for index in range(3):
        record = by_date1_final[colsnames[index]]
        array=record.iloc[:,:].mean()
        table_1.loc[index,'ASSAULT'] = array['ASSAULT']
        table_1.loc[index,'BURGLARY'] = array['BURGLARY']
        table_1.loc[index,'ROBBERY'] = array['ROBBERY']
        table_1.loc[index,'WEAPON LAWS'] = array['WEAPON LAWS']
        table_1.loc[index,'STOLEN PROPERTY'] = array['STOLEN PROPERTY']
        
        record = by_date2_final[colsnames[index]]
        array=record.iloc[:,:].mean()
        table_2.loc[index,'ASSAULT'] = array['ASSAULT']
        table_2.loc[index,'BURGLARY'] = array['BURGLARY']
        table_2.loc[index,'ROBBERY'] = array['ROBBERY']
        table_2.loc[index,'WEAPON'] = array['WEAPON']
        table_2.loc[index,'STOLEN PROPERTY'] = array['STOLEN PROPERTY']
   
except Exception as exception1:
    print("Exception: {0}".format(exception1))
    sys.exit(0)

graphics_trends(table_1,table_2,'Incidents in San Francisco in 2014 Summer by month',
                'Incidents in Seatle in 2014 Summer by month',
                'figs/Question5_1.png')
