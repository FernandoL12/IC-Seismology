#! /usr/bin/env python3


###########################
###### Analysis code ######
###########################


## Libraries
import numpy as np
import correlation
import pandas as pd
from obspy.clients import fdsn
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from obspy.core import UTCDateTime, AttribDict, Stream

import warnings
warnings.filterwarnings("ignore")

#-----------------------------------------------------------------------
## Functions
## 1) Get evids by date
def get_ids(start_date, end_date, dates, evid):
	'''
	str, str, list, list
	
	Get a list with the events' ids within time interval.
	'''
	
	start1_date = UTCDateTime(start_date)
	start1 = next(i for i, d in enumerate(dates) if d >= start1_date)

	end1_date   = UTCDateTime(end_date)
	end1 = next(i for i in reversed(range(len(dates))) if dates[i] <= end1_date)

	return evid[start1:end1+1]


## 2) Write file with ids
def write_file(path, id_list, sep=" "):
	'''
	str, str --> file.txt
	
	Get a list with ID and write them on a .txt file.
	'''
	
	with open(file_path, 'w') as file:
		for ev_id in id_list:
			file.write(ev_id + sep)
#-----------------------------------------------------------------------
## Code
# Data selection criteria: events within 0.1° radius (11.11 km)
#of station BL.SLBO using the station's GPS coordinates

#'U10' for a Unicode string of max length 10, 'f8' for 64-bit float, 'i4' for 32-bit integer
# dtype_spec = [('evid', 'U11'), ('date', 'U26'), ('lat', 'f8'), ('lon', 'f8'), ('mag', 'f8')]

evid, date_str, lat, lon, mag = np.loadtxt(fname="induced.txt"    , 
                                          usecols=(0, 1, 2, 3, 10), 
                                          unpack=True             ,
                                          delimiter="|"           , 
                                          dtype=object)  
                                          
# Convert to appropriate types
dates = [UTCDateTime(d).datetime for d in date_str]
lat = lat.astype(float)
lon = lon.astype(float) 
mag = mag.astype(float)

# Plot date by magnitude graph
plt.plot(dates, mag, '*', markersize=3)
plt.title('Induced earthquake occurrence over time')
plt.xlabel('Date')
plt.ylabel('Magnitude')
plt.grid(alpha=0.7)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
plt.savefig("induced-map-by-date.png")

####
# CLUSTERS

## Cluster 1
# Start date: 2024-12-15
# End date  : 2025-02-01
start_date = UTCDateTime('2024-12-15')
end_date   = UTCDateTime('2024-12-15')
c1_ids = get_ids(start_date, end_date, dates, evid)

# Creating a txt document to keep IDs
file_path = "cluster1.txt"
write_file(file_path, c1_ids)


## Cluster 2
# Start date: 2025-04-03
# End date  : 2025-04-05
start_date = UTCDateTime('2025-04-03')
end_date   = UTCDateTime('2025-04-05')
c2_ids = get_ids(start_date, end_date, dates, evid)
# Creating a txt document to keep IDs
file_path = "cluster2.txt"
write_file(file_path, c2_ids)

		
## Cluster 3
# Start date: 2025-07-01
# End date  : 2025-07-15
start_date = UTCDateTime('2025-07-01')
end_date   = UTCDateTime('2025-07-15')
c3_ids = get_ids(start_date, end_date, dates, evid)

# Creating a txt document to keep IDs
file_path = "cluster3.txt"
write_file(file_path, c3_ids)



























