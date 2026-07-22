########################################################################
# Makefile
########################################################################

#===============
# Configuration
#===============
PYTHON := python3
SCRIPT := correlation.py

#====================
# Default parameters
#====================
station := PDRB

window  := P/0.2/0.72

lp      := 10
hp      := 2

dfdsn   := http://10.110.0.134
#http://10.110.0.134
#http://www.sismo.iag.usp.br
#http://seisarc.sismo.iag.usp.br 
#http://10.110.0.135:18003/ <--

shift   := 0.05

#=======================================================================
### HOW TO USE
#-- Direct use:
# python3 correlation.py val2025gnbo val2025gmvf val2025gmvl -S SLBO -w P/1/2 -lp 10 -hp 2 -F http://10.110.0.135:18003/ -c -cs 0.05 --matrix -v
# $(PYTHON) $(SCRIPT) $(input) -S $(station) -w $(window) -lp $(lp) -hp $(hp) -F $(dfdsn) -c -cs $(shift) $(EXTRA_ARGS)
#
#
#-- Makefile use:
#
# make run input="val2025gnbo val2025gmvf"
#
# make run input="cluster1.sac cluster2.sac"
#
# make run input="$(cat cluster1.txt)"
#
# Override defaults:
#
# make run input="..." station=VL.SRN1..HH1
#
# Extra options:
#
# make run input="..." extra="--matrix"
#
# make run input="..." extra="--matrix --save"
#
# make run input="..." extra="--waveform"
#
# make run input="..." extra="--correlation --pair ev1/ev2"
#
#=======================================================================


run:
	@if [ -z "$(input)" ]; then \
		echo "Usage: make run input=\"event1 event2 ...\""; \
		exit 1; \
	fi

	$(PYTHON) $(SCRIPT) \
		$(input) \
		-S $(station) \
		-w $(window) \
		-lp $(lp) \
		-hp $(hp) \
		-F $(dfdsn) \
		-c \
		-cs $(shift) \
		$(extra)
		
		
		
		
		
		
