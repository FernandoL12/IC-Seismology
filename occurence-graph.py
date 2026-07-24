#! /usr/bin/env python3

##########################################
###       Region earthquake plot       ###
#                                        #
# Initial Developed  by: Fernando (2025) #
#                                        #
##########################################

###############################
# Terminal command to get data:
# 1 - Londrina:
# wget -O - -q 'http://10.110.0.134/fdsnws/event/1/query?format=text&orderby=time&maxlat=-22.0&minlon=-53.0&maxlon=-49.2&minlat=-24.7' > file.txt



######
# Code
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from obspy.core import UTCDateTime

if __name__ == '__main__':

    file = input('Name of file.txt: ')
    evid, date_str, mag, local = np.loadtxt(fname= file   ,
                                            unpack=True   ,
                                            delimiter=" " ,
                                            dtype=object)

    # Convert to appropriate types
    dates = np.array([UTCDateTime(d) for d in date_str])
    mag   = mag.astype(float)
    local = local.astype(str)

    # Sort everything by time
    idx   = np.argsort(dates)
    dates = dates[idx]
    evid  = evid[idx]
    mag   = mag[idx]

    # Plot date by magnitude graph
    plt.plot([d.datetime for d in dates], mag, '*', markersize=3)
    plt.title(f'{local[0]}')
    plt.xlabel('Date')
    plt.ylabel('Magnitude')
    plt.grid(alpha=0.7)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.show()
    #plt.savefig(f"{file.removesuffix('.txt')}-map-by-date.png")




