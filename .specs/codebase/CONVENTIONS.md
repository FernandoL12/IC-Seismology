# Code Conventions

## Naming Conventions

Files:
- Predominantly snake_case: `analysis.py`, `cluster_map.py`, `correlation.py`
- Mixed exception with hyphenated helper text file: `extract-dados-ex.txt`

Functions/Methods:
- Lower snake_case: `evpicks`, `evtrace`, `corr_matrix`, `assembly_matrix`, `get_ids`, `write_file`

Variables:
- Lower snake_case for regular variables (`start_date`, `cluster_dict`, `corr_shift`)
- Uppercase temporary scientific markers for algorithm internals (`OFFSET`, `FACTOR1`, `FACTOR2`)

Constants:
- Not centralized; defaults often configured inline in code or Makefile variables.

## Code Organization

Imports:
- Grouped near file top, but no enforced formatter/linter order.
- Some unused imports remain (`pandas` and `correlation` import in `analysis.py`).

File structure:
- Large procedural scripts with function definitions followed by executable block.
- `if __name__ == '__main__':` used in `correlation.py`.

## Type Safety and Documentation

- Type hints are mostly absent.
- Functions include descriptive docstrings (English + Portuguese context/comments).
- Scientific intent frequently explained in comments.

## Error Handling

Pattern:
- Exceptions raised for invalid data states (`no waveform`, missing station, empty lists).
- User-facing prints for recoverable issues (invalid event IDs, availability hints).

Examples:
- `analysis.py`: defensive validation in `statistical(...)` with explicit `ValueError` messages.
- `correlation.py`: graceful fallback in `evpicks` when event ID lookup fails.

## Comments and Documentation Style

- Mixed English/Portuguese comments.
- Frequent section headers separating logical phases (Input, Processing, Visualization).
- README is short and objective; operational details are partly captured in `Makefile` and `extract-dados-ex.txt`.
