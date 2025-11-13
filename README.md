# IC-Seismology-2025
Data and codes developed during my scientific initiation in seismology at Center of Seismology (IAG-USP).

## Objective
Develop a code for automatic P pick correction for aftershocks based on the maximum correlation with the main event.

## Method
Gets and cut data from a given FDSN Client, interval (in seconds) and event(s) ID(s). After that, the code makes data cross-correlation, generates and saves as figure: 1. Correlation matrix; 2. Time correction times matrix; 3. A post P pick time correction seismogram with superposed waveforms.
