# Tech Stack

Analyzed: 2026-02-20

## Core

- Language: Python (scripts with `#!/usr/bin/env python3`)
- Runtime: Python 3 (`Correlation.ipynb` metadata indicates Python 3.12.9 in local environment)
- Execution mode: Script + CLI + notebook workflow
- Package manager: Not defined in repository (no `requirements.txt`, `pyproject.toml`, or `environment.yml`)

## Scientific/Data Libraries

- `numpy` (array operations, statistics, sorting)
- `scipy.signal` (`correlate`, `correlation_lags`)
- `obspy` (`fdsn.Client`, `UTCDateTime`, `AttribDict`, `Catalog`, `Stream`)
- `matplotlib` (plot generation)
- `seaborn` (heatmaps)
- `pandas` (imported in `analysis.py`, not actively used in current code path)

## CLI and Automation

- `argparse` in `correlation.py`
- `Makefile` with reproducible command targets:
- `test_ids`
- `test_file`

## Data and Artifacts

- Input IDs: positional CLI args or text files (`cluster1.txt` style)
- Event catalogs: text exports (`eventos.txt`, `induced.txt` expected locally)
- Outputs (ignored by git):
- `matrix-corr.png`
- `matrix-off.png`
- `all-graphs.png`
- `process.png`
- `induced-map-by-date.png`
- `cluster1.txt`, `cluster2.txt`, `cluster3.txt`, `Clusters.txt`

## External Services

- FDSN event/waveform endpoints consumed via ObsPy clients:
- `http://10.110.0.135:18003/`
- `http://seisvl.sismo.iag.usp.br/` (default in CLI)
