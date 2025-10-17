# Linopy Backend - Quick Start Guide

This guide helps you get started with the linopy backend for EnergyScope.

## What is Linopy?

[Linopy](https://linopy.readthedocs.io/) is a Python library for linear and mixed-integer optimization. Unlike AMPL, it's pure Python and allows you to define optimization models programmatically.

## Why Add Linopy Support?

1. **Pure Python** - No need for AMPL license or installation
2. **Open Source** - Fully open-source workflow
3. **Flexibility** - Easier to extend and modify models programmatically
4. **Integration** - Better integration with Python data science ecosystem

## Installation

### Basic Installation (AMPL only)
```bash
pip install -e .
```

### With Linopy Support
```bash
pip install -e ".[linopy]"
```

### With All Optional Dependencies
```bash
pip install -e ".[all]"
```

### Solvers

You'll also need a solver. Options:

**HiGHS (recommended for testing - free)**
```bash
pip install highspy
```

**Gurobi (recommended for production - requires license)**
```bash
pip install gurobipy
# Requires a Gurobi license (free for academics)
```

## Running the Toy Model

### Using the Example Script

```bash
python scripts/linopy_model.py
```

Expected output:
```
Loading toy model data...

Model configuration:
  Technologies: ['PV', 'WIND', 'GAS_PLANT', 'BATTERY', 'GRID']
  Layers: ['ELECTRICITY', 'GAS', 'END_USE']
  Time periods: 24 hours
  Storage technologies: ['BATTERY']

Building and solving linopy model...
Solver: gurobi

Solution status: ok
Objective value: 123.45 M€

=== Installed Capacity (F) ===
...

✓ Model solved successfully!
```

### Programmatic Usage

```python
from energyscope.linopy_backend.data_loader import create_toy_data
from energyscope.linopy_backend.toy_model import solve_toy_model
from energyscope.linopy_backend.result_parser import parse_linopy_result

# Load data
data = create_toy_data()

# Solve
model, solution = solve_toy_model(data, solver='gurobi')

# Parse results
result = parse_linopy_result(model, data)

# Access results
print(f"Total cost: {model.objective.value}")
print(result.variables['F'])  # Installed capacities
```

## Current Implementation Status

### ✅ Implemented (Toy Model)

- **Phase 1**: Infrastructure setup
  - LinopyModel class
  - Data loading utilities
  - Result parser
  
- **Phase 2**: Toy model
  - 5 technologies (PV, Wind, Gas, Battery, Grid)
  - 3 layers (Electricity, Gas, End-use)
  - 24-hour time horizon
  - Basic constraints:
    - Energy balance
    - Capacity limits
    - Simple storage
    - Cost minimization

### 🚧 In Progress

None yet - see Phase 3 in the migration strategy

### 📋 Planned (Phase 3+)

- Full core model with all 37 constraints
- Infrastructure module
- LCA module
- Transition/pathway model
- Validation against AMPL results

See [linopy_migration_strategy.md](linopy_migration_strategy.md) for complete roadmap.

## Running Tests

### Without Solver (basic tests only)
```bash
pytest tests/test_linopy_toy_model.py
```

### With Solver
```bash
pytest tests/test_linopy_toy_model.py --run-solver-tests
```

## Development Workflow

### 1. Create Data

```python
from energyscope.linopy_backend.data_loader import ModelData

# Option A: Use toy data
data = create_toy_data()

# Option B: Create custom data
data = ModelData.from_dict({
    'sets': {
        'TECHNOLOGIES': ['TECH1', 'TECH2'],
        ...
    },
    'parameters': {
        'f_max': {'TECH1': 10, 'TECH2': 20},
        ...
    },
    'time_series': {
        'demand': pd.Series([...]),
    }
})
```

### 2. Build Model

```python
import linopy
from energyscope.linopy_backend.toy_model import build_toy_model

model = build_toy_model(data)

# Inspect model
print(f"Variables: {list(model.variables.keys())}")
print(f"Constraints: {len(model.constraints)}")
```

### 3. Solve

```python
# Solve with specific solver
model.solve(solver_name='gurobi')

# Or use helper function
from energyscope.linopy_backend.toy_model import solve_toy_model
model, solution = solve_toy_model(data, solver='highs')
```

### 4. Parse Results

```python
from energyscope.linopy_backend.result_parser import parse_linopy_result

result = parse_linopy_result(model, data)

# Result has same structure as AMPL results
print(result.objectives)   # Objective values
print(result.variables)    # Decision variables
print(result.parameters)   # Input parameters
print(result.sets)         # Sets
```

## Comparing AMPL and Linopy Results

Once you have both backends implemented:

```python
from energyscope.linopy_backend.result_parser import compare_results

# Solve with AMPL
result_ampl = es_ampl.calc()

# Solve with Linopy  
result_linopy = es_linopy.calc()

# Compare
comparison = compare_results(result_ampl, result_linopy, rtol=1e-4)

if comparison['success']:
    print("✓ Results match!")
else:
    print("✗ Discrepancies found:")
    for msg in comparison['messages']:
        print(f"  - {msg}")
```

## Troubleshooting

### Import Error: No module named 'linopy'

Install linopy:
```bash
pip install -e ".[linopy]"
```

### Solver Error

Make sure you have a solver installed:
```bash
# For HiGHS
pip install highspy

# Check if Gurobi is available
python -c "import gurobipy; print('Gurobi available')"
```

### Different Results from AMPL

This is expected during development. Check:
1. Are all constraints implemented?
2. Are solver tolerances the same?
3. Are there numerical precision differences?

Use the `compare_results` function to identify specific differences.

## Next Steps

1. **Validate Toy Model** - Compare with equivalent AMPL model
2. **Add Constraints** - Follow Phase 3 of migration strategy
3. **Test Incrementally** - Add one constraint group at a time
4. **Document** - Update this guide as you progress

## Resources

- [Linopy Documentation](https://linopy.readthedocs.io/)
- [Linopy Examples](https://linopy.readthedocs.io/en/latest/examples.html)
- [Migration Strategy](linopy_migration_strategy.md)
- [AMPL Core Model](../src/energyscope/data/models/core/td/ESTD_model_core.mod)

## Support

For issues or questions:
1. Check the [migration strategy](linopy_migration_strategy.md)
2. Look at existing test cases in `tests/`
3. Open an issue on GitLab

## Contributing

Contributions to the linopy backend are welcome! See the migration strategy for areas needing work.

