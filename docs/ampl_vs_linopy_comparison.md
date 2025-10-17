# AMPL vs Linopy: Comparison Guide

This document helps you understand the differences between the AMPL and linopy backends for EnergyScope.

## Quick Comparison Table

| Aspect | AMPL Backend | Linopy Backend |
|--------|--------------|----------------|
| **Language** | AMPL (algebraic modeling) | Python |
| **License** | Commercial (free academic) | Open source (MIT) |
| **Installation** | Requires AMPL installation | `pip install linopy` |
| **Model Definition** | `.mod` files (text) | Python functions |
| **Data Format** | `.dat` files | Python dicts/DataFrames |
| **Solver Interface** | Through AMPL | Direct (via linopy) |
| **Extensibility** | Harder (text parsing) | Easier (pure Python) |
| **Performance** | Generally fast | Comparable (TBD) |
| **Debugging** | Limited | Full Python debugging |
| **IDE Support** | Text editors | Full Python IDE features |
| **Version Control** | Good (text files) | Good (Python code) |
| **Learning Curve** | Learn AMPL syntax | Use Python knowledge |
| **Community** | Established (AMPL) | Growing (linopy) |
| **Maturity** | Very mature | Relatively new |

## Translation Examples

### Example 1: Sets

#### AMPL
```ampl
set TECHNOLOGIES;
set STORAGE_TECH within TECHNOLOGIES;
set PERIODS := 1..8760;
```

#### Linopy (Python)
```python
TECHNOLOGIES = ['PV', 'WIND', 'GAS', ...]
STORAGE_TECH = ['BATTERY', 'HYDRO_STORAGE', ...]
PERIODS = list(range(1, 8761))
```

### Example 2: Parameters

#### AMPL
```ampl
param f_max {TECHNOLOGIES} >= 0;
param c_inv {TECHNOLOGIES} >= 0;
param layers_in_out {TECHNOLOGIES, LAYERS};
```

#### Linopy (Python)
```python
# Option 1: Dictionary
f_max = {'PV': 10, 'WIND': 5, 'GAS': 8}
c_inv = {'PV': 100, 'WIND': 150, 'GAS': 80}

# Option 2: DataFrame
layers_in_out = pd.DataFrame({
    'ELECTRICITY': {'PV': 1.0, 'WIND': 1.0, 'GAS': 0.4},
    'GAS': {'PV': 0.0, 'WIND': 0.0, 'GAS': -1.0},
})
```

### Example 3: Variables

#### AMPL
```ampl
var F {TECHNOLOGIES} >= 0, <= f_max;
var F_t {TECHNOLOGIES, PERIODS} >= 0;
```

#### Linopy
```python
import linopy

m = linopy.Model()

# With explicit bounds
F = m.add_variables(
    lower=0,
    upper=f_max,
    coords=[TECHNOLOGIES],
    name="F"
)

# With default bounds
F_t = m.add_variables(
    lower=0,
    coords=[TECHNOLOGIES, PERIODS],
    name="F_t"
)
```

### Example 4: Simple Constraint

#### AMPL
```ampl
subject to capacity_limit {j in TECHNOLOGIES, t in PERIODS}:
    F_t[j,t] <= F[j] * c_p_t[j,t];
```

#### Linopy
```python
# Option 1: Loop (simpler, but slower for large models)
for j in TECHNOLOGIES:
    for t in PERIODS:
        m.add_constraints(
            F_t.loc[j, t] <= F.loc[j] * c_p_t.loc[j, t],
            name=f"capacity_limit_{j}_{t}"
        )

# Option 2: Vectorized (faster)
capacity_limit = F_t <= F * c_p_t
m.add_constraints(capacity_limit, name="capacity_limit")
```

### Example 5: Summation Constraint

#### AMPL
```ampl
subject to energy_balance {l in LAYERS, t in PERIODS}:
    sum {j in TECHNOLOGIES} (F_t[j,t] * layers_in_out[j,l]) >= demand[l,t];
```

#### Linopy
```python
# Using xarray for vectorized operations
import xarray as xr

# Create coefficient array
coef = xr.DataArray(
    layers_in_out.values,
    coords=[TECHNOLOGIES, LAYERS],
    dims=['tech', 'layer']
)

# For each layer and time
for l in LAYERS:
    for t in PERIODS:
        production = (F_t.sel(TECHNOLOGIES=slice(None), PERIODS=t) * 
                     coef.sel(layer=l)).sum('TECHNOLOGIES')
        m.add_constraints(
            production >= demand.loc[l, t],
            name=f"energy_balance_{l}_{t}"
        )
```

### Example 6: Conditional Constraints

#### AMPL
```ampl
subject to storage_constraint {j in STORAGE_TECH, t in PERIODS}:
    Storage_level[j,t] <= F[j];
```

#### Linopy
```python
# Simply iterate over the subset
for j in STORAGE_TECH:
    for t in PERIODS:
        m.add_constraints(
            Storage_level.loc[j, t] <= F.loc[j],
            name=f"storage_constraint_{j}_{t}"
        )
```

### Example 7: Objective Function

#### AMPL
```ampl
minimize TotalCost:
    sum {j in TECHNOLOGIES} (F[j] * c_inv[j]) +
    sum {j in TECHNOLOGIES} (F[j] * c_maint[j]) +
    sum {i in RESOURCES, t in PERIODS} (R_t[i,t] * c_op[i]);
```

#### Linopy
```python
# Build objective as sum of terms
investment_cost = sum(F.loc[j] * c_inv[j] for j in TECHNOLOGIES)
maintenance_cost = sum(F.loc[j] * c_maint[j] for j in TECHNOLOGIES)
operating_cost = sum(R_t.loc[i,t] * c_op[i] 
                     for i in RESOURCES 
                     for t in PERIODS)

total_cost = investment_cost + maintenance_cost + operating_cost
m.add_objective(total_cost, sense="min")
```

## Common Patterns

### Pattern 1: Set Operations

#### AMPL
```ampl
set TECH_NO_STORAGE := TECHNOLOGIES diff STORAGE_TECH;
set LAYERS := RESOURCES union END_USES_TYPES;
set TECH_SUBSET within TECHNOLOGIES;
```

#### Python/Linopy
```python
# Difference (set subtraction)
TECH_NO_STORAGE = [t for t in TECHNOLOGIES if t not in STORAGE_TECH]
# Or using sets:
TECH_NO_STORAGE = list(set(TECHNOLOGIES) - set(STORAGE_TECH))

# Union
LAYERS = list(set(RESOURCES) | set(END_USES_TYPES))

# Subset (just filtering)
TECH_SUBSET = [t for t in TECHNOLOGIES if some_condition(t)]
```

### Pattern 2: Indexed Parameters

#### AMPL
```ampl
param end_uses_input {i in END_USES_INPUT} := 
    sum {s in SECTORS} (end_uses_demand_year[i,s]);
```

#### Python
```python
# Using pandas
end_uses_input = end_uses_demand_year.sum(axis=1)  # Sum over sectors

# Or explicit:
end_uses_input = {
    i: sum(end_uses_demand_year.loc[i, s] for s in SECTORS)
    for i in END_USES_INPUT
}
```

### Pattern 3: Time-dependent Constraints

#### AMPL
```ampl
subject to storage_balance {j in STORAGE_TECH, t in PERIODS: t > 1}:
    Storage_level[j,t] = Storage_level[j,t-1] + 
                         Storage_in[j,t] - Storage_out[j,t];
```

#### Python/Linopy
```python
for j in STORAGE_TECH:
    for i, t in enumerate(PERIODS):
        if i == 0:
            # Initial condition
            m.add_constraints(
                Storage_level.loc[j, t] == initial_storage[j] + 
                Storage_in.loc[j, t] - Storage_out.loc[j, t],
                name=f"storage_balance_{j}_{t}_initial"
            )
        else:
            prev_t = PERIODS[i-1]
            m.add_constraints(
                Storage_level.loc[j, t] == Storage_level.loc[j, prev_t] +
                Storage_in.loc[j, t] - Storage_out.loc[j, t],
                name=f"storage_balance_{j}_{t}"
            )
```

## Data Management

### AMPL Approach

**File**: `data.dat`
```ampl
param f_max :=
    PV 10
    WIND 5
    GAS 8
;

param layers_in_out :=
[*,*]:  ELECTRICITY  GAS :=
PV      1.0          0.0
WIND    1.0          0.0
GAS     0.4         -1.0
;
```

### Linopy Approach

**Option 1: Python dictionaries**
```python
f_max = {'PV': 10, 'WIND': 5, 'GAS': 8}
layers_in_out = {
    ('PV', 'ELECTRICITY'): 1.0,
    ('PV', 'GAS'): 0.0,
    ('WIND', 'ELECTRICITY'): 1.0,
    ('WIND', 'GAS'): 0.0,
    ('GAS', 'ELECTRICITY'): 0.4,
    ('GAS', 'GAS'): -1.0,
}
```

**Option 2: JSON file**
```json
{
  "f_max": {"PV": 10, "WIND": 5, "GAS": 8},
  "layers_in_out": {
    "PV": {"ELECTRICITY": 1.0, "GAS": 0.0},
    "WIND": {"ELECTRICITY": 1.0, "GAS": 0.0},
    "GAS": {"ELECTRICITY": 0.4, "GAS": -1.0}
  }
}
```

**Option 3: Pandas DataFrame**
```python
layers_in_out = pd.DataFrame({
    'ELECTRICITY': [1.0, 1.0, 0.4],
    'GAS': [0.0, 0.0, -1.0]
}, index=['PV', 'WIND', 'GAS'])
```

## Solving and Results

### AMPL Workflow

```python
from energyscope import Energyscope
from energyscope.models import core

es = Energyscope(model=core, solver_options={'solver': 'gurobi'})
result = es.calc()

# Access results
print(result.objectives['TotalCost'])
print(result.variables['F'])
```

### Linopy Workflow

```python
from energyscope.linopy_backend import build_toy_model
from energyscope.linopy_backend.data_loader import create_toy_data
from energyscope.linopy_backend.result_parser import parse_linopy_result

# Load data
data = create_toy_data()

# Build and solve
model = build_toy_model(data)
model.solve(solver_name='gurobi')

# Parse results (converts to same format as AMPL)
result = parse_linopy_result(model, data)

# Access results (same interface!)
print(result.objectives['TotalCost'])
print(result.variables['F'])
```

## When to Use Which?

### Use AMPL When:
- ✅ You already have AMPL installed and licensed
- ✅ You have existing AMPL models
- ✅ You need maximum performance (sometimes)
- ✅ You're comfortable with AMPL syntax
- ✅ You want a proven, stable solution

### Use Linopy When:
- ✅ You want an open-source solution
- ✅ You prefer working in Python
- ✅ You want easier model extension/modification
- ✅ You need better IDE support and debugging
- ✅ You want to integrate with Python data science tools
- ✅ You want to avoid licensing issues

### Both Are Good For:
- Solving large-scale linear optimization problems
- Integration with professional solvers (Gurobi, CPLEX, HiGHS)
- Academic research
- Production use (once linopy implementation is complete)

## Performance Considerations

### AMPL
- **Pros**: 
  - Highly optimized
  - Direct solver communication
  - Decades of optimization
- **Cons**:
  - Python ↔ AMPL overhead
  - Data conversion costs

### Linopy
- **Pros**:
  - Pure Python (no conversion overhead)
  - Can use NumPy/xarray optimizations
  - Direct solver interfaces
- **Cons**:
  - Newer, less optimized
  - Python overhead for large models
  - Need to vectorize properly

**Reality**: For models of EnergyScope's size (~10,000-100,000 constraints), both should perform comparably. The solving time (in Gurobi/CPLEX) dominates, not the model building.

## Migration Path

If you want to migrate from AMPL to linopy:

1. **Start with toy/test models** - Validate the approach
2. **Translate incrementally** - One constraint group at a time
3. **Verify results** - Compare with AMPL at each step
4. **Keep both versions** - Don't delete AMPL model yet
5. **Test thoroughly** - Ensure all scenarios work
6. **Switch gradually** - Once confident, use linopy for new work
7. **Maintain AMPL** - Keep as reference/backup

## Common Pitfalls

### Pitfall 1: Index Mismatches
❌ **Wrong**: Assuming 0-based indexing in all places  
✅ **Right**: Be consistent (use 0-based in Python, 1-based if matching AMPL)

### Pitfall 2: Forgetting Efficiency
❌ **Wrong**: Nested loops for everything  
✅ **Right**: Use vectorized operations where possible

### Pitfall 3: Not Testing Early
❌ **Wrong**: Translate everything, then test  
✅ **Right**: Test each constraint group immediately

### Pitfall 4: Ignoring Data Structures
❌ **Wrong**: Using nested dicts for everything  
✅ **Right**: Use pandas DataFrames for tabular data

### Pitfall 5: Over-complicating
❌ **Wrong**: Trying to make linopy code look like AMPL  
✅ **Right**: Write Pythonic code, use Python strengths

## Resources

### AMPL
- [AMPL Documentation](https://ampl.com/resources/the-ampl-book/)
- [AMPL Python API](https://amplpy.readthedocs.io/)

### Linopy
- [Linopy Documentation](https://linopy.readthedocs.io/)
- [Linopy GitHub](https://github.com/PyPSA/linopy)
- [Linopy Examples](https://linopy.readthedocs.io/en/latest/examples.html)

### EnergyScope Linopy
- [Migration Strategy](linopy_migration_strategy.md)
- [Quick Start Guide](linopy_quickstart.md)
- [TODO List](../LINOPY_TODO.md)
- [Implementation Summary](../LINOPY_IMPLEMENTATION_SUMMARY.md)

## Conclusion

Both AMPL and linopy are excellent tools. AMPL is mature and battle-tested. Linopy offers flexibility and open-source benefits. 

With the dual-backend architecture, you get the best of both worlds:
- Use AMPL when you need it
- Use linopy when it fits better
- Same results, same interface
- Choose freely based on your needs

The linopy implementation is designed to be a **complement**, not a replacement. Use what works for you!

