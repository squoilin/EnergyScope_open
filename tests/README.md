# EnergyScope Tests

This directory contains tests for the EnergyScope package.

## Running Tests

### Basic tests (no solver required)
```bash
pytest tests/
```

### Tests with solver (requires Gurobi or HiGHS)
```bash
pytest tests/ --run-solver-tests
```

### Specific test file
```bash
pytest tests/test_linopy_toy_model.py -v
```

## Test Structure

- `test_linopy_toy_model.py` - Tests for linopy backend toy model
- (More test files to be added)

## Requirements

For linopy tests:
```bash
pip install -e ".[linopy]"
```

For solver tests, you need at least one solver installed:
- HiGHS (free, open-source): `pip install highspy`
- Gurobi (commercial, free academic license)
- CPLEX (commercial)

