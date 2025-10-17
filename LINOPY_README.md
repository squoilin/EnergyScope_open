# EnergyScope Linopy Backend

This directory and documentation set describes the linopy backend implementation for EnergyScope - an alternative to the AMPL backend that provides a pure Python, open-source optimization workflow.

## 📚 Documentation Index

### Start Here
1. **[Implementation Summary](LINOPY_IMPLEMENTATION_SUMMARY.md)** ⭐ START HERE
   - Overview of what was done
   - Current status
   - How to use it now
   - Next steps

2. **[Quick Start Guide](docs/linopy_quickstart.md)**
   - Installation instructions
   - Running your first linopy model
   - Basic usage examples
   - Troubleshooting

### Planning & Strategy
3. **[Migration Strategy](docs/linopy_migration_strategy.md)**
   - Complete 10-phase implementation plan
   - Constraint-by-constraint translation approach
   - Risk mitigation strategies
   - Timeline estimates

4. **[TODO List](LINOPY_TODO.md)**
   - Working checklist with all tasks
   - Current progress tracking
   - Next immediate actions

### Reference
5. **[AMPL vs Linopy Comparison](docs/ampl_vs_linopy_comparison.md)**
   - Side-by-side syntax comparison
   - Translation patterns
   - When to use which
   - Common pitfalls

## 🚀 Quick Start

### Installation

```bash
# Install with linopy support
pip install -e ".[linopy]"

# Add a solver
pip install highspy  # Free, open-source
# or
pip install gurobipy  # Commercial (free for academics)
```

### Run the Toy Model

```bash
python scripts/linopy_model.py
```

### Use in Code

```python
from energyscope.linopy_backend.data_loader import create_toy_data
from energyscope.linopy_backend.toy_model import solve_toy_model
from energyscope.linopy_backend.result_parser import parse_linopy_result

# Create data
data = create_toy_data()

# Solve
model, solution = solve_toy_model(data, solver='gurobi')

# Get results
result = parse_linopy_result(model, data)
print(f"Total cost: {model.objective.value}")
```

## 📁 File Structure

```
energyscope/
├── src/energyscope/linopy_backend/    # Linopy implementation
│   ├── __init__.py                    # Module exports
│   ├── data_loader.py                 # Data management (ModelData class)
│   ├── result_parser.py               # Result conversion
│   └── toy_model.py                   # Toy model implementation
│
├── scripts/
│   ├── ampl_model.py                  # AMPL example (existing)
│   └── linopy_model.py                # Linopy example (new)
│
├── tests/
│   ├── test_linopy_toy_model.py       # Linopy tests
│   └── README.md                      # Testing guide
│
├── docs/
│   ├── linopy_migration_strategy.md   # Complete strategy (37 pages)
│   ├── linopy_quickstart.md           # User guide
│   └── ampl_vs_linopy_comparison.md   # Comparison guide
│
├── LINOPY_README.md                   # This file
├── LINOPY_IMPLEMENTATION_SUMMARY.md   # Executive summary
└── LINOPY_TODO.md                     # Task checklist
```

## ✅ Current Status

### Completed (Phase 1-2)
- ✅ Infrastructure setup (linopy_backend module)
- ✅ LinopyModel class in models.py
- ✅ Data management (ModelData class)
- ✅ Result parser (linopy → Result conversion)
- ✅ Toy model implementation (5 technologies, 24 hours)
- ✅ Example script
- ✅ Test suite
- ✅ Comprehensive documentation (5 documents)

### In Progress (Phase 2.5)
- ⏳ Validate toy model against AMPL
- ⏳ Ensure results match (< 0.1% difference)

### Next Up (Phase 3)
- 📋 Translate full core model (37 constraints)
- 📋 Group 1: Core energy balance (4 constraints)
- 📋 Group 2: Resources (2 constraints)
- 📋 Groups 3-9: Remaining constraints

## 🎯 What's Working Now

### ✅ You Can Do This Today:

1. **Run the toy model**
   ```bash
   python scripts/linopy_model.py
   ```

2. **Run tests**
   ```bash
   pytest tests/test_linopy_toy_model.py -v
   ```

3. **Use linopy programmatically**
   ```python
   from energyscope.linopy_backend import build_toy_model
   from energyscope.linopy_backend.data_loader import create_toy_data
   
   data = create_toy_data()
   model = build_toy_model(data)
   model.solve(solver_name='gurobi')
   ```

4. **Compare results** (once both AMPL and linopy are run)
   ```python
   from energyscope.linopy_backend.result_parser import compare_results
   comparison = compare_results(result_ampl, result_linopy)
   ```

### ⏳ Not Yet Available:

- Full core model (only toy model works)
- Integration with main Energyscope class
- Infrastructure/LCA/transition modules
- AMPL .dat file parsing
- Production-ready workflows

## 🛠️ Development Workflow

### For Adding New Constraints

1. **Study the AMPL constraint**
   ```ampl
   # In ESTD_model_core.mod
   subject to energy_balance {l in LAYERS, t in PERIODS}:
       sum {j in TECH} (F_t[j,t] * layers_out[j,l]) >= demand[l,t];
   ```

2. **Translate to linopy**
   ```python
   for l in LAYERS:
       for t in PERIODS:
           production = sum(F_t.loc[j,t] * layers_out.loc[j,l] for j in TECH)
           m.add_constraints(production >= demand.loc[l,t], 
                           name=f"energy_balance_{l}_{t}")
   ```

3. **Test it**
   ```python
   # Solve both AMPL and linopy
   # Compare results
   assert_close(result_ampl, result_linopy)
   ```

4. **Document it**
   - Add to constraint group in TODO
   - Note any translation challenges
   - Update documentation

### Testing Strategy

```bash
# Basic tests (no solver)
pytest tests/test_linopy_toy_model.py

# Full tests (with solver)
pytest tests/test_linopy_toy_model.py --run-solver-tests

# Specific test
pytest tests/test_linopy_toy_model.py::TestToyModel::test_model_solving -v
```

## 📖 Translation Patterns

### Pattern 1: Simple Constraint
```ampl
# AMPL
F[j] <= f_max[j]
```
```python
# Linopy
m.add_constraints(F.loc[j] <= f_max[j], name=f"limit_{j}")
```

### Pattern 2: Summation
```ampl
# AMPL
sum {j in TECH} (F[j] * coef[j]) >= target
```
```python
# Linopy
production = sum(F.loc[j] * coef[j] for j in TECH)
m.add_constraints(production >= target, name="sum_constraint")
```

### Pattern 3: Time-Dependent
```ampl
# AMPL (t > 1)
Storage[t] = Storage[t-1] + In[t] - Out[t]
```
```python
# Linopy
for i, t in enumerate(PERIODS):
    if i > 0:
        prev_t = PERIODS[i-1]
        m.add_constraints(
            Storage.loc[t] == Storage.loc[prev_t] + In.loc[t] - Out.loc[t]
        )
```

More patterns in [AMPL vs Linopy Comparison](docs/ampl_vs_linopy_comparison.md).

## 🎓 Learning Resources

### Linopy Documentation
- [Official Docs](https://linopy.readthedocs.io/)
- [API Reference](https://linopy.readthedocs.io/en/latest/api.html)
- [Examples](https://linopy.readthedocs.io/en/latest/examples.html)

### EnergyScope Linopy Docs
- [Quick Start](docs/linopy_quickstart.md) - Get started quickly
- [Migration Strategy](docs/linopy_migration_strategy.md) - Full plan
- [Comparison Guide](docs/ampl_vs_linopy_comparison.md) - AMPL vs Linopy

### Examples
- `scripts/linopy_model.py` - Basic usage
- `tests/test_linopy_toy_model.py` - Test examples
- `src/energyscope/linopy_backend/toy_model.py` - Model building

## 🐛 Troubleshooting

### "No module named 'linopy'"
```bash
pip install -e ".[linopy]"
```

### "Solver not available"
```bash
# Install a solver
pip install highspy  # Free
# or
pip install gurobipy  # Commercial
```

### "Results don't match AMPL"
1. Check which constraints are implemented
2. Verify solver settings are identical
3. Use `compare_results()` to identify differences
4. Check for numerical precision issues

### "Model is infeasible"
1. Check constraint definitions
2. Verify data is valid
3. Add slack variables for debugging
4. Check bounds on variables

## 🤝 Contributing

### Areas Needing Help

1. **Phase 2.5**: Validate toy model vs AMPL
2. **Phase 3**: Translate core model constraints
   - Group 1: Energy balance (critical)
   - Group 2: Resources (high priority)
   - Groups 3-9: See TODO list
3. **Phase 4**: Data management (decide on format)
4. **Phase 7**: Testing and validation

### How to Contribute

1. Pick a task from [LINOPY_TODO.md](LINOPY_TODO.md)
2. Read relevant documentation
3. Implement and test
4. Update documentation
5. Submit for review

### Coding Standards

- Follow existing code style
- Add docstrings to all functions
- Write tests for new functionality
- Update TODO list as you go
- Document translation challenges

## 📊 Progress Tracking

| Phase | Status | Completion |
|-------|--------|------------|
| 1. Infrastructure | ✅ Complete | 100% |
| 2. Toy Model | ✅ Complete | 100% |
| 2.5. Validation | ⏳ In Progress | 0% |
| 3. Core Model | 📋 Planned | 0/37 constraints |
| 4. Data Management | 📋 Planned | 0% |
| 5. Result Parser | ✅ Complete | 100% |
| 6. Integration | 📋 Planned | 0% |
| 7. Testing | ⏳ Partial | 30% |
| 8. Documentation | ✅ Complete | 100% |
| 9. Advanced Features | 📋 Future | 0% |
| 10. Optimization | 📋 Future | 0% |

**Overall Progress**: 25% (Phases 1-2 complete)

## 🎯 Success Criteria

### Phase 2 (Toy Model) ✅
- [x] Model builds without errors
- [x] Model solves successfully
- [x] Results are parseable
- [x] Tests pass
- [ ] Results match AMPL (pending Phase 2.5)

### Phase 3 (Core Model) 📋
- [ ] All 37 constraints translated
- [ ] All tests passing
- [ ] Results match AMPL (< 0.1% difference)
- [ ] Documentation complete

### Final (Full Implementation) 📋
- [ ] Core model complete
- [ ] Infrastructure module
- [ ] Integration with Energyscope class
- [ ] All tests passing
- [ ] Performance acceptable (< 2x AMPL solve time)
- [ ] Production-ready

## 📝 Citation

If you use the linopy backend in research, please cite:

```bibtex
@software{energyscope_linopy,
  title = {EnergyScope Linopy Backend},
  author = {[Your Name]},
  year = {2025},
  url = {https://library.energyscope.ch}
}
```

(Update with actual citation information when published)

## 📧 Support

- **Issues**: GitLab issue tracker
- **Questions**: See documentation first
- **Contributions**: See contributing section above

## 📜 License

Same as EnergyScope main project (Apache License 2.0)

---

## Quick Navigation

- 🚀 **Getting Started**: [Quick Start Guide](docs/linopy_quickstart.md)
- 📋 **What to Do**: [TODO List](LINOPY_TODO.md)
- 📊 **Current Status**: [Implementation Summary](LINOPY_IMPLEMENTATION_SUMMARY.md)
- 🗺️ **Full Plan**: [Migration Strategy](docs/linopy_migration_strategy.md)
- 🔄 **AMPL vs Linopy**: [Comparison Guide](docs/ampl_vs_linopy_comparison.md)

**Ready to start?** Begin with the [Implementation Summary](LINOPY_IMPLEMENTATION_SUMMARY.md) to understand what's been done, then jump to the [Quick Start Guide](docs/linopy_quickstart.md) to try it out!

