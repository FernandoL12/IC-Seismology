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
from obspy.core import UTCDateTime, AttribDict, Stream

import warnings
warnings.filterwarnings("ignore")

#-----------------------------------------------------------------------
## Functions


#-----------------------------------------------------------------------
## Code
# Data selection criteria: events within 0.1° radius (11.11 km)
#of station BL.SLBO using the station's GPS coordinates

#'U10' for a Unicode string of max length 10, 'f8' for 64-bit float, 'i4' for 32-bit integer
# dtype_spec = [('evid', 'U11'), ('date', 'U26'), ('lat', 'f8'), ('lon', 'f8'), ('mag', 'f8')]

evid, date_str, lat, lon, mag = np.loadtxt(fname="induced.txt", 
                                          usecols=(0, 1, 2, 3, 10), 
                                          unpack=True             ,
                                          delimiter="|"           , 
                                          dtype=str)  
                                          
# Convert to appropriate types
dates = [UTCDateTime(d) for d in date_str]
lat = lat.astype(float)
lon = lon.astype(float) 
mag = mag.astype(float)

# Plot date by magnitude graph
plt.plot(dates, mag, '*', markersize=3)
plt.title('Induced earthquake occurrence over time')
plt.xlabel('Date')
plt.ylabel('Magnitude')
plt.grid(alpha=0.7)
plt.show()
































