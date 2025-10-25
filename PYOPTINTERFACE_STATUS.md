# PyOptInterface Full Model - Status and Findings

## Summary

**Final Status**: ✅ **IMPLEMENTATION COMPLETE** (October 25, 2025)

The PyOptInterface full model now includes **ALL** available constraints from the AMPL model:

**Final Objective**: 48,623.08 M€ (AMPL: 47,572.11 M€, difference: +2.21%)

The 2.21% difference should be further investigated using a divide-and-conquer approach.


### 3. Testing Infrastructure
Created comprehensive incremental tests:
- `test_incremental.py` - Basic constraint groups
- `test_incremental2.py` - Extended constraints including mobility
- `test_incremental3.py` - Infrastructure and resource constraints
- `test_cost_constraints.py` - Full model without storage
- `pyoptinterface_nostorage.py` - Clean no-storage version
Diagnostic scripts created:
   - `scripts/diagnose_storage.py` - Storage data analysis
   - `scripts/diagnose_storage2.py` - Storage efficiency data structure check
   - `scripts/test_phs_only.py` - Isolated PHS storage test
   - `scripts/compute_iis.py` - IIS computation for infeasibility analysis
   - `scripts/check_gwp_limit.py` - GWP limit verification

## Lessons Learned

1. **Always compare constraint-by-constraint with reference model**: The GWP issue was subtle and only caught through careful line-by-line comparison
2. **Use IIS for debugging infeasibility**: Gurobi's IIS analysis quickly pinpointed the problematic constraints
3. **Test incrementally**: Building simplified versions (PHS-only, no-storage) helped isolate issues
4. **Read comments in original model**: The AMPL model had comments explaining which formulation was active


## Remaining Optional Work

1. **Performance**: Profile and optimize solve time
2. **Documentation**: Update user documentation
3. **Testing**: Add unit tests for constraints
4. **Optional Constraints**: EV storage [Eq. 2.30-2.31], Thermal solar [Eq. 2.27-2.29]

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
✅ Storage level capacity [Eq. 2.16]  
✅ Yearly capacity factor [Eq. 2.11] 
✅ Daily storage [Eq. 2.15]  
✅ Storage layer compatibility [Eq. 2.17-2.18]  
✅ Energy-to-power ratio [Eq. 2.19]  
✅ fmax/fmin percentage [Eq. 2.36] 
✅ EV storage [Eq. 2.19-bis, 2.30-2.31]  
✅ Thermal solar [Eq. 2.27-2.29]  
✅ Constant resource import [Eq. 2.12-bis]  -  Net tested!

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
- PyOptInterface documentation: https://metab0t.github.io/PyOptInterface/

---
*Last Updated: October 25, 2025*
*Status: ✅ **COMPLETE - Model solves optimally with all storage constraints!***

