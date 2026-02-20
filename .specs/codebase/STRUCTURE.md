# Project Structure

Root: `.`

## Directory Tree (max depth 3)

```text
.
|-- README.md
|-- Makefile
|-- correlation.py
|-- analysis.py
|-- cluster_map.py
|-- Correlation.ipynb
|-- extract-dados-ex.txt
|-- .gitignore
`-- .specs/
    `-- codebase/
        |-- STACK.md
        |-- ARCHITECTURE.md
        |-- CONVENTIONS.md
        |-- STRUCTURE.md
        |-- TESTING.md
        `-- INTEGRATIONS.md
```

## Module Organization

### Correlation Engine

Purpose: Core P-pick correction and pairwise waveform correlation.
Location: `correlation.py`
Key elements: CLI parser, ObsPy fetch, cross-correlation, matrix assembly, plotting.

### Cluster and Statistics Pipeline

Purpose: Select induced events by date windows and summarize clusters.
Location: `analysis.py`
Key elements: ID filtering, file output, statistics, time vs magnitude plot.

### Spatial Visualization

Purpose: Local map plotting from a cluster file.
Location: `cluster_map.py`
Key elements: FDSN event fetch loop + `Catalog.plot`.

### Experimental Workflow

Purpose: Interactive prototyping and algorithm exploration.
Location: `Correlation.ipynb`
Key elements: iterative function variants, manual tests, TODO notes.

## Where Things Live

Correlation workflow:
- Interface: `Makefile`, CLI args in `correlation.py`
- Business logic: `correlation.py`
- Data access: ObsPy FDSN clients in `correlation.py` and `cluster_map.py`
- Outputs: PNG artifacts listed in `.gitignore`

Cluster generation:
- Interface: direct run of `analysis.py`
- Business logic: `analysis.py`
- Data source expectation: `induced.txt` generated from `eventos.txt`
- Outputs: `cluster*.txt`, `Clusters.txt`

## Special Files

`extract-dados-ex.txt`:
- Purpose: manual command cookbook to extract induced-event rows from raw export files.

`Makefile`:
- Purpose: reproducible invocation of correlation script with defaults and two input styles.
