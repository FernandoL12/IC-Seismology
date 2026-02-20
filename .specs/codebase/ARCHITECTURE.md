# Architecture

Pattern: Script-centric scientific workflow (single-module core + analysis helpers + notebook prototype)

## High-Level Structure

1. Event IDs are obtained from manual lists or date windows.
2. P-phase picks are fetched from FDSN event metadata.
3. Waveforms are fetched for selected stations/time windows.
4. Cross-correlation computes lag/offset between event pairs.
5. Corrected traces are trimmed to comparable windows.
6. Correlation and offset matrices are assembled and plotted.

## Main Components

### `correlation.py`

Location: `correlation.py`
Purpose: Main processing engine and CLI entrypoint.
Implementation:
- Input parsing (`cmdline`)
- Event picks and waveform extraction (`evpicks`, `evtrace`)
- Cross-correlation and sub-sample lag refinement (`Ppick_cc`)
- Pairwise processing (`corr_matrix`)
- Matrix builders (`assembly_matrix`, `assembly_off`)
- Visualization (`plot_matrix`, `plot_graph`, `plot_offset`, `plot_all`)
Example:
- `corr_matrix(...)` loops through event pairs and stores `AttribDict` result records.

### `analysis.py`

Location: `analysis.py`
Purpose: Offline event filtering, clustering by date ranges, and cluster statistics.
Implementation:
- Reads `induced.txt` with `numpy.loadtxt`
- Converts/sorts by `UTCDateTime`
- Creates fixed temporal clusters (`cluster1..3`)
- Writes cluster ID files and summary metrics (`Clusters.txt`)
Example:
- `get_ids(start_date, end_date, dates, evid)` selects IDs in time intervals.

### `cluster_map.py`

Location: `cluster_map.py`
Purpose: Build and map a catalog for a specific cluster list.
Implementation:
- Reads `cluster1.txt`
- Fetches events from FDSN
- Builds an ObsPy `Catalog` and plots local projection map.

### `Correlation.ipynb`

Location: `Correlation.ipynb`
Purpose: Exploratory/prototyping environment that predates or parallels `correlation.py`.
Implementation:
- Contains iterative versions of core functions
- Includes manual experiments, TODOs, and plotting diagnostics
- Not production-hardened (contains exploratory cells and partial snippets)

## Data Flow

### Flow A: Correlation CLI

1. User invokes `correlation.py` with station/events/window/filter options.
2. For each event pair, code fetches picks and waveforms.
3. If correction is enabled, code estimates offset via cross-correlation.
4. Code trims traces to equal sample counts and computes normalized pair correlation.
5. Code generates figures and prints offsets/sorted pair quality.

### Flow B: Cluster Preparation

1. User prepares `induced.txt` from `eventos.txt` filtering.
2. `analysis.py` segments time windows into fixed clusters.
3. Cluster ID files feed downstream processing (`Makefile` -> `correlation.py`, or `cluster_map.py`).

## Code Organization

Approach: Flat repository with module-level functions; no package layout.

- Domain logic: `correlation.py`
- Dataset preprocessing: `analysis.py`
- Mapping utility: `cluster_map.py`
- Workflow docs/commands: `README.md`, `extract-dados-ex.txt`, `Makefile`
- Experimental notebooks: `Correlation.ipynb`

## Notable Technical Risks

- Strong reliance on global state in plotting helpers (`plot_matrix`/`plot_offset` read global `station`).
- `phase == "S"` branch in main path references undefined symbols (`shiftmargin`) and mismatched call signature, indicating incomplete path.
- No dependency lockfile/environment specification, so reproducibility depends on local setup.
