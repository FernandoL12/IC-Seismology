# External Integrations

## FDSN / ObsPy Data Service

Service: Seismology FDSN endpoints
Purpose: Fetch events, picks, arrivals, and waveforms for correlation analysis.
Implementation locations:
- `correlation.py` (`evpicks`, `evtrace`, `get_event_by_data`, main clients)
- `cluster_map.py`
- `Correlation.ipynb`
Configuration:
- CLI flag: `-F/--fdsn` in `correlation.py`
- Optional event endpoint override: `-E/--event-fdsn`
Authentication:
- None in code (open HTTP endpoints expected)

Observed endpoints:
- `http://10.110.0.135:18003/`
- `http://seisvl.sismo.iag.usp.br/`

## Data Export and Filtering Workflow

Service category: Manual local preprocessing from event exports
Purpose: Build `induced.txt` subset used by `analysis.py`
Implementation locations:
- `extract-dados-ex.txt` command snippets
- `analysis.py` expects `induced.txt`
Configuration:
- Shell filtering by event type field (`"induced earthquake"`)
Authentication:
- Not applicable

## Plotting and Scientific Output

Service category: Local figure generation
Purpose: Persist visual artifacts for scientific inspection and reporting
Implementation locations:
- `correlation.py`
- `analysis.py`
- `cluster_map.py`
Generated artifacts (git-ignored):
- `matrix-corr.png`
- `matrix-off.png`
- `all-graphs.png`
- `process.png`
- `induced-map-by-date.png`

## Notes on Integration Robustness

- Network and service uptime directly affect execution success.
- No retry/backoff logic around FDSN requests.
- No local cache layer for repeated event/waveform retrieval.
