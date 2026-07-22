#! /usr/bin/env python3

##########################################
###       Cross-Correlation Code       ###
#                                        #
# Initial Developed  by: Fernando (2025) #
#         Refactored by:  Bianchi (2026) #
#                                        #
##########################################

## Libraries
import os, sys
import argparse
import numpy as np
import seaborn as sns

from obspy import read
from obspy.clients import fdsn
from obspy.core import UTCDateTime, AttribDict, Stream, Trace

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

from scipy.signal import correlate, correlation_lags

import warnings
warnings.filterwarnings("ignore")

###############
## Functions ##
###############

#--------
# 1) IO
class LoadError(BaseException):
	pass


def cmdline():
	parser = argparse.ArgumentParser(
					prog='mCCC',
					description='Matriz Cross-Correlation Code',
					formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	# General Parameters
	g0 = parser.add_argument_group('General')
	g0.add_argument('-v', '--verbose', action='store_true',
					help = 'Be verbose')

	g0.add_argument('-S', '--station', type = str, default = None,
					help = 'Indicate station to use (needed if only events IDs are supplied).')

	g0.add_argument('-w', '--window', default = 'P/1/2', type = str,
					help = 'Window size to perform the correlation. Format is Phase/pre[/pos]. Pre and Pos are positive numbers, Phase is one of P or S. [] are optional.')

	g0.add_argument('events', nargs='+',
					help='Id of one or more events to process.')

	# Correlation parameters
	g1 = parser.add_argument_group('Correlation Parameters')

	g1.add_argument('-c', '--correction', action = 'store_true',
					help = 'Perform a correction shift of given seconds to search for best alignment.')

	g1.add_argument('-cs', '--correction-shift', default = 2.0, type = float,
					help = 'Amount of shift allowed while searching for the max correlation in a given window.')

	g1.add_argument('-s', '--self', action = 'store_true',
					help = 'Perform auto-correlation')

	# Filters
	g2 = parser.add_argument_group('Data Processing Parameters')

	g2.add_argument('-lp', '--low-pass', type = float, default = None,
					help = 'Low pass filter value [Hz].')

	g2.add_argument('-hp', '--high-pass', type = float, default = None,
					help = 'High pass filter value [Hz].')

	
	# FDSN server sources
	g3 = parser.add_argument_group('Data Fetching parameters')

	g3.add_argument('-F', '--dfdsn', type = str, default = 'http://seisarc.sismo.iag.usp.br',
					help = 'FDSN server to fetch data. If no -E option is given this is the default server to fetch events.')

	g3.add_argument('-E', '--efdsn', type = str, default = None,
					help = 'FDSN serve to fetch event. Defaults to same as -F')


	# FDSN server sources
	g4 = parser.add_argument_group('Visualization parameters')

	g4.add_argument('--matrix', action = 'store_true', 
					help = 'Show correlation results.')

	g4.add_argument('--matrixmode', choices = [ 'corr', 'lag' ], default = 'corr',
					help = 'Input a mode for matrix.')

	g4.add_argument('--correlation', action = 'store_true', 
					help = 'Show correlation result for one pair.')

	g4.add_argument('--pair', type = str, default = None, 
					help = 'Indicate correlation plot pair labels.')

	g4.add_argument('--waveform', action = 'store_true', 
					help = 'Show waveforms results.')

	g4.add_argument('--waveform-cols', type = int, default = 3, 
					help = 'Number of columns in waveform plot.')

	g4.add_argument('--save', action = 'store_true',
					help = 'Instead of showing in screen, save to disk images.')

	# Process
	args = parser.parse_args()

	return args


def parse_phase(v):
	phase, pre, pos = v.split("/")
	pre = float(pre)
	pos = float(pos)

	return phase, pre, pos


def load_event(event, args):
	"""
	Load an event waveform and its associated phase pick.

	The event may be provided either as a SAC file or as an event ID
	available from an FDSN server. When loading from a SAC file, the
	requested phase pick must be stored in the corresponding SAC header
	field:
	
	For sac files:
	
	 - P mark must be on A 
	 - S mark must be on T0

	When loading from an FDSN server, the function retrieves the preferred
	origin, searches for the requested phase arrival at the selected
	station, and downloads the corresponding waveform.

	Parameters
	----------
	event : str
		Event identifier or path to a SAC file.

	args : argparse.Namespace
		Parsed command-line arguments containing the processing options,
		waveform window, station code, and FDSN server configuration.

	Returns
	-------
	tuple[str, obspy.UTCDateTime, obspy.Trace]
		A tuple containing:

		- Event identifier.
		- Pick time of the requested phase.
		- Loaded waveform as an ObsPy "Trace".

	Raises
	------
	LoadError
		If the SAC file is invalid, the requested phase pick cannot be
		found, the event or waveform cannot be retrieved from the FDSN
		server, or the downloaded waveform does not contain the requested
		pick.
	"""

	phase, pre, pos = args.window

	_REQUEST_MARGIN_ = 30 + args.correction_shift

	_HEADER_MAP = {
		'P' : 'a',
		'S' : 't0'
	}

	pick = tr = None

	if os.path.isfile(event): # Load from FILE - must be SAC !

		data = read(event)
		tr = data[0]

		if not hasattr(tr.stats, "sac"):
			raise LoadError(f"W:> File {event} is not a sac file, or header not loaded.")

		try:
			mappedphase = _HEADER_MAP[phase]
		except ValueError:
			raise LoadError(f"W:> Phase {phase} is not supported with SAC files.")

		if not hasattr(tr.stats.sac, mappedphase) or tr.stats.sac[mappedphase] == -12345:
			raise LoadError(f"W:> File {event} does not have a {phase} pick on header variable 'T0'.")

		pick = tr.stats.starttime + tr.stats.sac[mappedphase] - tr.stats.sac.b

		if tr.stats.sac.kevnm != "-12345":
			event = tr.stats.sac.kevnm
		else:
			event = event.replace(".sac","").replace(".SAC","")
    #====
	else:                     # Load from FDSN event ID
		# Check that station is set
		if args.station is None:
			raise LoadError(f"W:> When loading from an EVID and an FDSN server a station code must be given")

		# Setup fdsn servers
		if type(args.dfdsn) == str:
			if args.verbose: print(f"I:> Using Data fdsn from {args.dfdsn}" )
			args.dfdsn = fdsn.Client(args.dfdsn)

		if type(args.efdsn) == str:
			if args.verbose: print(f"I:> Using Event fdsn from {args.efdsn}" )
			args.efdsn = fdsn.Client(args.efdsn)

		if args.efdsn is None:
			if args.verbose: print(f"I:> Using same fdsn for Data & Event requests." )
			args.efdsn = args.dfdsn

		# Find event
		try:
			evp = args.efdsn.get_events(eventid = event, includearrivals = True)

		except Exception as e:
			raise LoadError(f"W:> Event {event} not found on FDSN server")

		E = evp[0]
		O = E.preferred_origin()

		# Find Arrival & Pick
		for A in O.arrivals:
			if A.time_weight <= 0.0: continue
			if A.phase != phase: continue
			P = [ P for P in E.picks if P.resource_id == A.pick_id ][0]
			if P.waveform_id.station_code != args.station: continue
			
			break
		else:
			raise LoadError(f'W:> Cannot find valid {phase} pick @ {event} for {args.station} station.')

		# Load data
		try:
			N = P.waveform_id.network_code
			S = P.waveform_id.station_code
			L = P.waveform_id.location_code if P.waveform_id.location_code is not None else ""

			# this is hardcoded, should be an option!
			C = P.waveform_id.channel_code[:2] + "Z"

			start = P.time - (pre + _REQUEST_MARGIN_)
			end   = P.time + (pos + _REQUEST_MARGIN_)

			if args.verbose:
				print(f'I:> Requesting {N}.{S}.{L}.{C} from {start} to {end}')

			st = args.dfdsn.get_waveforms(N,S,L,C, start, end)

		except fdsn.header.FDSNNoDataException as E:
			raise LoadError(str(E))

		# guarantee data
		st.merge(method = 1, fill_value = 'latest')
		tr = st[0]

		# Save pick
		pick = P.time

	if tr.stats.starttime > pick or tr.stats.endtime < pick:
		raise LoadError(f"I:> Data for {event} with {phase} Pick @ {pick} is gappy -- skipped!")

	if args.verbose:
		print(f'I:> Loaded {event} = {tr.stats.network}.{tr.stats.station}.{tr.stats.location}.{tr.stats.channel} with {tr.stats.sampling_rate} sps and {phase} pick @ {pick}')

	return event, pick, tr


#----------------
# 2) Processing
def npts_cut(
			tr: Trace,
			t0: UTCDateTime,
			length: float | None = None,
			npts: int | None = None,
			) -> Trace:
				
	'''
	Return a copy of a trace trimmed from a given start time.

	The trace is trimmed starting at the sample immediately preceding
	the sample nearest to ``t0``. The trimming interval can be specified
	either by its duration (`length`) or by the desired number of
	samples (`npts`), but not both simultaneously.

	Parameters
	----------
	tr : obspy.Trace
		Input seismic trace.

	t0 : obspy.UTCDateTime
		Desired start time of the trimmed trace.

	length : float, optional
		Length of the trimmed trace in seconds.

	npts : int, optional
		Number of samples of the trimmed trace.

	Returns
	-------
	obspy.Trace
		A copy of the input trace containing only the selected interval.

	Raises
	------
	ValueError
		If both `length` and `npts` are provided.
	'''
	
	if length is not None and npts is not None:
		raise Exception(f'E:> It is impossible to cut on a length and npts at the same time.')

	t0real = tr.times("utcdatetime")[(np.abs(tr.times("utcdatetime")-t0).argmin())] - tr.stats.delta / 2.0
	trc = tr.copy()
	
	if length is None:
		length = npts * tr.stats.delta
	
	trc.trim(t0real, t0real + length, nearest_sample = False)    

	return trc


def pre_process(pick, trace, args, add_corr_margin):
	'''
	Pre process downloaded data with needed parameters and options
	
	returns: a copy of the given trace
	'''

	_,pre,pos = args.window

	tr = trace.copy()

	tr.detrend()

	if args.low_pass is None and args.high_pass is not None:
		tr.filter("lowpass", freq = args.low_pass)
	elif args.low_pass is not None and args.high_pass is None:
		tr.filter("highpass", freq = args.high_pass)
	elif args.low_pass is not None and args.high_pass is not None:
		tr.filter("bandpass", freqmin = args.high_pass, freqmax = args.low_pass)

	tr.trim(pick - pre - (args.correction_shift if add_corr_margin and args.correction else 0.0),
			pick + pos + (args.correction_shift if add_corr_margin and args.correction else 0.0))

	return tr


def build_corr_matrix(data, args):
	"""
	Cross correlate input data using the given readed files and arguments.
	"""

	size = len(data)

	_,pre,pos = args.window

	results = []

	if args.verbose:
		print(f'')
		print(f'I:> Computing correlation of {size} events')
		if args.correction:
			print(f'I:>  Event can be shift for maximum fit.')
			print(f'I:>  Maximum shift is {args.correction_shift} seconds.')
		if args.high_pass is not None or args.low_pass is not None:
			print(f'I:>  Frequency filter set to {args.high_pass if args.high_pass else "None"} < f < {args.low_pass  if args.low_pass else "None"}')
		else:
			print(f'I:>  No filter will be applied')
		print(f'')

	for i in range(size):
		evid1, pick1, data1 = data[i]
		data1 = pre_process(pick1, data1, args, False)

		for j in range(i+(0 if args.self else 1), size):
			evid2, pick2, data2 = data[j]
			data2 = pre_process(pick2, data2, args, True)

			OFFSET = 0.0
			rs1    = 0.0
			rs2    = 0.0
			lags   = None
			corr   = None
			lag_maxi  = 0.0
			corr_maxi = 0.0

			if args.correction and i != j:
				# Correlate
				corr = correlate(data1.data, data2.data, mode='valid')
				lags = correlation_lags(len(data1.data), len(data2.data), mode='valid')

				# Upscalling the correlation 
				index = np.argmax(corr)
				dt    = data1.stats.delta
				
				# Boundary value problem
				if index == 0 or index == len(corr) - 1:
					lag_maxi  = lags[index] * dt
					corr_maxi = corr[index]

				else:
					lag_3     = lags[index-1:index+2]
					corr3     = corr[index-1:index+2]

					
					a,b,c     = np.polyfit(lag_3*dt, corr3, deg=2)
					x         = -b/(2*a)
					lag_maxi  = x
					corr_maxi = a*x**2 + b*x + c
				
				# Finding offset
				rs1 = data1.times('utcdatetime')[0]
				rs2 = data2.times('utcdatetime')[0]
				OFFSET = (pick1 - rs1) - (pick2 - rs2 + lag_maxi)

			data1 = npts_cut(data1, t0 = pick1 - pre, length = (pre + pos))
			data2 = npts_cut(data2, t0 = pick2 - pre + OFFSET, npts = data1.stats.npts)
			corr_coef = np.abs(np.corrcoef(data1.data, data2.data)[0][1])

			if args.verbose:
				print(f"I:> For i={i:03d} j={j:03d} evA={evid1:18s} evB={evid2:18s} OFFSET={OFFSET:+8.3f} CORR_COEF={corr_coef:+9.4f}")

			results.append(AttribDict({
				'i' : i,
				'j' : j,
				'data1'  : data1,
				'data2'  : data2,
				'lags'   : lags,
				'corr'   : corr,
				'lag_maxi' : lag_maxi,
				'OFFSET' : OFFSET,
				'M' : corr_coef
			}))

	return results, [ evid for evid,_,_ in data ]


#----------
# 3) Plot
def N(data):
	return data / np.max(np.abs(data))


def plot_matrix(data, results, labels, args, figsize=(7,6), cmap=plt.cm.RdYlGn):
	"""
	Plot a heatmap from results and labels by evids
	"""

	size = len(data)

	fig, ax = plt.subplots(nrows=1, ncols=1, figsize=figsize)

	### Assembly heat map
	heat = np.ones([size, size])
	heat[:,:] = np.nan
	for r in results:
		heat[r.i][r.j] = r.M if args.matrixmode == 'corr' else r.OFFSET

	cmap.set_bad('#48494B')

	sns.heatmap(
		heat,
		cmap  = cmap,
		vmin  = 0.0,
		vmax  = np.nanmax(heat),
		annot = True,
		ax    = ax,
		xticklabels = labels,
		yticklabels = labels,
		cbar_kws = {'label': 'Correlation value' if args.matrixmode == 'corr' else 'Correlation Lag [s]' }
	)

	ax.figure.axes[-1].yaxis.label.set_size(12)
	ax.set_title(f'Correlation matrix{" (corrected)" if args.correction else " "}\nNº of events: {size}', fontsize=15)

	plt.tight_layout()
	
	if args.save:
		if args.verbose:
			print(f'I:> Save matrix correlation plot to matrix-corr.png')
		plt.savefig("matrix-corr.png")
		return

	plt.show()

	return


def plot_waveforms(data, results, labels, args):
	"""
	Plot waveforms wiggle correlated
	"""

	phase,pre,pos = args.window

	# Number of plot and panels
	ntotal = len(results)

	ncols = args.waveform_cols if ntotal > args.waveform_cols else ntotal
	nrows = 1 if ntotal <= args.waveform_cols else ntotal // ncols
	
	if ncols * nrows < ntotal:
		nrows += 1

	# plots
	fig, axs = plt.subplots(nrows = nrows,
						   ncols = ncols,
						   figsize = (ncols * 5, nrows * 2), squeeze = False)

	# working ...
	cont = 0
	for row in range(nrows):
		for col in range(ncols):
			evid1,_,_ = data[results[cont].i]
			evid2,_,_ = data[results[cont].j]

			data1 = results[cont].data1
			data2 = results[cont].data2

			title = evid1 + " -x- " + evid2
			ax = axs[row][col]
			
			# Waveforms
			ax.plot(data1.times(), N(data1.data), color='#F97306', ls='--')
			ax.plot(data2.times(), N(data2.data), color='C0', ls='--')

			# Marks
			OFFSET = results[cont].OFFSET

			ax.axvline(pre, 0.55, 0.95, color ='#F97306', lw=1)
			ax.axvline(pre - OFFSET, 0.05, 0.50, color ='C0', lw=1)

			ax.set_title(title)
			cont += 1
			
			if cont == ntotal:
				break
	
	plt.tight_layout()
	
	if args.save:
		if args.verbose:
			print(f'I:> Save matrix correlation plot to all-graphs.png')
		plt.savefig("all-graphs.png")
		return

	plt.show()
	
	return
	

def plot_correlation(data, results, labels, args):

	# Find correct correlation result to plot
	eva,evb = args.pair.split("/")

	r = [ rr for rr in [ r for r in results if (data[r.i][0] == eva) or (data[r.j][0] == evb) ] if (data[rr.i][0] == eva) or (data[rr.j][0] == evb)][0]

	evid1,t1,_ = data[r.i]
	evid2,t2,_ = data[r.j]

	# Plot
	fig = plt.figure(figsize = (14,6))

	gs = GridSpec(2, 2, figure = fig)

	ax1 = fig.add_subplot(gs[0, 0])
	ax2 = fig.add_subplot(gs[0, 1])
	ax3 = fig.add_subplot(gs[1, :])

	ax1.set_title(f"Before correlation\n{evid1} -x- {evid2}", fontsize=16) 
	ax1.plot(r.data2.times('utcdatetime') - t2, N(r.data2.data), "--", color='#F97306', label='Event 2')
	ax1.plot(r.data1.times('utcdatetime') - t1, N(r.data1.data), color ='C0', label='Event 1')
	ax1.axvline(0.0, 0.05, 0.50, color ='C0', lw=2)
	ax1.axvline(0.0, 0.55, 0.95, color ='#F97306', lw=2)
	
	mmin  = min(r.data1.times('utcdatetime') - t1)
	mmax  = max(r.data1.times('utcdatetime') - t1)
	mmin -= abs(0.02 * (mmax-mmin))
	mmax += abs(0.02 * (mmax-mmin))
	ax1.set_xlim((mmin, mmax))
	
	ax1.set_xlabel(f"Time relative to trace start time (s)\n\n", fontsize=14)
	ax1.set_ylabel("Normalized amplitude", fontsize=14)
	ax1.grid(alpha=0.4)
	ax1.legend(loc=4, ncols = 2)

	ax2.set_title(f"After correlation\n{evid1} -x- {evid2}", fontsize=16) 

	ax2.plot(r.data2.times('utcdatetime') - t2 - r.OFFSET, N(r.data2.data), "--", color='#F97306', label='Event 2')
	ax2.axvline(- r.OFFSET, 0.55, 0.95, color ='#F97306', lw=2)
	ax2.axvline(0.0, color ='limegreen', label='Corrected Pick (2)', ls='--', lw=1)

	ax2.plot(r.data1.times('utcdatetime') - t1, N(r.data1.data), color ='C0', label='Event 1')
	ax2.axvline(0.0, 0.05, 0.50, color ='C0', lw=2)

	ax2.set_xlim((mmin, mmax))
	ax2.set_xlabel(f"Time relative to trace start time (s)\n\n", fontsize=14)

	ax2.grid(alpha=0.4)
	ax2.legend(loc=4, ncols = 2)

	dt = r.data1.stats.delta
	ax3.plot(r.lags * dt - r.OFFSET, N(r.corr), '.', color='red')
	ax3.plot(r.lags * dt - r.OFFSET, N(r.corr), color='red', lw=0.5)
	ax3.axvline(r.lag_maxi - r.OFFSET, color ='limegreen', label=f'Lag ({r.lag_maxi - r.OFFSET:.3f})')
	ax3.grid(alpha=0.4)

	ax3.set_title("Correlation lag", fontsize=16)
	ax3.set_xlabel('LAG (s)', fontsize=14)
	ax3.legend()

	plt.tight_layout()

	if args.save:
		print(f'Saving figure to file cross-{evid1}x{evid2}.png')
		plt.savefig(f"cross-{evid1}x{evid2}.png")
		return

	plt.show()

	return


##################
##     Main     ##
##################
if __name__ == '__main__':
	# Call arguments
	args = cmdline()

	#
	args.window = parse_phase(args.window)

	if not args.matrix and not args.correlation and not args.waveform:
		print('E:> Nothing to do', file = sys.stderr)
		sys.exit(1)

	##
	# Load the data for each event given
	##
	data = []
	stop = False
	for event in args.events:
		try:
			# Try to load ... 
			data.append(load_event(event, args))
		except LoadError as E:
			print(f"W:> Failed to load data from event {event} \n\tReason => {E}", file = sys.stderr)
			continue

		# Warns: if different stations are considered!
		for e,p,d in data[:-1]:
			if data[-1][2].id != d.id:
				print(f'W:> Current id {data[-1][2].id} @ event {data[-1][0]} differ from id {d.id} @ event {e}.', file = sys.stderr)

			if data[-1][2].stats.delta != d.stats.delta:
				print(f'E:> Current delta {data[-1][2].stats.delta} @ event {data[-1][0]} differ from delta {d.stats.delta} @ event {e} -- will abort computation.', file = sys.stderr)
				stop = True
	# Sort data chronologically
	data.sort(key= lambda x: x[1])
	
	if stop:
		sys.exit(1)

	if args.verbose:
		print("")

	if len(data) == 0:
		print(f'E:> No data was loaded!', file = sys.stderr)
		sys.exit(1)

	if args.verbose:
		print(f'I:> A total of {len(data)} traces was found!')

	if args.correlation and args.pair is None:
		print(f'E:> ', file = sys.stderr)
		print(f'E:> Indicate a pair of events plot with option --pair One/Another.', file = sys.stderr)
		print(f'E:> Loaded ids are:', file = sys.stderr)
		for evid,_,_ in data:
			print(f'E:>   {evid}', file = sys.stderr)
		stop = True

	if args.pair:
		eva,evb = args.pair.split("/")
		valids = [ evid for evid,_,_ in data ]

		if eva not in valids:
			print(f'E:> Event id: \'{eva}\' not in {"/".join(valids)}', file = sys.stderr)
			stop = True

		if evb not in valids:
			print(f'E:> Event id: \'{evb}\' not in {"/".join(valids)}', file = sys.stderr)
			stop = True

	if stop:
		sys.exit(1)

	##
	# Compute matrix
	##
	results, labels = build_corr_matrix(data, args)

	##
	# Generate desired outputs
	##
	
	# Matrix plot
	if args.matrix:
		plot_matrix(data, results, labels, args)

	# All graph plot
	if args.waveform:
		plot_waveforms(data, results, labels, args)

	# Seismograms plot
	if args.correlation:
		plot_correlation(data, results, labels, args)

	sys.exit(0)
