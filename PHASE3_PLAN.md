# Phase 3 Implementation Plan - Core Model Translation

**Goal**: Translate all 37 AMPL constraints to linopy incrementally  
**Approach**: Group-by-group, test-driven, systematic  
**Timeline**: 15-25 days estimated

---

## Current Progress

**Phase 1-2**: ✅ Complete (Infrastructure + Toy model)  
**Phase 3**: 🚧 In Progress (Core model translation)

---

## Constraint Groups Overview

| Group | Priority | Constraints | Status | Complexity |
|-------|----------|-------------|--------|------------|
| 1. Energy Balance | Critical | 4 | 📋 TODO | High (conditional logic) |
| 2. Resources | High | 2 | 📋 TODO | Medium |
| 3. Storage | High | 7 | 📋 TODO | High (time dependencies) |
| 4. Costs | High | 4 | 📋 TODO | Medium |
| 5. GWP | Medium | 4 | 📋 TODO | Medium |
| 6. Mobility | Medium | 5 | 📋 TODO | Medium |
| 7. Heating | Medium | 3 | 📋 TODO | Medium |
| 8. Network | Low | 4 | 📋 TODO | Low |
| 9. Policy | Low | 4 | 📋 TODO | Low |
| **Total** | | **37** | **0/37** | |

---

## Group 1: Energy Balance (Critical)

### Constraints to Implement

#### 1.1 `end_uses_t` [Lines 166-187]
**AMPL**:
```ampl
subject to end_uses_t {l in LAYERS, h in HOURS, td in TYPICAL_DAYS}:
    End_uses [l, h, td] = (complex conditional expression)
```

**Purpose**: Calculate hourly end-use demand from annual data  
**Complexity**: HIGH - Many nested conditionals  
**Dependencies**: 
- `end_uses_input` (annual demand by type)
- Time series (electricity, heating, mobility)
- Share variables (heat_dhn, mobility, freight)

**Linopy Strategy**:
- Break into separate calculations per layer type
- Use Python conditionals instead of AMPL if-then-else
- Pre-compute demand arrays

#### 1.2 `capacity_factor_t` [Line 235-236]
**AMPL**:
```ampl
subject to capacity_factor_t {j in TECHNOLOGIES, h in HOURS, td in TYPICAL_DAYS}:
    F_t [j, h, td] <= F [j] * c_p_t [j, h, td];
```

**Purpose**: Limit hourly operation by installed capacity × capacity factor  
**Complexity**: LOW - Simple constraint  
**Dependencies**: F, F_t, c_p_t

**Linopy Strategy**:
- Direct translation: `F_t[j,h,td] <= F[j] * c_p_t[j,h,td]`
- Can use vectorized operations

#### 1.3 `capacity_factor` [Line 239-240]
**AMPL**:
```ampl
subject to capacity_factor {j in TECHNOLOGIES}:
    sum {t in PERIODS, h in HOUR_OF_PERIOD [t], td in TYPICAL_DAY_OF_PERIOD [t]} 
        (F_t [j, h, td] * t_op [h, td]) 
    <= F [j] * c_p [j] * total_time;
```

**Purpose**: Limit annual operation by yearly capacity factor  
**Complexity**: MEDIUM - Requires summation over periods  
**Dependencies**: F, F_t, t_op, c_p, total_time, T_H_TD mapping

**Linopy Strategy**:
- Sum F_t over all time periods
- Use T_H_TD set to map periods to (h, td)

#### 1.4 `layer_balance` [Line 259-264]
**AMPL**:
```ampl
subject to layer_balance {l in LAYERS, h in HOURS, td in TYPICAL_DAYS}:
    sum {i in RESOURCES union TECHNOLOGIES diff STORAGE_TECH} 
        (layers_in_out[i, l] * F_t [i, h, td]) 
    + sum {j in STORAGE_TECH} 
        (Storage_out [j, l, h, td] - Storage_in [j, l, h, td])
    - End_uses [l, h, td]
    = 0;
```

**Purpose**: Balance all layers (supply = demand + storage)  
**Complexity**: MEDIUM - Multiple sums, storage interaction  
**Dependencies**: layers_in_out, F_t, Storage_in/out, End_uses

**Linopy Strategy**:
- Production: sum over techs with layers_in_out > 0
- Consumption: sum over techs with layers_in_out < 0
- Storage: add/subtract storage flows
- Balance: production - consumption - demand = 0

---

## Implementation Strategy for Group 1

### Step 1: Data Preparation (Day 1-2)
**Priority**: IMMEDIATE  
**Task**: Create Python data structures for core model

Options:
- **Option A**: Parse existing AMPL .dat files using amplpy
- **Option B**: Create minimal test dataset manually
- **Option C**: Export from AMPL and convert

**Recommended**: Start with Option B (minimal dataset)

**Minimal Dataset Requirements**:
```python
{
    'sets': {
        'PERIODS': list(range(1, 289)),  # 12 TD × 24 hours
        'HOURS': list(range(1, 25)),
        'TYPICAL_DAYS': list(range(1, 13)),
        'T_H_TD': [...],  # Mapping
        'TECHNOLOGIES': [...],
        'STORAGE_TECH': [...],
        'RESOURCES': [...],
        'LAYERS': [...],
        'END_USES_TYPES': [...],
    },
    'parameters': {
        'f_max': {...},
        'f_min': {...},
        'c_p_t': pd.DataFrame(...),  # Tech × Hour × TD
        'c_p': {...},  # Annual capacity factor
        'layers_in_out': pd.DataFrame(...),
        't_op': pd.DataFrame(...),  # Operating hours
        'end_uses_input': {...},  # Annual demand
        'total_time': 8760,
        # Time series
        'electricity_time_series': pd.DataFrame(...),
        'heating_time_series': pd.DataFrame(...),
        'mob_pass_time_series': pd.DataFrame(...),
        'mob_freight_time_series': pd.DataFrame(...),
    },
    'variables': {
        # Share variables (these might be parameters or variables)
        'Share_heat_dhn': 0.3,  # Can be variable or fixed
        'Share_mobility_public': 0.3,
        'Share_freight_train': 0.2,
        'Share_freight_road': 0.7,
        'Share_freight_boat': 0.1,
    }
}
```

### Step 2: Implement Simple Constraints First (Day 2-3)
Start with easiest:
1. ✅ Implement `capacity_factor_t` (simplest)
2. ✅ Test with minimal data
3. ✅ Implement `layer_balance` (without end_uses calculation)
4. ✅ Test incrementally

### Step 3: Implement Complex Constraint (Day 3-5)
1. ✅ Break down `end_uses_t` into layer-specific functions
2. ✅ Implement each layer type separately
3. ✅ Test each layer
4. ✅ Integrate

### Step 4: Annual Constraint (Day 5-6)
1. ✅ Implement `capacity_factor` with period summation
2. ✅ Test

### Step 5: Full Group Test (Day 6-7)
1. ✅ Solve model with all Group 1 constraints
2. ✅ Verify feasibility
3. ✅ Compare with AMPL if possible
4. ✅ Document

---

## Testing Approach

### Test Levels

#### Unit Tests
Test each constraint independently:
```python
def test_capacity_factor_t():
    # Create minimal model with just this constraint
    # Verify constraint is correctly added
    # Check coefficient values
```

#### Integration Tests
Test constraint groups together:
```python
def test_group1_energy_balance():
    # Build model with all Group 1 constraints
    # Solve with simple data
    # Verify solution is feasible
```

#### Validation Tests
Compare with AMPL:
```python
def test_group1_vs_ampl():
    # Solve same problem with AMPL and linopy
    # Compare objective, variables
    # Assert < 0.1% difference
```

---

## Data Preparation Script

Create: `scripts/prepare_core_data.py`

```python
"""
Prepare core model data for linopy.

Two modes:
1. From AMPL (parse .dat files)
2. Manual (create minimal test dataset)
"""

def create_minimal_core_data():
    """Create minimal dataset for testing."""
    # Simple version: 3-5 technologies, 1-2 typical days
    pass

def load_from_ampl(dat_files):
    """Load from AMPL .dat files."""
    # Use amplpy to load and extract
    pass

def convert_ampl_to_python(ampl_model):
    """Convert AMPL model data to Python structures."""
    pass
```

---

## Next Immediate Actions (Today)

### Action 1: Create Minimal Test Data (30 min)
```bash
# Create: src/energyscope/linopy_backend/test_data.py
# With: create_minimal_core_data()
```

### Action 2: Implement capacity_factor_t (30 min)
- Update `core_model.py`
- Add constraint
- Test

### Action 3: Implement layer_balance (1 hour)
- Add to `core_model.py`
- Test

### Action 4: Test Group 1 Partial (30 min)
- Solve model
- Verify feasibility

**Total: ~2.5-3 hours for first working prototype**

---

## Success Criteria for Group 1

- [x] All 4 constraints implemented
- [ ] Model builds without errors
- [ ] Model solves (feasible or optimal)
- [ ] Constraints are active (duals non-zero where expected)
- [ ] Results make physical sense
- [ ] (Optional) Match AMPL results within 1%

---

## Risk Mitigation

### Risk: Conditional Logic Complex
**Mitigation**: Break `end_uses_t` into separate functions per layer

### Risk: Index Alignment Issues
**Mitigation**: Use xarray with explicit coordinates, test thoroughly

### Risk: Data Preparation Takes Too Long
**Mitigation**: Start with minimal synthetic data, expand incrementally

### Risk: Numerical Issues
**Mitigation**: Check scaling, use appropriate units, compare with AMPL

---

## Files to Create/Modify

### New Files
1. `src/energyscope/linopy_backend/test_data.py` - Test datasets
2. `scripts/prepare_core_data.py` - Data preparation
3. `scripts/test_core_group1.py` - Group 1 testing
4. `tests/test_core_constraints.py` - Unit tests

### Modified Files
1. `src/energyscope/linopy_backend/core_model.py` - Add constraints
2. `PHASE3_PLAN.md` - This file (track progress)
3. `LINOPY_TODO.md` - Update task status

---

## Timeline Estimate

| Task | Time | Cumulative |
|------|------|------------|
| Data preparation | 2-3 days | 3 days |
| Group 1 (4 constraints) | 5-7 days | 10 days |
| Group 2 (2 constraints) | 2-3 days | 13 days |
| Group 3 (7 constraints) | 4-6 days | 19 days |
| Group 4 (4 constraints) | 2-3 days | 22 days |
| Groups 5-9 (remaining) | 3-5 days | 27 days |
| **Total** | **20-27 days** | |

Plus testing and validation: +3-5 days  
**Total estimate: 23-32 days**

---

## Resources

- **AMPL Model**: `src/energyscope/data/models/core/td/ESTD_model_core.mod`
- **Strategy Doc**: `docs/linopy_migration_strategy.md`
- **Translation Guide**: `docs/ampl_vs_linopy_comparison.md`
- **TODO List**: `LINOPY_TODO.md`

---

**Status**: Ready to begin Group 1 implementation  
**Next**: Create minimal test data and implement first constraints  
**Updated**: October 17, 2025

