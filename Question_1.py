import sys
import numpy as np # linear algebra
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import time
print("#############################################################################")
print("QUESTION 1 -How do incidents vary by time of day for either city")
print("S.Francisco vs Seatle")
print("#############################################################################")  


try:   
    namefile_1 = "./sanfrancisco_incidents_summer_2014.csv"
    analysis_1 = pd.read_csv(namefile_1,  sep=',')
    ind1 = pd.DatetimeIndex(analysis_1.Time)
    analysis_1.Time = ind1.hour
    
    namefile_2 = "./seattle_incidents_summer_2014.csv"
    analysis_2 = pd.read_csv(namefile_2,  sep=',')
    ind2 = pd.DatetimeIndex(analysis_2['Date Reported'])
    analysis_2['Date Reported'] = ind2.hour
    
except Exception as exc:
    print("Excepcion: {0}".format(exc))
finally:
    print("Data Format Conversion ......")

   

by_day1 = analysis_1.pivot_table(values = 'IncidntNum', aggfunc='count',index = 'Time',  columns=['Category'],)
table_1 = by_day1.iloc[:,[1,23,3,33,26]] 

by_day2 = analysis_2.pivot_table(values = 'RMS CDW ID', aggfunc='count',index = 'Date Reported',  columns=['Summarized Offense Description'],)
table_2 = by_day2.iloc[:,[1,36,4,46,38]] 

try:    
    color_cycle = plt.rcParams['axes.color_cycle']
    fig, ax = plt.subplots(2, 1, figsize=(16, 8), sharex=True, sharey=True)
    table_1.iloc[:, :5].plot(ax=ax[0],title='Incidents in San Francisco by Hours');
    table_2.iloc[:, :5].plot(ax=ax[1],title='Incidents in Seatle by Hours');
    fig.savefig('figs/Question1.png', bbox_inches='tight')    
    
except Exception as exception1:
    print("Graphical plot exception: {0}".format(exception1))
finally:
    print("Results:")
