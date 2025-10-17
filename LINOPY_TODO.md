# Linopy Implementation TODO

This is a working checklist for implementing the linopy backend.

## Phase 1: Infrastructure Setup ✅ COMPLETE

- [x] Create `src/energyscope/linopy_backend/` module
- [x] Create `LinopyModel` class in `models.py`
- [x] Create `data_loader.py` with `ModelData` class
- [x] Create `result_parser.py` with `parse_linopy_result()`
- [x] Update `pyproject.toml` with linopy dependencies
- [x] Create example script `scripts/linopy_model.py`
- [x] Create test file `tests/test_linopy_toy_model.py`
- [x] Write documentation (quickstart, strategy)

## Phase 2: Toy Model ✅ COMPLETE

- [x] Create simplified toy data (`create_toy_data()`)
- [x] Implement basic model builder (`build_toy_model()`)
- [x] Add decision variables (F, F_t, Storage)
- [x] Add basic constraints:
  - [x] Capacity limits
  - [x] Energy balance
  - [x] Storage balance
  - [x] Operation limits
- [x] Add objective function (cost minimization)
- [x] Write tests
- [x] Create example script

## Phase 2.5: Validation ⏳ NEXT

- [ ] Create equivalent AMPL toy model
- [ ] Solve both with Gurobi
- [ ] Compare objective values (should match within 0.1%)
- [ ] Compare variable values
- [ ] Document any differences
- [ ] Fix discrepancies

## Phase 3: Incremental Core Model Translation

### Group 1: Core Energy Balance (Priority: Critical)
- [ ] Study AMPL constraints in detail
- [ ] `end_uses_t` - Layer balance at each time period
- [ ] `layer_balance` - Complete layer balance with technologies
- [ ] `capacity_factor_t` - Time-varying capacity factors
- [ ] `capacity_factor` - Annual capacity factor constraint
- [ ] Test group 1 against AMPL
- [ ] Document translation

### Group 2: Resources (Priority: High)
- [ ] `resource_availability` - Annual resource limits
- [ ] `resource_constant_import` - Constant import resources
- [ ] Test group 2 against AMPL
- [ ] Document translation

### Group 3: Storage (Priority: High)
- [ ] `storage_level` - Storage state equation
- [ ] `storage_layer_in` - Storage charging
- [ ] `storage_layer_out` - Storage discharging
- [ ] `limit_energy_stored_to_maximum` - Storage capacity limit
- [ ] `impose_daily_storage` - Daily cycling constraint
- [ ] `limit_energy_to_power_ratio` - E/P ratio constraint
- [ ] `limit_energy_to_power_ratio_bis` - E/P for V2G
- [ ] Test group 3 against AMPL
- [ ] Document translation

### Group 4: Costs (Priority: High)
- [ ] `totalcost_cal` - Total cost calculation
- [ ] `investment_cost_calc` - Investment costs
- [ ] `main_cost_calc` - Maintenance costs
- [ ] `op_cost_calc` - Operating costs
- [ ] Test group 4 against AMPL
- [ ] Document translation

### Group 5: GWP Constraints (Priority: Medium)
- [ ] `totalGWP_calc` - Total GWP calculation
- [ ] `gwp_constr_calc` - Construction GWP
- [ ] `gwp_op_calc` - Operational GWP
- [ ] `Minimum_GWP_reduction` - GWP limit constraint
- [ ] Test group 5 against AMPL
- [ ] Document translation

### Group 6: Mobility (Priority: Medium)
- [ ] `operating_strategy_mob_passenger` - Passenger mobility
- [ ] `operating_strategy_mobility_freight` - Freight mobility
- [ ] `Freight_shares` - Freight mode shares
- [ ] `EV_storage_size` - EV battery sizing
- [ ] `EV_storage_for_V2G_demand` - V2G constraint
- [ ] Test group 6 against AMPL
- [ ] Document translation

### Group 7: Heating (Priority: Medium)
- [ ] `thermal_solar_capacity_factor` - Solar thermal CF
- [ ] `thermal_solar_total_capacity` - Solar thermal sizing
- [ ] `decentralised_heating_balance` - Decentralized heat balance
- [ ] Test group 7 against AMPL
- [ ] Document translation

### Group 8: Network & Infrastructure (Priority: Low)
- [ ] `network_losses` - Network loss constraints
- [ ] `extra_grid` - Grid constraints
- [ ] `extra_dhn` - DHN constraints
- [ ] `extra_efficiency` - Efficiency constraints
- [ ] Test group 8 against AMPL
- [ ] Document translation

### Group 9: Policy Constraints (Priority: Low)
- [ ] `f_max_perc` - Max technology share
- [ ] `f_min_perc` - Min technology share
- [ ] `solar_area_limited` - Solar area constraint
- [ ] Test group 9 against AMPL
- [ ] Document translation

## Phase 4: Data Management

- [ ] Decide on data format (AMPL .dat parsing vs native Python)
- [ ] Implement AMPL .dat parser (if chosen)
- [ ] Or create converter from .dat to JSON/pickle
- [ ] Create data validation utilities
- [ ] Test with real EnergyScope datasets
- [ ] Document data format

## Phase 5: Result Parser Enhancement

- [ ] Ensure all variables are captured
- [ ] Add computed parameters (if any)
- [ ] Ensure DataFrame indices match AMPL exactly
- [ ] Test with plotting functions
- [ ] Verify postprocessing works
- [ ] Document result format

## Phase 6: Integration

- [ ] Update `Energyscope.__init__()` to detect backend
- [ ] Add `_calc_linopy()` method
- [ ] Add backend routing in `calc()`
- [ ] Test seamless switching between backends
- [ ] Update `calc_sequence()` for linopy (if needed)
- [ ] Document usage

## Phase 7: Testing

- [ ] Unit tests for all constraint groups
- [ ] Integration tests (full model)
- [ ] Regression tests (known scenarios)
- [ ] Performance benchmarks
- [ ] Test with different solvers (Gurobi, HiGHS, CPLEX)
- [ ] Document test suite

## Phase 8: Documentation

- [ ] Complete API documentation
- [ ] Tutorial notebook for linopy backend
- [ ] Migration guide (AMPL → linopy patterns)
- [ ] Contribution guide
- [ ] Update main README
- [ ] Create examples gallery

## Phase 9: Advanced Features (Future)

- [ ] Infrastructure module (linopy version)
- [ ] LCA module (linopy version)
- [ ] Transition/pathway module (linopy version)
- [ ] Monthly model (linopy version)
- [ ] Typical days model (linopy version)

## Phase 10: Optimization (Future)

- [ ] Vectorize operations for speed
- [ ] Use sparse matrices where appropriate
- [ ] Lazy constraint generation
- [ ] Parallel solving (if applicable)
- [ ] Performance profiling
- [ ] Document optimizations

---

## Current Status

**Phase Completed**: 1, 2
**Current Phase**: 2.5 (Validation)
**Next Milestone**: Validate toy model against AMPL

## Notes

- Focus on correctness first, optimization later
- Test each constraint group before moving to next
- Document AMPL → linopy translation patterns
- Keep AMPL version as reference (don't delete)
- Maintain compatibility with existing plotting/analysis tools

## Questions / Issues

- Q: Should we parse .dat files or convert to native Python format?
  - A: TBD - Start with manual data for toy model, decide later
  
- Q: How to handle AMPL-specific syntax (e.g., `setof`, `diff`, `union`)?
  - A: Use Python set operations and list comprehensions

(Add more as they arise)

