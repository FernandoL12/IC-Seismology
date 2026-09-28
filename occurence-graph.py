#! /usr/bin/env python3

##########################################
###       Region earthquake plot       ###
#                                        #
# Initial Developed  by: Fernando (2025) #
#                                        #
##########################################

###############################
### Terminal command to get data:
## 1 - Londrina/RS
# wget -O - -q 'http://10.110.0.134/fdsnws/event/1/query?format=text&orderby=time&maxlat=-22.0&minlon=-53.0&maxlon=-49.2&minlat=-24.7' > file.txt
# awk -F '|' '$13 ~/Londrina/ {print $1, $2, $11, $13}' earthquake.txt > Londrina.txt
# make run input="$(awk '{print $1}' Londrina.txt | tr '\n' ' ')" window="P/0.2/0.7" station="LDASE" extra="--matrix"
# Reduced ev_list = usp2018blwx usp2018boet usp2018bojv usp2018cdft usp2018cxej usp2018dbml usp2018dbep

## 2 - Frutal/MG
# wget -O - -q 'http://10.110.0.134/fdsnws/event/1/query?format=text&orderby=time&maxlat=-18.4&minlon=-50.6&maxlon=-47.1&minlat=-21.2 > file.txt
# awk -F '|' '$13 ~/Frutal/ {print $1, $2, $11, $13}' earthquake.txt > Londrina.txt

## TUDO

# awk -F '|' '$13 ~/Londrina/ || $13 ~/Frutal/ || $13 ~/Divinópolis/ || $13 ~/Salobo/ || $13 ~/Sete-Lagoas/ {print $1, $2, $11, $13}' earthquake.txt > regioes.txt
# Só terremoto
# awk -F '|' '$15 == "earthquake" && ($13 ~/Londrina/ || $13 ~/Frutal/ || $13 ~/Divinopolis/ || $13 ~/Salobo/ || $13 ~/Sete/) {print $1, $2, $11, $13}' earthquakes.txt > regioes.txt

######
# Code
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from obspy.core import UTCDateTime

choose  = True
if choose:
    id_list = str(input('Events IDs: '))
    id_list = id_list.split()
    if not id_list:
        choose = False

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
    date_str = date_str[idx]
    local    = local[idx]

    # Choose specific IDs (if necessary)    
    if choose:
        temp_evid     = []
        temp_date_str = []
        temp_mag      = []
        temp_local    = []
        
        for ids, dat, mags, locs in zip(evid, date_str, mag, local):
            if ids in id_list:
                temp_evid.append(ids)
                temp_date_str.append(dat)
                temp_mag.append(mags)
                temp_local.append(locs)
                id_list.remove(ids)
                
        if id_list:
            print(f"Events not found: {id_list}")
        
        evid  = temp_evid
        dates = np.array([UTCDateTime(d) for d in temp_date_str])
        mag   = np.array(temp_mag)
        local = temp_local
    #-------------------------------------  
    # Filter events by magnitude
    mask = mag >= 0.5

    evid  = np.array(evid)[mask]
    dates = dates[mask]
    mag   = mag[mask]
    local = np.array(local)[mask]
    
    # Number of events
    num_events = len(evid)
    
    # Print useful informations
    print(f'Number of events in {local[0]}: {num_events}')
    print(f'MAX Magnitude: {mag.max()}')
    print(f'min Magnitude: {mag.min()}')
    print(f'Start date: {dates[0]}')
    print(f'End date: {dates[-1]}')
    
    # Plot date by magnitude graph
    plt.figure(figsize=(3,3))
    plt.plot([d.datetime for d in dates], mag, '*', markersize=8)
    
    plt.title(f'{local[0]}\nNº Events: {num_events}', fontsize=14)
    plt.xlabel('Date')
    plt.ylabel('Magnitude')
    
    plt.xticks(rotation=45)
    plt.grid(alpha=0.5, linestyle='--')
    
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    
    plt.tight_layout()
    plt.savefig(f"{file.removesuffix('.txt')}-map-by-date.png")
    plt.show()










