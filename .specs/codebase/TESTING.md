# Testing Infrastructure

## Test Frameworks

- Unit tests: not present
- Integration tests: not present as test suite
- E2E tests: not present
- Coverage tooling: not present

## Current Validation Approach

The project currently uses manual/scientific validation:
- Run script against known event IDs and inspect generated figures.
- Compare correlation and offset outputs visually and numerically.
- Iterate parameters (`window`, filters, correction shift) to evaluate behavior.

## Test Organization

Location:
- No dedicated `tests/` directory.

Naming:
- Not applicable (no automated tests).

Structure:
- Operational checks are encoded in `Makefile` targets:
- `test_ids`: accepts IDs directly.
- `test_file`: reads IDs from a text file.

## Test Execution

Main commands:

```bash
make test_ids ids="val2024gnbo val2024gmvf val2025gmvl"
make test_file file=cluster1.txt
```

Static syntax check used during mapping:

```bash
python3 -m py_compile analysis.py cluster_map.py correlation.py
```

Result on 2026-02-20: syntax compilation successful for all three scripts.

## Residual Risk

- No regression safety net for refactors.
- No mocked tests for FDSN interactions.
- No deterministic fixtures; runtime depends on external service availability and returned data.
