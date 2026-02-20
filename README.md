# IC-Seismology-2025
Data and codes developed during my scientific initiation in seismology at Center of Seismology (IAG-USP).

## Objective
Develop a code for automatic P pick correction for aftershocks based on the maximum correlation with the main event.

## Method
Gets and cut data from a given FDSN Client, interval (in seconds) and event(s) ID(s). After that, the code makes data cross-correlation, generates and saves as figure: 1. Correlation matrix; 2. Time correction times matrix; 3. A post P pick time correction seismogram with superposed waveforms.

## Setup
Install dependencies from `requirements.txt`:

```bash
python3.13 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

Supported Python versions: `3.12` and `3.13`.

If `python3.13` is not available on your system, install it first (or use `python3.12`).

## Smoke tests (Makefile)
Default `Makefile` settings now assume the seisarc tunnel on localhost:
- FDSN: `http://127.0.0.1:28080/`
- Station: `BL.RVDE..HHZ`

Run:

```bash
make check_fdsn
make test_ids ids="usp2026doac usp2026dmwl usp2026dmvw"
make test_file file=cluster1.txt
```

You can always override defaults, for example:

```bash
make test_ids ids="..." station=BL.AQDB..HHZ fdsn=http://127.0.0.1:28080/
```
