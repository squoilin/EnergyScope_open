# PyOptInterface Full Model - Status and Findings

## Summary

Through systematic debugging, we have successfully identified and partially resolved the issues preventing the PyOptInterface full model from solving with the complete ESTD dataset.

## Key Findings

### ✅ Working: Model WITHOUT Storage
- **Status**: FEASIBLE and SOLVES
- **Objective Value**: 10,747.94 M€
- **Constraints Implemented**:
  - End-uses calculation (with Share variables)
  - Network losses
  - Layer balance (without storage)
  - Hourly capacity factors
  - Operating strategies for mobility (passenger & freight)
  - Resource availability
  - Extra grid, DHN, efficiency constraints
  - Solar area limits
  - Cost and GWP calculations

### ❌ Not Working: Model WITH Storage
- **Status**: INFEASIBLE
- **Issue**: Storage constraints cause infeasibility
- **Root Cause**: Still under investigation, but likely related to:
  - Storage level dynamics formulation
  - Interaction between storage and layer balance
  - Possible missing constraints (daily storage, energy-to-power ratio, etc.)

## Improvements Made

### 1. Data Loader (`data_loader_full.py`)
- **Fixed**: Extraction of indexed sets
- Added proper extraction for `TECHNOLOGIES_OF_END_USES_TYPE` and `TECHNOLOGIES_OF_END_USES_CATEGORY`
- These are now correctly returned as dictionaries mapping end-use types/categories to lists of technologies

### 2. Model Structure (`pyoptinterface_full_model.py`)
- **Fixed**: End_uses are now VARIABLES (not fixed parameters)
- **Added**: Share variables for modal split and DHN penetration
- **Added**: Shares_mobility_passenger and Shares_mobility_freight variables
- **Added**: Operating strategy constraints for mobility
- **Added**: Network losses as variables with proper constraints
- **Added**: Infrastructure constraints (extra_grid, extra_dhn, extra_efficiency)
- **Added**: Solar area limitation constraint
- **Fixed**: Indentation bug in storage level constraints (line 331-333)

### 3. Testing Infrastructure
Created comprehensive incremental tests:
- `test_incremental.py` - Basic constraint groups
- `test_incremental2.py` - Extended constraints including mobility
- `test_incremental3.py` - Infrastructure and resource constraints
- `test_cost_constraints.py` - Full model without storage
- `pyoptinterface_nostorage.py` - Clean no-storage version

## Comparison with AMPL Model

### Implemented Constraints (matching AMPL)
✅ End-uses calculation [Eq. 2.8 / Figure 2.8]  
✅ Layer balance [Eq. 2.13]  
✅ Hourly capacity factor [Eq. 2.10]  
✅ Resource availability [Eq. 2.12]  
✅ Freight shares [Eq. 2.26]  
✅ Network losses [Eq. 2.20]  
✅ Operating strategy passenger mobility [Eq. 2.24]  
✅ Operating strategy freight mobility [Eq. 2.25]  
✅ Extra grid [Eq. 2.21]  
✅ Extra DHN [Eq. 2.22]  
✅ Extra efficiency [Eq. 2.37]  
✅ Solar area limited [Eq. 2.39]  
✅ Cost calculation [Eq. 2.1-2.5]  
✅ GWP calculation [Eq. 2.6-2.8]  

### Partially Implemented
⚠️ Storage level [Eq. 2.14] - Implemented but causing infeasibility  
⚠️ Storage level capacity [Eq. 2.16] - Implemented but needs verification

### Not Yet Implemented
❌ Yearly capacity factor [Eq. 2.11]  
❌ Daily storage [Eq. 2.15]  
❌ Storage layer compatibility [Eq. 2.17-2.18]  
❌ Energy-to-power ratio [Eq. 2.19]  
❌ EV storage [Eq. 2.19-bis, 2.30-2.31]  
❌ Thermal solar [Eq. 2.27-2.29]  
❌ fmax/fmin percentage [Eq. 2.36]  
❌ Constant resource import [Eq. 2.12-bis]

## Next Steps

### Immediate Priority: Fix Storage Constraints

1. **Debug Storage Level Constraint**
   - Compare storage formulation line-by-line with AMPL
   - Verify T_H_TD mapping is used correctly
   - Check storage_eff_in/out application
   - Test with a single storage technology first

2. **Add Missing Storage Constraints**
   - Implement daily storage constraint [Eq. 2.15]
   - Implement storage layer compatibility [Eq. 2.17-2.18]
   - Implement energy-to-power ratio [Eq. 2.19]

3. **Incremental Testing**
   - Start with the working no-storage model
   - Add ONE storage technology at a time
   - Add storage constraints one at a time
   - Identify exactly which constraint causes infeasibility

### Secondary Priority: Complete Remaining Constraints

4. **Yearly Capacity Factor** [Eq. 2.11]
   - Limits total annual output based on `c_p` parameter

5. **Thermal Solar and Decentralized Heating** [Eq. 2.27-2.29]
   - Required for systems with thermal solar storage

6. **EV Storage** [Eq. 2.30-2.31]
   - Special handling for electric vehicle batteries

7. **Advanced Constraints**
   - fmax/fmin percentage constraints
   - Constant resource import

### Final Steps: Validation

8. **Compare Results with AMPL**
   - Run both models with identical data
   - Compare objective values
   - Compare key decision variables
   - Verify capacity allocations match

9. **Performance Optimization**
   - Once functional, optimize solve time
   - Consider using Gurobi-specific features
   - Benchmark against AMPL version

## Technical Notes

### Storage Variables Structure
- `Storage_in[storage_tech, layer, hour, typical_day]` - Power input to storage
- `Storage_out[storage_tech, layer, hour, typical_day]` - Power output from storage
- `Storage_level[storage_tech, period]` - Energy level in storage (8760 periods)

### Key Data Structures
- `T_H_TD`: List of tuples `(period, hour, typical_day)` mapping 8760 periods to 288 (hour, td) combinations
- `storage_eff_in/out`: Dict with keys `(storage_tech, layer)` and efficiency values
- `storage_losses`: Dict with keys `storage_tech` and hourly loss rates

### Solver Information
- **Solver**: Gurobi 12.0.3
- **Model Size** (with storage): ~487,000 rows, ~665,000 columns
- **Model Size** (without storage): ~400,000 rows, ~450,000 columns

## Files Modified

1. `src/energyscope/linopy_backend/data_loader_full.py` - Fixed indexed set extraction
2. `scripts/pyoptinterface_full_model.py` - Major overhaul with proper structure
3. Created multiple test scripts for incremental debugging

## References

- AMPL Model: `src/energyscope/data/models/core/td/ESTD_model_core.mod`
- AMPL Data: `src/energyscope/data/datasets/core/td/ESTD_*.dat`
- Baseline AMPL Objective: 47,572.11 M€
- PyOptInterface (no storage): 10,747.94 M€ (different because storage excluded)

---
*Last Updated: [Current Date]*
*Status: Storage debugging in progress*

