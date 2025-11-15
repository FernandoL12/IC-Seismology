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
def get_ids(start_date, end_date, dates, evid):
	'''
	str, str, list, list
	
	Get a list with the events' ids within time interval.
	'''
	start1_date = UTCDateTime(start_date)
	start1 = next(i for i, d in enumerate(dates) if d >= start1_date)

	end1_date   = UTCDateTime(end_date)
	end1 = next(i for i in reversed(range(len(dates))) if dates[i] <= end1_date)

	return c1_ids = evid[start1:end1+1]

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
start1_date = UTCDateTime('2024-12-15')
start1 = next(i for i, d in enumerate(dates) if d >= start1_date)

end1_date   = UTCDateTime('2024-12-15')
end1 = next(i for i in reversed(range(len(dates))) if dates[i] <= end1_date)

c1_ids = evid[start1:end1+1]
print(c1_ids)

## Cluster 2
# Start date: 2025-04-03
# End date  : 2025-04-05
start2_date = UTCDateTime('2025-04-03')
start2 = next(i for i, d in enumerate(dates) if d >= start2_date)

end2_date   = UTCDateTime('2025-04-05')
end2 = next(i for i in reversed(range(len(dates))) if dates[i] <= end2_date)
c2_ids = evid[start2:end2+1]

## Cluster 3
# Start date: 2025-07-01
# End date  : 2025-07-15
start3_date = UTCDateTime('2025-07-01')
start3 = next(i for i, d in enumerate(dates) if d >= start3_date)

end3_date   = UTCDateTime('2025-07-15')
end3 = next(i for i in reversed(range(len(dates))) if dates[i] <= end3_date)

c3_ids = evid[start3:end3+1]



























