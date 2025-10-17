# Linopy Migration Strategy for EnergyScope

## Executive Summary

This document outlines a systematic strategy to add linopy support to EnergyScope alongside the existing AMPL implementation. The goal is to translate the AMPL model (397 lines, 37 constraints, 1 objective) into linopy while maintaining compatibility and verification.

## Architecture Overview

### Current Structure
```
Model (models.py)
  └── list of (type, file_path) tuples
       └── AMPL reads .mod and .dat files
            └── Energyscope class handles solve
                 └── Result parser extracts outputs
```

### Target Structure (Dual Backend)
```
Model (models.py)
  ├── AMPL Backend (existing)
  │    └── .mod/.dat files
  └── Linopy Backend (new)
       └── Python model builders
```

## Phase 1: Infrastructure Setup

### 1.1 Create New Module Structure
- Create `src/energyscope/linopy_backend/` directory
- Files to create:
  - `__init__.py` - Module initialization
  - `base_model.py` - Base linopy model builder
  - `core_model.py` - Core model implementation
  - `result_parser.py` - Linopy result to Result class converter
  - `data_loader.py` - Load .dat files or Python data structures

### 1.2 Update Dependencies
- Add linopy to `pyproject.toml`
- Add required solver interfaces (highspy, gurobipy interfaces)

### 1.3 Create Linopy Model Class
- New class: `LinopyModel` (analogous to AMPL `Model`)
- Stores reference to builder function instead of file paths
- Example: `core_linopy = LinopyModel(builder=build_core_model)`

### 1.4 Update Energyscope Class
- Detect model backend type (AMPL vs Linopy)
- Route to appropriate solver
- Ensure common Result interface

## Phase 2: Minimal Model Implementation

### 2.1 Simplify Core Model (Create "Toy Model")
Start with a drastically simplified version with:
- **5 technologies** (e.g., PV, Wind, Gas, Battery, Grid)
- **3 layers** (Electricity, Gas, End-use)
- **24 time periods** (1 day, hourly)
- **Core constraints only**:
  1. Energy balance
  2. Capacity limits
  3. Resource availability
  4. Simple storage balance
  5. Total cost objective

### 2.2 Implementation Steps for Toy Model

#### Step 1: Data Structures
```python
# Define sets using simple Python structures
TECHNOLOGIES = ['PV', 'WIND', 'GAS_PLANT', 'BATTERY', 'GRID']
LAYERS = ['ELECTRICITY', 'GAS', 'END_USE']
PERIODS = range(1, 25)  # 24 hours

# Parameters as dictionaries or DataFrames
f_max = {'PV': 10, 'WIND': 5, ...}
c_inv = {'PV': 100, 'WIND': 150, ...}
layers_in_out = {...}  # Tech-layer matrix
```

#### Step 2: Create Linopy Model
```python
import linopy

def build_toy_model(data):
    m = linopy.Model()
    
    # Variables
    F = m.add_variables(name="F", lower=0, coords=[TECHNOLOGIES])
    F_t = m.add_variables(name="F_t", lower=0, coords=[TECHNOLOGIES, PERIODS])
    
    # Constraints
    # 1. Capacity constraint
    # 2. Energy balance
    # 3. Resource limits
    
    # Objective
    m.add_objective(...)
    
    return m
```

#### Step 3: Test Equivalence
- Export toy model from AMPL
- Solve with AMPL/Gurobi
- Solve with Linopy/Gurobi  
- Compare:
  - Objective values (should match within tolerance)
  - Variable values (F, F_t)
  - Dual values if needed

### 2.3 Create Testing Framework
File: `tests/test_linopy_ampl_equivalence.py`
```python
def test_toy_model_equivalence():
    # Solve with AMPL
    es_ampl = Energyscope(model=core_toy_ampl, solver='gurobi')
    result_ampl = es_ampl.calc()
    
    # Solve with Linopy
    es_linopy = Energyscope(model=core_toy_linopy, solver='gurobi')
    result_linopy = es_linopy.calc()
    
    # Compare
    assert_results_close(result_ampl, result_linopy, rtol=1e-4)
```

## Phase 3: Incremental Model Building

### 3.1 Constraint Groups (Add in Order)
Translate constraints one group at a time:

**Group 1: Core Energy Balance** (Priority: Critical)
- `end_uses_t` - Layer balance
- `layer_balance` - Layer balance with technologies
- `capacity_factor_t` - Capacity factor constraints
- `size_limit` - Technology size limits

**Group 2: Resources** (Priority: High)
- `resource_availability` - Resource limits
- `resource_constant_import` - Constant imports

**Group 3: Storage** (Priority: High)
- `storage_level` - Storage state equation
- `storage_layer_in/out` - Storage input/output
- `limit_energy_stored_to_maximum` - Storage capacity
- `impose_daily_storage` - Daily cycling
- `limit_energy_to_power_ratio` - E/P ratio

**Group 4: Costs** (Priority: High)
- `totalcost_cal` - Total cost calculation
- `investment_cost_calc` - Investment costs
- `main_cost_calc` - Maintenance costs
- `op_cost_calc` - Operating costs

**Group 5: GWP Constraints** (Priority: Medium)
- `totalGWP_calc` - Total GWP
- `gwp_constr_calc` - Construction GWP
- `gwp_op_calc` - Operational GWP
- `Minimum_GWP_reduction` - GWP limits

**Group 6: Mobility** (Priority: Medium)
- `operating_strategy_mob_passenger`
- `operating_strategy_mobility_freight`
- `Freight_shares`
- `EV_storage_size`
- `EV_storage_for_V2G_demand`

**Group 7: Heating** (Priority: Medium)
- `thermal_solar_capacity_factor`
- `thermal_solar_total_capacity`
- `decentralised_heating_balance`

**Group 8: Network & Infrastructure** (Priority: Low)
- `network_losses`
- `extra_grid`
- `extra_dhn`
- `extra_efficiency`

**Group 9: Policy Constraints** (Priority: Low)
- `f_max_perc` / `f_min_perc` - Technology share limits
- `solar_area_limited` - Area constraints

### 3.2 Workflow for Each Group
For each constraint group:
1. **Study AMPL syntax** - Understand the mathematical formulation
2. **Translate to linopy** - Write equivalent Python/linopy code
3. **Unit test** - Test constraint in isolation if possible
4. **Integration test** - Solve model with new constraints
5. **Verification** - Compare with AMPL results
6. **Document** - Add comments explaining the constraint

### 3.3 Translation Patterns

#### Pattern 1: Simple Linear Constraint
```ampl
# AMPL
subject to capacity_limit {j in TECHNOLOGIES}:
    F[j] <= f_max[j];
```
```python
# Linopy
for j in TECHNOLOGIES:
    m.add_constraints(F[j] <= f_max[j], name=f"capacity_limit_{j}")
```

#### Pattern 2: Indexed Constraint
```ampl
# AMPL
subject to balance {l in LAYERS, t in PERIODS}:
    sum{j in TECH} (F_t[j,t] * layers_out[j,l]) >= demand[l,t];
```
```python
# Linopy - vectorized
import xarray as xr
# Create coefficient array
coef = xr.DataArray(layers_out, coords=[TECH, LAYERS])
# Constraint
for l in LAYERS:
    for t in PERIODS:
        m.add_constraints(
            (F_t.sel(TECHNOLOGIES=TECH) * coef.sel(LAYERS=l)).sum('TECHNOLOGIES') 
            >= demand[l,t],
            name=f"balance_{l}_{t}"
        )
```

#### Pattern 3: Conditional Constraints
```ampl
# AMPL
subject to storage_only_if {j in STORAGE_TECH}:
    constraint_expr;
```
```python
# Linopy
for j in STORAGE_TECH:  # Subset
    m.add_constraints(constraint_expr, name=f"storage_{j}")
```

## Phase 4: Data Management

### 4.1 Data Loading Strategy
Two approaches:

**Option A: Reuse .dat files**
- Parse AMPL .dat files using amplpy
- Extract parameter values into Python structures
- Pro: Reuses existing data
- Con: Dependency on AMPL for data

**Option B: Native Python data**
- Create Python data loaders (JSON, CSV, pickle)
- Convert .dat to native format
- Pro: Independent of AMPL
- Con: Need to maintain two data formats

**Recommended: Hybrid**
- Phase 1-3: Use Option A for speed
- Phase 4+: Migrate to Option B for independence

### 4.2 Data Structure
```python
@dataclass
class ModelData:
    sets: dict[str, list]
    parameters: dict[str, pd.DataFrame | dict | float]
    time_series: dict[str, pd.DataFrame]
    
    @classmethod
    def from_ampl_dat(cls, dat_files: list):
        # Parse AMPL .dat files
        pass
    
    @classmethod
    def from_json(cls, json_file: str):
        # Load from JSON
        pass
```

## Phase 5: Result Parser

### 5.1 Linopy Result → Result Class
Create mapping from linopy solution to Result dataclass:

```python
def parse_linopy_result(linopy_model, linopy_solution, id_run=None) -> Result:
    """Convert linopy solution to energyscope Result format"""
    
    variables = {}
    for var_name, var in linopy_model.variables.items():
        # Extract solution values
        df = var.solution.to_pandas()
        variables[var_name] = df
    
    objectives = {
        'obj': pd.DataFrame({'obj': [linopy_model.objective.value]})
    }
    
    # Parameters from model data
    parameters = {...}
    
    # Sets from model data
    sets = {...}
    
    return Result(
        variables=variables,
        objectives=objectives,
        parameters=parameters,
        sets=sets
    )
```

### 5.2 Ensure Compatibility
- Result structure must match AMPL version
- DataFrame indices must be consistent
- Column names must match
- Allows downstream plotting/analysis code to work unchanged

## Phase 6: Integration into Energyscope Class

### 6.1 Model Type Detection
```python
# models.py
@dataclass
class LinopyModel:
    builder: Callable
    data_loader: Callable
    backend: str = 'linopy'

# Existing Model class gets backend attribute
@dataclass  
class Model:
    files: list[tuple[str, Path]]
    backend: str = 'ampl'
```

### 6.2 Update Energyscope.__init__
```python
class Energyscope:
    def __init__(self, model: Model | LinopyModel, ...):
        self.model = model
        self.backend = getattr(model, 'backend', 'ampl')
        # ...
```

### 6.3 Backend Router in calc()
```python
def calc(self, ds: Dataset = None, ...) -> Result:
    if self.backend == 'ampl':
        return self._calc_ampl(ds, ...)
    elif self.backend == 'linopy':
        return self._calc_linopy(ds, ...)
    
def _calc_linopy(self, ds: Dataset = None, ...) -> Result:
    # Build model
    data = self.model.data_loader(ds)
    lp_model = self.model.builder(data)
    
    # Solve
    lp_model.solve(solver_name=self.solver_options['solver'])
    
    # Parse result
    return parse_linopy_result(lp_model, lp_model.solution)
```

## Phase 7: Testing & Verification

### 7.1 Test Levels

**Unit Tests**
- Individual constraint translation
- Data loaders
- Result parsers

**Integration Tests**
- Full model solve
- AMPL vs Linopy comparison
- Different solvers (Gurobi, HiGHS, CPLEX)

**Regression Tests**
- Known scenarios with expected results
- Performance benchmarks

### 7.2 Verification Metrics
```python
def assert_results_close(result_ampl, result_linopy, rtol=1e-4):
    # Objective value
    obj_ampl = result_ampl.objectives['obj'].values[0]
    obj_linopy = result_linopy.objectives['obj'].values[0]
    np.testing.assert_allclose(obj_ampl, obj_linopy, rtol=rtol)
    
    # Key variables (F, F_t, etc.)
    for var_name in ['F', 'F_t', 'Storage_level']:
        if var_name in result_ampl.variables:
            df_ampl = result_ampl.variables[var_name].sort_index()
            df_linopy = result_linopy.variables[var_name].sort_index()
            np.testing.assert_allclose(
                df_ampl.values, 
                df_linopy.values, 
                rtol=rtol,
                err_msg=f"Mismatch in {var_name}"
            )
```

### 7.3 Performance Testing
- Solve time comparison (linopy may be slower for small models)
- Memory usage
- Scaling with problem size

## Phase 8: Documentation

### 8.1 User Documentation
- Tutorial: How to use linopy backend
- Examples: `scripts/linopy_model.py`
- API reference

### 8.2 Developer Documentation  
- Translation guide (AMPL → linopy patterns)
- How to add new constraints
- Contribution guidelines

## Phase 9: Advanced Features

### 9.1 Model Modularity
Once core model works:
- Infrastructure module (linopy version)
- LCA module (linopy version)
- Transition/pathway module

### 9.2 Performance Optimization
- Vectorized operations
- Sparse matrix usage
- Lazy constraint generation

## Implementation Timeline Estimate

| Phase | Estimated Time | Deliverable |
|-------|----------------|-------------|
| 1. Infrastructure | 1-2 days | Module structure, dependencies |
| 2. Toy Model | 2-3 days | Working minimal model, test passing |
| 3. Group 1-2 (Core) | 3-5 days | Energy balance, resources |
| 3. Group 3-4 (Storage/Cost) | 3-5 days | Storage, cost calculations |
| 3. Group 5-9 (Rest) | 5-7 days | All remaining constraints |
| 4. Data Management | 2-3 days | Data loaders |
| 5. Result Parser | 1-2 days | Complete Result compatibility |
| 6. Integration | 1-2 days | Unified Energyscope interface |
| 7. Testing | 3-5 days | Comprehensive test suite |
| 8. Documentation | 2-3 days | Docs and examples |
| **Total** | **23-37 days** | Full linopy support |

## File Organization

```
energyscope/
├── src/energyscope/
│   ├── linopy_backend/
│   │   ├── __init__.py
│   │   ├── base_model.py
│   │   ├── core_model.py           # build_core_model()
│   │   ├── infrastructure_model.py
│   │   ├── data_loader.py
│   │   └── result_parser.py
│   ├── models.py                    # Add LinopyModel class
│   ├── energyscope.py               # Update with backend routing
│   └── ...
├── scripts/
│   ├── ampl_model.py               # Existing
│   ├── python_model.py             # Existing  
│   └── linopy_model.py             # New example
├── tests/
│   ├── test_linopy_equivalence.py
│   ├── test_linopy_constraints.py
│   └── test_linopy_data_loading.py
└── docs/
    └── linopy_migration_strategy.md  # This file
```

## Risk Mitigation

### Risk 1: Complex AMPL Syntax
- **Mitigation**: Start with simple constraints, build pattern library
- Export AMPL model to see expanded form

### Risk 2: Performance Issues
- **Mitigation**: Focus on correctness first, optimize later
- Use linopy best practices (vectorization, sparse)

### Risk 3: Numerical Differences
- **Mitigation**: Use appropriate tolerances (1e-4 to 1e-6)
- Document expected differences
- May need to tune solver settings

### Risk 4: Maintenance Burden
- **Mitigation**: Shared test suite ensures both backends stay in sync
- Good documentation for future developers
- Consider making AMPL version read-only after linopy is stable

## Success Criteria

1. ✅ Linopy model solves without errors
2. ✅ Objective value matches AMPL (within 0.1%)
3. ✅ Key variables match AMPL (within 0.1%)
4. ✅ All 37 constraints translated
5. ✅ Solver time within 2x of AMPL
6. ✅ Compatible with existing plotting/analysis tools
7. ✅ Full test coverage (>80%)
8. ✅ Documentation complete
9. ✅ Example scripts working

## Next Steps

1. Review this strategy with team
2. Set up Phase 1 (infrastructure)
3. Create toy model (Phase 2)
4. Begin incremental constraint translation (Phase 3)

## References

- [Linopy Documentation](https://linopy.readthedocs.io/)
- [AMPL Model: ESTD_model_core.mod](../src/energyscope/data/models/core/td/ESTD_model_core.mod)
- [Current Result Structure](../src/energyscope/result.py)

