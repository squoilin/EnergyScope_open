# Continue From Here - Next Session Guide

**Current Status**: ✅ Phases 1-2 Complete | 🚧 Phase 3 Started  
**Last Updated**: October 17, 2025  
**Next Task**: Implement Group 1 constraints in core model

---

## ⚡ Quick Start (5 minutes)

### 1. Verify Environment
```bash
conda activate dispaset
cd /home/sylvain/svn/energyscope
python -c "import linopy; print('✓ Ready!')"
```

### 2. Test Current Implementation
```bash
# Test toy model (should work)
python scripts/linopy_model.py

# Expected output: "✓ Model solved successfully! Objective: 2548.52 M€"
```

### 3. View Test Data
```bash
# See core model test data
python src/energyscope/linopy_backend/test_data_core.py
```

**If all 3 work**: ✅ You're ready to continue!

---

## 📍 Where We Are

### Completed ✅
- **Infrastructure**: linopy_backend module fully functional
- **Toy model**: Works perfectly (2548.52 M€ objective)
- **Test data**: Minimal core dataset ready
- **Documentation**: ~150 pages complete

### Current Task 🚧
**Phase 3, Group 1: Energy Balance Constraints**

Need to implement 4 constraints:
1. `capacity_factor_t` - Hourly capacity limits
2. `layer_balance` - Layer balance equation
3. `capacity_factor` - Annual capacity limits
4. `end_uses_t` - End-use demand calculation

### Files to Modify
- `src/energyscope/linopy_backend/core_model.py` - Add constraints here
- `PHASE3_PLAN.md` - Track progress

---

## 🎯 Next Immediate Steps

### Step 1: Implement capacity_factor_t (Easiest First)

**File**: `src/energyscope/linopy_backend/core_model.py`  
**Function**: `build_core_model_partial()`  
**Location**: After variable definitions

**Add this code**:
```python
# Group 1.1: capacity_factor_t
# F_t[j,h,td] <= F[j] * c_p_t[j,h,td]
print("Adding capacity_factor_t constraints...")
for j in TECH_NOSTORAGE:
    for h in HOURS:
        for td in TYPICAL_DAYS:
            # Get capacity factor
            if (j, h, td) in c_p_t.index:
                cf = c_p_t.loc[(j, h, td)]
            else:
                cf = 1.0
            
            m.add_constraints(
                F_t.loc[j, h, td] <= F.loc[j] * cf,
                name=f"capacity_factor_t_{j}_{h}_{td}"
            )
```

### Step 2: Test It
```bash
# Create test script: scripts/test_group1.py
```

```python
from energyscope.linopy_backend.test_data_core import create_minimal_core_data
from energyscope.linopy_backend.core_model import build_core_model_partial

data = create_minimal_core_data()
model = build_core_model_partial(data, constraint_groups=['energy_balance'])

# Check if model builds
print(f"✓ Model created with {len(model.constraints)} constraints")

# Try to solve (might be infeasible without all constraints)
model.solve(solver_name='highs')
print(f"✓ Model solve attempted")
```

### Step 3: Implement layer_balance

**Add this code** (in same file, after capacity_factor_t):
```python
# Group 1.2: layer_balance
# sum(tech production) + storage_out - storage_in = End_uses
print("Adding layer_balance constraints...")
for l in LAYERS:
    for h in HOURS:
        for td in TYPICAL_DAYS:
            # Production from technologies
            prod_terms = []
            for j in TECH_NOSTORAGE:
                if (j, l) in layers_in_out.index:
                    coef = layers_in_out.loc[(j, l), 'value']  # Adjust based on your data structure
                    if coef != 0:
                        prod_terms.append(F_t.loc[j, h, td] * coef)
            
            # Storage (if applicable)
            if STORAGE_TECH:
                for s in STORAGE_TECH:
                    prod_terms.append(Storage_out.loc[s, l, h, td])
                    prod_terms.append(-Storage_in.loc[s, l, h, td])
            
            # Demand
            if (l, h, td) in End_uses.index:
                demand = End_uses.loc[(l, h, td)]
            else:
                demand = 0
            
            # Balance
            if prod_terms:
                m.add_constraints(
                    sum(prod_terms) >= demand,
                    name=f"layer_balance_{l}_{h}_{td}"
                )
```

### Step 4: Continue with capacity_factor and end_uses_t

Follow the same pattern. See `PHASE3_PLAN.md` for details.

---

## 📚 Key Documents

### Quick Reference
| What | Where |
|------|-------|
| Current status | `LINOPY_STATUS.md` |
| Test results | `TESTING_RESULTS.md` |
| Phase 3 plan | `PHASE3_PLAN.md` |
| Session summary | `SESSION_SUMMARY.md` |

### Implementation Guides
| What | Where |
|------|-------|
| Full strategy | `docs/linopy_migration_strategy.md` |
| AMPL→linopy patterns | `docs/ampl_vs_linopy_comparison.md` |
| Quick start | `docs/linopy_quickstart.md` |

### Code
| What | Where |
|------|-------|
| Core model structure | `src/energyscope/linopy_backend/core_model.py` |
| Test data | `src/energyscope/linopy_backend/test_data_core.py` |
| Toy model (reference) | `src/energyscope/linopy_backend/toy_model.py` |

---

## 🔧 Useful Commands

### Test Toy Model
```bash
python scripts/linopy_model.py
```

### View Test Data
```bash
python src/energyscope/linopy_backend/test_data_core.py
```

### Run Comparison Test
```bash
python scripts/test_toy_model_comparison.py
```

### Check AMPL Model (for reference)
```bash
less src/energyscope/data/models/core/td/ESTD_model_core.mod
# Look at lines 235-240 for capacity_factor_t
# Look at lines 259-264 for layer_balance
```

---

## 💡 Tips

### Translation Strategy
1. **Look at AMPL** - Understand the constraint
2. **Break it down** - Simplify the logic
3. **Translate incrementally** - One piece at a time
4. **Test immediately** - Don't wait to test
5. **Compare** - Check against AMPL if possible

### Debugging
```python
# Print constraint count
print(f"Constraints: {len(model.constraints)}")

# Print variable count
print(f"Variables: {len(model.variables)}")

# Check if constraint was added
print(f"Has capacity_factor_t: {'capacity_factor_t' in str(model.constraints)}")
```

### Common Issues
- **Index mismatch**: Make sure indices match between DataFrame and variables
- **Missing data**: Check if parameter exists before using
- **Coordinate alignment**: Use `.loc[]` for explicit indexing

---

## 📈 Progress Tracking

Update `LINOPY_TODO.md` as you go:
```markdown
- [x] Phase 3.1: Minimal test data
- [ ] Phase 3.2: Group 1 constraint 1/4 (capacity_factor_t)
- [ ] Phase 3.2: Group 1 constraint 2/4 (layer_balance)
- [ ] Phase 3.2: Group 1 constraint 3/4 (capacity_factor)
- [ ] Phase 3.2: Group 1 constraint 4/4 (end_uses_t)
```

---

## 🎯 Goals for Next Session

### Minimum (1-2 hours)
- ✅ Implement `capacity_factor_t`
- ✅ Test that constraint is added correctly

### Target (2-3 hours)
- ✅ Implement `capacity_factor_t`
- ✅ Implement `layer_balance`
- ✅ Test both constraints
- ✅ Model solves (feasible or optimal)

### Stretch (4-6 hours)
- ✅ Complete all Group 1 (4 constraints)
- ✅ Full testing
- ✅ Compare with AMPL (if possible)
- ✅ Start Group 2

---

## ⚠️ Important Notes

### Don't Break Toy Model
- Toy model works perfectly - don't modify it
- Core model is separate (`core_model.py` vs `toy_model.py`)
- If something breaks, revert and try again

### Test Incrementally
- Add one constraint at a time
- Test after each addition
- Don't add all 4 constraints at once

### Use the Data
- Test data is in `test_data_core.py`
- It's already validated and working
- Use `create_minimal_core_data()` to get it

### Reference AMPL
- Original model: `src/energyscope/data/models/core/td/ESTD_model_core.mod`
- Lines 235-236: capacity_factor_t
- Lines 259-264: layer_balance
- Lines 239-240: capacity_factor

---

## 🚦 Health Checks

Before starting, verify:
```bash
# 1. Environment works
conda activate dispaset
python -c "import linopy; print('✓')"

# 2. Toy model works
python scripts/linopy_model.py | grep "solved successfully"

# 3. Test data works
python src/energyscope/linopy_backend/test_data_core.py | grep "created successfully"
```

All should print ✓ or success message.

---

## 📞 When You Get Stuck

### Check These First
1. `PHASE3_PLAN.md` - Detailed implementation guide
2. `docs/ampl_vs_linopy_comparison.md` - Translation patterns
3. `src/energyscope/linopy_backend/toy_model.py` - Working example

### Common Problems

**Problem**: Constraint not added  
**Solution**: Check if condition is being met, print debug info

**Problem**: Index error  
**Solution**: Verify indices match, use `.loc[]` not `[]`

**Problem**: Model infeasible  
**Solution**: Check constraint bounds, start with loose bounds

**Problem**: Solver error  
**Solution**: Try `solver='highs'` instead of gurobi

---

## 🎯 Success Criteria

### You'll know it's working when:
1. ✅ Model builds without errors
2. ✅ Constraints are added (count > 0)
3. ✅ Model solves (status = 'ok' or 'optimal')
4. ✅ Solution values are reasonable

### You'll know to move on when:
1. ✅ All 4 Group 1 constraints implemented
2. ✅ Tests pass
3. ✅ Model solves optimally
4. ✅ Results make physical sense

---

## 📋 Checklist for Next Session

- [ ] Activate dispaset environment
- [ ] Verify toy model still works
- [ ] Open `core_model.py` in editor
- [ ] Read `PHASE3_PLAN.md` Group 1 section
- [ ] Implement `capacity_factor_t`
- [ ] Test it
- [ ] Implement `layer_balance`
- [ ] Test it
- [ ] Continue with remaining constraints
- [ ] Update `LINOPY_TODO.md`
- [ ] Document any issues

---

## 🎉 You've Got This!

The hard parts are done:
- ✅ Infrastructure works
- ✅ Toy model proves the concept
- ✅ Test data is ready
- ✅ Documentation is complete

Now it's just systematic translation:
1. Read AMPL constraint
2. Translate to Python/linopy
3. Test
4. Repeat

**Estimated time for Group 1**: 5-7 hours  
**Estimated time for full Phase 3**: 20-30 days

---

**Ready to start?** Open `src/energyscope/linopy_backend/core_model.py` and begin! 🚀

**Questions?** Check `PHASE3_PLAN.md` for detailed guidance.

**Last updated**: October 17, 2025  
**Status**: ✅ Ready to continue!

