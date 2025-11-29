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
	
	with open(path, 'w') as file:
		for ev_id in id_list:
			file.write(ev_id + sep)
			

## 3) Statistical analysis
def statistical(ids, ids_list, mag_list):
	"""
	list, list, list --> dict
	
	Computes basic magnitude statistics for the subset of event IDs provided.
	"""

	# Verification if lists are not None
	if ids is None or len(ids) == 0:
		raise ValueError("Error: 'ids' list is empty — no events were provided.")

	if ids_list is None or len(ids_list) == 0:
		raise ValueError("Error: 'ids_list' is empty — cannot match events.")

	if mag_list is None or len(mag_list) == 0:
		raise ValueError("Error: 'mag_list' is empty — no magnitudes available.")

	# Find indices of selected IDs
	magnitudes = [mag_list[i] for i, eid in enumerate(ids_list) if eid in ids]

	if not magnitudes:
		raise ValueError("Error: None of the provided IDs exist in ids_list.")

	# Calculate statistics
	num_events  = len(magnitudes)
	max_mag     = max(magnitudes)
	mean_mag    = sum(magnitudes) / num_events
	median_mag  = np.median(magnitudes)

	return num_events, max_mag, mean_mag, median_mag


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
dates = np.array([UTCDateTime(d) for d in date_str])
lat = lat.astype(float)
lon = lon.astype(float) 
mag = mag.astype(float)

# Sort everything by time
idx   = np.argsort(dates)
dates = dates[idx]
evid  = evid[idx]
mag   = mag[idx]

# Plot date by magnitude graph
plt.plot([d.datetime for d in dates], mag, '*', markersize=3)
plt.title('Induced earthquake occurrence over time')
plt.xlabel('Date')
plt.ylabel('Magnitude')
plt.grid(alpha=0.7)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
plt.savefig("induced-map-by-date.png")


####
# CLUSTERS
cluster_dict = {}

## Cluster 1
start_date = '2024-12-15'
end_date   = '2025-02-01'
c1_ids = get_ids(start_date, end_date, dates, evid)

write_file("cluster1.txt", c1_ids)
cluster_dict["cluster 1"] = c1_ids

## Cluster 2
start_date = '2025-04-03'
end_date   = '2025-04-05'
c2_ids = get_ids(start_date, end_date, dates, evid)

write_file("cluster2.txt", c2_ids)
cluster_dict["cluster 2"] = c2_ids

## Cluster 3
start_date = '2025-07-01'
end_date   = '2025-07-15'
c3_ids = get_ids(start_date, end_date, dates, evid)

write_file("cluster3.txt", c3_ids)
cluster_dict["cluster 3"] = c3_ids


####
# Statistical analysis
clusters = {}

for cluster_name, ids in cluster_dict.items():
    num_events, max_mag, mean_mag, median_mag = statistical(ids, evid, mag)

    clusters[cluster_name] = {
							"ev_ids"    : ids       ,
							"num_events": num_events,
							"max_mag"   : max_mag   ,
							"mean_mag"  : mean_mag  ,
							"median_mag": median_mag
							}

# Save clusters information to a text file
with open('Clusters.txt', 'w') as file:
	for cluster_name, data in clusters.items():

		file.write(f"{cluster_name}:\n")
		file.write(f"    ev_ids     : {', '.join(data['ev_ids'])}\n")
		file.write(f"    num_events : {data['num_events']}\n"       )
		file.write(f"    max_mag    : {data['max_mag']}\n"          )
		file.write(f"    mean_mag   : {data['mean_mag']}\n"         )
		file.write(f"    median_mag : {data['median_mag']}\n"       )
		file.write("\n")

