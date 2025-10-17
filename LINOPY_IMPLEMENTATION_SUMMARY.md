# Linopy Implementation - Summary

**Date**: October 17, 2025  
**Status**: Phase 1 & 2 Complete - Infrastructure and Toy Model Ready

## What Was Done

I have created a comprehensive strategy and initial implementation for adding linopy support to EnergyScope. Here's what has been set up:

### 1. Strategic Planning

**Documents Created:**
- `docs/linopy_migration_strategy.md` - Complete 37-page strategy document
- `docs/linopy_quickstart.md` - User-facing quick start guide  
- `LINOPY_TODO.md` - Working checklist with detailed tasks

**Strategy Highlights:**
- 10-phase implementation plan
- Estimated 23-37 days of work
- Systematic constraint-by-constraint translation approach
- Risk mitigation strategies
- Success criteria defined

### 2. Infrastructure (Phase 1) ✅

**Module Structure:**
```
src/energyscope/linopy_backend/
├── __init__.py           - Module exports
├── data_loader.py        - ModelData class, toy data creation
├── result_parser.py      - Linopy → Result conversion
└── toy_model.py          - Simplified test model
```

**Key Components:**
- `LinopyModel` class added to `models.py`
- `ModelData` class for managing input data
- `parse_linopy_result()` for result conversion
- `compare_results()` for AMPL/linopy validation

### 3. Toy Model (Phase 2) ✅

**Model Characteristics:**
- 5 technologies: PV, Wind, Gas Plant, Battery, Grid
- 3 layers: Electricity, Gas, End-use
- 24 time periods (1 day, hourly)
- Simple storage modeling

**Constraints Implemented:**
1. Capacity limits (F_t ≤ F * c_p_t)
2. Energy balance (supply ≥ demand per layer/period)
3. Storage balance (level tracking)
4. Storage capacity limits
5. Cyclic boundary conditions

**Objective:**
- Minimize: Investment + Maintenance + Operating costs
- Annualized investment using capital recovery factor

### 4. Testing & Examples

**Files Created:**
- `scripts/linopy_model.py` - Example usage script
- `tests/test_linopy_toy_model.py` - Comprehensive test suite
- `tests/README.md` - Testing documentation

**Test Coverage:**
- Data creation tests
- Model building tests
- Solving tests (optional, needs solver)
- Result parsing tests
- Energy balance validation tests

### 5. Dependencies

**Updated `pyproject.toml`:**
```toml
[project.optional-dependencies]
linopy = [
    "linopy>=0.3.0",
    "xarray>=2023.0.0",
]
```

**Installation:**
```bash
# With linopy support
pip install -e ".[linopy]"

# Add a solver (choose one)
pip install highspy      # Free, open-source
pip install gurobipy     # Commercial (free academic)
```

## Project Structure

```
energyscope/
├── src/energyscope/
│   ├── linopy_backend/          [NEW]
│   │   ├── __init__.py
│   │   ├── data_loader.py
│   │   ├── result_parser.py
│   │   └── toy_model.py
│   ├── models.py                [MODIFIED - added LinopyModel]
│   ├── energyscope.py           [TO MODIFY - add backend routing]
│   └── ...
├── scripts/
│   ├── ampl_model.py
│   ├── python_model.py
│   └── linopy_model.py          [NEW]
├── tests/                       [NEW]
│   ├── test_linopy_toy_model.py
│   └── README.md
├── docs/
│   ├── linopy_migration_strategy.md  [NEW]
│   └── linopy_quickstart.md          [NEW]
├── LINOPY_TODO.md               [NEW]
├── LINOPY_IMPLEMENTATION_SUMMARY.md  [NEW - this file]
└── pyproject.toml               [MODIFIED - added linopy dependency]
```

## How to Use (Right Now)

### 1. Install Dependencies

```bash
# Install energyscope with linopy support
pip install -e ".[linopy]"

# Install a solver
pip install highspy  # or gurobipy if you have a license
```

### 2. Run the Toy Model

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
Objective value: XXX.XX M€

=== Installed Capacity (F) ===
[Results displayed]

✓ Model solved successfully!
```

### 3. Run Tests

```bash
# Basic tests (no solver needed)
pytest tests/test_linopy_toy_model.py -v

# Full tests (needs solver)
pytest tests/test_linopy_toy_model.py --run-solver-tests -v
```

### 4. Programmatic Usage

```python
from energyscope.linopy_backend.data_loader import create_toy_data
from energyscope.linopy_backend.toy_model import solve_toy_model
from energyscope.linopy_backend.result_parser import parse_linopy_result

# Create data
data = create_toy_data()

# Solve
model, solution = solve_toy_model(data, solver='gurobi')

# Parse results
result = parse_linopy_result(model, data)

# Access results
print(f"Total cost: {model.objective.value}")
print(result.variables['F'])
```

## What's Next (Immediate Actions)

### Phase 2.5: Validation (CRITICAL - DO THIS FIRST)

1. **Create Equivalent AMPL Toy Model**
   - Export current toy model as AMPL .mod/.dat
   - Or create simplified AMPL version matching toy model
   
2. **Solve Both Models with Gurobi**
   - AMPL version → result_ampl
   - Linopy version → result_linopy
   
3. **Compare Results**
   ```python
   from energyscope.linopy_backend.result_parser import compare_results
   comparison = compare_results(result_ampl, result_linopy, rtol=1e-4)
   ```
   
4. **Fix Any Discrepancies**
   - Objective values should match within 0.1%
   - Variable values should match within 0.1%
   - Document any expected differences

### Phase 3: Start Core Model Translation

Once toy model is validated:

1. **Add Constraint Group 1 (Critical)**
   - Translate 4 core energy balance constraints
   - Test against AMPL
   - Verify results match
   
2. **Add Constraint Group 2 (High Priority)**
   - Resource constraints
   - Test and verify
   
3. **Continue systematically** through all 9 constraint groups

See `LINOPY_TODO.md` for detailed checklist.

## Integration Roadmap

Once core model is complete, update `Energyscope` class:

```python
# In energyscope.py
class Energyscope:
    def __init__(self, model: Model | LinopyModel, ...):
        self.backend = getattr(model, 'backend', 'ampl')
        # ...
    
    def calc(self, ...):
        if self.backend == 'ampl':
            return self._calc_ampl(...)
        elif self.backend == 'linopy':
            return self._calc_linopy(...)
    
    def _calc_linopy(self, ds=None, ...) -> Result:
        # Build and solve linopy model
        data = self.model.data_loader(ds)
        lp_model = self.model.builder(data)
        lp_model.solve(solver_name=self.solver_options['solver'])
        return parse_linopy_result(lp_model, data)
```

Then users can do:

```python
from energyscope.models import core, core_linopy

# AMPL version (existing)
es_ampl = Energyscope(model=core, solver_options={'solver': 'gurobi'})
result_ampl = es_ampl.calc()

# Linopy version (new)
es_linopy = Energyscope(model=core_linopy, solver_options={'solver': 'gurobi'})
result_linopy = es_linopy.calc()

# Results have identical structure!
```

## Key Design Decisions

### 1. Dual Backend Architecture
- **Rationale**: Preserve existing AMPL implementation, add linopy alongside
- **Benefit**: Users can choose backend, gradual migration possible
- **Trade-off**: Some code duplication, but worth it for flexibility

### 2. Toy Model First
- **Rationale**: Validate approach with simple model before tackling full complexity
- **Benefit**: Quick iteration, easier debugging, proof of concept
- **Trade-off**: Extra work, but essential for risk mitigation

### 3. Incremental Constraint Addition
- **Rationale**: Add constraints one group at a time, verify each
- **Benefit**: Easier to debug, can track down issues to specific constraints
- **Trade-off**: Slower than doing everything at once, but much safer

### 4. Result Format Compatibility
- **Rationale**: Linopy results → same `Result` class as AMPL
- **Benefit**: Existing plotting/analysis code works unchanged
- **Trade-off**: Some conversion overhead, but enables seamless switching

### 5. Data Format (TBD)
- **Current**: Manual Python data structures for toy model
- **Options**: 
  - Parse AMPL .dat files (maintains compatibility)
  - Native Python format (JSON/pickle/CSV)
  - Hybrid approach
- **Decision needed**: After Phase 2.5 validation

## Known Limitations & Future Work

### Current Limitations
- Only toy model implemented (not full core model)
- No integration with main `Energyscope` class yet
- Data must be created manually (no .dat parsing)
- Only tested conceptually (needs validation)

### Future Enhancements
- Full core model (37 constraints)
- Infrastructure module
- LCA module
- Transition/pathway module
- Performance optimization (vectorization, sparse matrices)
- Multi-scenario runs
- Uncertainty analysis

## Files Modified vs Created

### Modified
- `src/energyscope/models.py` - Added `LinopyModel` class and `core_toy_linopy`
- `pyproject.toml` - Added linopy dependencies

### Created
- `src/energyscope/linopy_backend/` (entire module)
- `scripts/linopy_model.py`
- `tests/` (entire directory)
- `docs/linopy_migration_strategy.md`
- `docs/linopy_quickstart.md`
- `LINOPY_TODO.md`
- `LINOPY_IMPLEMENTATION_SUMMARY.md`

### Unchanged (Your Existing Code)
- All AMPL model files (`.mod`, `.dat`)
- `src/energyscope/energyscope.py` (will be modified in Phase 6)
- `src/energyscope/result.py`
- All existing scripts and examples

## Success Metrics

### Phase 1-2 (Current)
- ✅ Infrastructure created
- ✅ Toy model implemented
- ✅ Tests written
- ✅ Documentation complete
- ⏳ Validation pending (Phase 2.5)

### Full Implementation (Future)
- All 37 AMPL constraints translated
- Objective matches AMPL (< 0.1% difference)
- Variables match AMPL (< 0.1% difference)
- All tests passing
- Documentation complete
- Example scripts working

## Questions & Answers

**Q: Can I use this now for real work?**  
A: Not yet. The toy model is for testing/validation. Wait for full core model (Phase 3).

**Q: Will this replace AMPL?**  
A: No, it's an alternative. Both backends will coexist. Use whichever fits your needs.

**Q: What if I don't want to install linopy?**  
A: No problem. Linopy is optional. Your existing AMPL workflow is unchanged.

**Q: How much faster/slower is linopy vs AMPL?**  
A: Unknown until we benchmark. Likely comparable for this model size. We'll measure in Phase 7.

**Q: Can I help?**  
A: Yes! See `LINOPY_TODO.md` for tasks. Start with Phase 2.5 validation or Phase 3 constraint translation.

## Conclusion

The foundation for linopy support is complete and ready for validation. The systematic approach should make the remaining work (Phase 3+) straightforward, if time-consuming.

**Next step**: Validate the toy model against AMPL (Phase 2.5), then begin incremental constraint translation (Phase 3).

For detailed guidance on any phase, refer to:
- Strategy: `docs/linopy_migration_strategy.md`
- Usage: `docs/linopy_quickstart.md`
- Tasks: `LINOPY_TODO.md`

Good luck with the implementation! 🚀

