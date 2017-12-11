import matplotlib
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import sys
import os

def add_inset(ax, rect, *args, **kwargs):
	try:
    		box = ax.get_position()
    		inax_position = ax.transAxes.transform(rect[0:2])
    		infig_position = ax.figure.transFigure.inverted().transform(inax_position)
    		new_rect = list(infig_position) + [box.width * rect[2], box.height * rect[3]]
    		return fig.add_axes(new_rect, *args, **kwargs)
	except Exception as ex:
		print("Exception: {0}".format(ex))

def cleaning_data_records(analysis_1):
	print("Starting the cleaning data ....")
	for index in range(len(analysis_1)):
		if (  str(analysis_1.loc[index,'Resolution'])  ==  (str('ARREST')) ) :
			if (np.int32(analysis_1.loc[index,'IncidntNum']) >= np.int32(140732575) ):
				analysis_1.loc[index,'Address'] = str(analysis_1.loc[index,'X'] )
				analysis_1.loc[index,'X'] = np.float(analysis_1.loc[index,'Y'] )
				analysis_1.loc[index,'Y'] = np.float(analysis_1.loc[index,'Location'] )
				analysis_1.loc[index,'Location'] = str("({0} - {1})".format(analysis_1.loc[index,'X'] ,analysis_1.loc[index,'Y']))
				analysis_1.loc[index,'PdId'] = str(analysis_1.loc[index,'Rec_A']) 
		else:
			analysis_1.loc[index,'Location'] = str("({0} - {1})".format(analysis_1.loc[index,'X'] ,analysis_1.loc[index,'Y']))
		
		
	analysis_1.to_csv("./sanfrancisco_incidents_summer_2014.csv")

	print("Complete the job .......")

def cleaning_data_records_2(analysis_1):
	print("Starting the cleaning data ....")
	for index in range(len(analysis_1)):
		if (  str(analysis_1.loc[index,'Address'])  ==  (str('CITED')) ) :
			analysis_1.loc[index,'Address'] = str(analysis_1.loc[index,'X'] )
			analysis_1.loc[index,'X'] = np.float(analysis_1.loc[index,'Y'] )
			analysis_1.loc[index,'Y'] = np.float(analysis_1.loc[index,'Location'] )
			analysis_1.loc[index,'Location'] = str("({0} - {1})".format(analysis_1.loc[index,'X'] ,analysis_1.loc[index,'Y']))
			analysis_1.loc[index,'PdId'] = str(analysis_1.loc[index,'Rec_A']) 
		else:
			analysis_1.loc[index,'Location'] = str("({0} - {1})".format(analysis_1.loc[index,'X'] ,analysis_1.loc[index,'Y']))
		
		
	analysis_1.to_csv("./sanfrancisco_incidents_summer_2014.csv")

	print("Complete the job .......")
	

if __name__ == "__main__":

	namefile_1 = "./sanfrancisco_incidents_summer_2014.csv"
	analysis_1 = pd.read_csv(namefile_1,  sep=',')

	namefile_2 = "./seattle_incidents_summer_2014.csv"
	analysis_2 = pd.read_csv(namefile_2,  sep=',')

	print(analysis_2)
	
	try:   
    		ind = pd.DatetimeIndex(analysis_2['Date Reported'])
    		analysis_2['Date Reported'] = ind.date.astype('datetime64')
    		
	except Exception as exc:
    		print("Excepcion: {0}".format(exc))
	finally:
		print("Data Format Conversion ......")
	
	print("################################")    
	print("Table 1: Incidents by Category in Seatle")
	print("################################")   
	
	by_date2 = analysis_2.pivot_table(values = 'RMS CDW ID', aggfunc='count',index = 'Date Reported',  columns=['Summarized Offense Description'],)
	
	cols= by_date2.columns
	for col in range(len(cols)):
		by_date2[cols[col]] = np.int16( by_date2[cols[col]])
	print(by_date2)
	
	
	
	print("######################################")   
	print("Table 2: Burglary vs week of year in Seatle")
	print("######################################")   

	try:
		ind = pd.DatetimeIndex(by_date2.index)
		by_date2.index = ind.date.astype('datetime64')
    
	except Exception as exc:
    		print("Excepcion: {0}".format(exc))
	finally:
    		print("Data Format Conversion ......")
	
	weekly_2 = by_date2.pivot_table('BURGLARY', index =by_date2.index.weekofyear, columns=by_date2.index.dayofweek)
	
	print(weekly_2)
	
	
	print("Tranformation of tables are completed .......")

	
	

	
	#Cleaning Data
	#print(analysis_1)
	#sys.exit(0)

	try:   
    		ind = pd.DatetimeIndex(analysis_1.Date)
    		analysis_1['Date'] = ind.date.astype('datetime64')
    		analysis_1['Time'] = ind.hour
	except Exception as exc:
    		print("Excepcion: {0}".format(exc))
	finally:
		print("Data Format Conversion ......")

	print("######################################")    
	print("Table 1: Incidents by Category in San Francisco")
	print("######################################")   
	by_date1 = analysis_1.pivot_table(values = 'IncidntNum', aggfunc='count',index = 'Date',  columns=['Category'],)
	cols= by_date1.columns
	
	for col in range(len(cols)):
		by_date1[cols[col]] = np.int16( by_date1[cols[col]])

	
			
	
	
	
	print("######################################")   
	print("Table 2: Burglary vs week of year")
	print("######################################")   

	

	weekly = by_date1.pivot_table('BURGLARY', index =by_date1.index.weekofyear, columns=by_date1.index.dayofweek)
	
	num = 0
	
	for col in range(len(weekly.columns)):
		print("{0}".format(col))
		print(weekly[col].values)
		
	weekly.columns.name = 'Day per Week'
	print(weekly)

	print("Tranformation of tables are completed .......")

	sys.exit(0)
	try:
	
	
		print("Graphical analysis ........")

		fig, ax = plt.subplots(2, 1, figsize=(16, 8), sharex=True, sharey=True)
		fig.subplots_adjust(hspace=0.1)
		color_cycle = plt.rcParams['axes.color_cycle']
	
		#print("Configuration OK")
	
		for i, col in enumerate(['BURGLARY']):
    			by_date1[col].plot(ax=ax[i], title=col, color=color_cycle[i])
    			ax[i].set_title(col + 's')

		with sns.axes_style('whitegrid'):
    			inset = [add_inset(ax[0], [0.07, 0.6, 0.2, 0.32]),
        	    		 add_inset(ax[1], [0.07, 0.6, 0.2, 0.32])]

	
		#index = 1
	
	
	
		
		for i, col in enumerate(['BURGLARY']):
    			inset[i].plot(range(7), weekly[col].values.T, color= color_cycle[i], lw= 2, alpha= 0.05);
    			inset[i].plot(range(7), weekly[col].mean(0), color= color_cycle[i], lw= 3)
    			inset[i].set_xticklabels(['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun'])
    			inset[i].yaxis.set_major_locator(plt.MaxNLocator(5))
    			inset[i].set_ylim(0, 500)
    			inset[i].set_title('Incidents by Day of Week')
    
		fig.savefig('figs/daily_incidents.png', bbox_inches='tight')
    
	except Exception as exc1:
		print("Excepcion: {0}".format(exc1))