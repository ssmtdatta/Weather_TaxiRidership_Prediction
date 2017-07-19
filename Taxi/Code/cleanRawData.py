"""
This code starts with the raw taxi ridership data in csv format,
downloaded from the Chicago City Data portal
(https://data.cityofchicago.org/Transportation/Taxi-Trips/wrvz-psew),
cleans the data, and stores the clean data as pickle files.
"""

import pandas as pd
from datetime import datetime as dt
import os
import pickle

raw_path = "../RawData/"
out_path = "../CleanData/"

csvfiles = os.listdir(raw_path)



def outputFileName(csv_filename):
	prefix = csv_filename.split(".")[0]
	filename = prefix+'.p'
	return filename

def dateTimeConversion(d): 
	date_format = "%m/%d/%Y %I:%M:%S %p"
	x = dt.strptime(d, date_format)
	return x 

def applyThresholds(df):
	"""eliminate data based on the following criteria:
	   trip duration > 3 min, 
	   miles travelled in a trip > 0.25 miles,
	   taxi speed must be less than 75 mph.
	"""
	df = df.drop_duplicates(keep='first')
	df = df.drop_duplicates(['trip_id'], keep='first')
	df = df[(df['sec'] > 180)]
	df = df[(df['mile'] > 0.25)]
	df['mph'] = df['mile']/df['sec']
	df['mph'] = round(df['mph']*3600)
	df = df[(df['mph'] < 75)]
	df = df.sort_values(['trip_datetime'], ascending=[True])
	return df

def selectColumns(df_all):
	keep_columns = ['Trip Start Timestamp',
					'Taxi ID',
					'Trip ID',
				    'Trip Seconds',
                	'Trip Miles']
	df_selected = df_all[ keep_columns ]
	df_selected.columns = ['trip_datetime','taxi_id','trip_id','sec', 'mile']
	return df_selected



for csv in csvfiles:

	print(csv)

	pickle_filename = outputFileName(csv) 
	
	csv_df = pd.read_csv(raw_path+csv)
	
	df_selected = selectColumns(csv_df)

	df = applyThresholds(df_selected)

	
	start_datetime = [] 
	df_datetime = df['trip_datetime'].tolist()
	for i in range(0, df.shape[0]):
		dt_ = dateTimeConversion(df_datetime[i])
		start_datetime.append(dt_)

	df['trip_datetime'] = start_datetime

	with open(out_path+pickle_filename, 'wb') as picklefile:
		pickle.dump(df, picklefile)








