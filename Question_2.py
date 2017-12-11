import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import namedtuple
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

def convert_to_array(table,incident):

	col = 0
	array = [0, 1, 2, 3, 4]
	for index in [0, 1, 2, 3, 4]:
		array[col] = table.iloc[index,incident]
		col = col + 1
		
	return array


print("#############################################################################")
print("QUESTION 2 - Which incidents are most common in the evening")
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
cols= by_day1.columns
for col in range(len(cols)):
    by_day1[cols[col]] = np.int16(by_day1[cols[col]])
table_1 = by_day1.iloc[15:20,[1,23,3,33,26]] 

by_day2 = analysis_2.pivot_table(values = 'RMS CDW ID', aggfunc='count',index = 'Date Reported',  columns=['Summarized Offense Description'],)
cols= by_day2.columns
for col in range(len(cols)):
    by_day2[cols[col]] = np.int16(by_day2[cols[col]])

table_2 = by_day2.iloc[15:20,[1,36,4,46,38]] 



color_cycle = plt.rcParams['axes.color_cycle']
fig, ax = plt.subplots(2, 1, figsize=(16, 8), sharex=True, sharey=True)
n_groups = 5
index = np.arange(n_groups)


bar_width = 0.35
opacity = 0.4
error_config = {'ecolor': '0.3'}


rects1 = ax[0].bar(index, convert_to_array(table_1,0),bar_width/2,alpha=opacity,label=table_1.columns[0])
rects2 = ax[0].bar(index + bar_width/2, convert_to_array(table_1,1),bar_width/2,alpha=opacity,label=table_1.columns[1])  
rects3 = ax[0].bar(index + bar_width, convert_to_array(table_1,2),bar_width/2,alpha=opacity,label=table_1.columns[2]) 
rects4 = ax[0].bar(index + bar_width + bar_width/2, convert_to_array(table_1,3),bar_width/2,alpha=opacity,label=table_1.columns[3]) 
rects5 = ax[0].bar(index + 2 * bar_width, convert_to_array(table_1,4),bar_width/2,alpha=opacity,label=table_1.columns[4]) 

ax[0].set_xlabel('Incidents')
ax[0].set_ylabel('Scores')
ax[0].set_title('Incidents vs Time in San Francisco')
ax[0].set_xticks(index + bar_width / 5)
ax[0].set_xticklabels(('15:00', '16:00', '17:00', '18:00', '19:00'))
ax[0].legend()


rects1 = ax[1].bar(index, convert_to_array(table_2,0),bar_width/2,alpha=opacity,label=table_1.columns[0])
rects2 = ax[1].bar(index + bar_width/2,convert_to_array(table_2,1),bar_width/2,alpha=opacity,label=table_1.columns[1])  
rects3 = ax[1].bar(index + bar_width, convert_to_array(table_2,2),bar_width/2,alpha=opacity,label=table_1.columns[2]) 
rects4 = ax[1].bar(index + bar_width + bar_width/2,convert_to_array(table_2,3),bar_width/2,alpha=opacity,label=table_1.columns[3]) 
rects5 = ax[1].bar(index + 2 * bar_width, convert_to_array(table_2,4),bar_width/2,alpha=opacity,label=table_1.columns[4]) 

ax[1].set_xlabel('Incidents')
ax[1].set_ylabel('Scores')
ax[1].set_title('Incidents vs Time in Seatle')
ax[1].set_xticks(index + bar_width / 5)
ax[1].set_xticklabels(('15:00', '16:00', '17:00', '18:00', '19:00'))
ax[1].legend()



fig.tight_layout()
#plt.show()
  

fig.savefig('figs/Question2.png', bbox_inches='tight')
