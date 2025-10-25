"""
Toy model implementation in linopy using xarray operations.

This is a refactored version of toy_model.py that uses vectorized xarray
operations instead of nested for loops. The mathematical model is identical,
but the implementation is cleaner and more efficient.

Changes from original:
- All parameters are xarray DataArrays
- Constraints use vectorized operations (no nested loops)
- Leverages automatic broadcasting and alignment
"""

import linopy
import numpy as np
import xarray as xr


def build_toy_model_xarray(data: dict) -> linopy.Model:
    """
    Build a simplified EnergyScope model using xarray operations.
    
    This toy model includes:
    1. Decision variables: F (capacity), F_t (operation), Storage_level
    2. Constraints (all vectorized):
       - Capacity limits (F_t <= F * c_p_t)
       - Energy balance (production >= demand)
       - Storage balance (temporal)
       - Storage capacity limits
    3. Objective: Minimize total cost (investment + maintenance + operation)
    
    Args:
        data: Dictionary with 'sets' and 'params' containing xarray DataArrays
              (as returned by create_toy_data_xarray())
        
    Returns:
        linopy.Model instance ready to solve
    """
    m = linopy.Model()
    
    # =========================================================================
    # EXTRACT DATA
    # =========================================================================
    
    # Extract sets
    TECHNOLOGIES = data['sets']['TECHNOLOGIES']
    STORAGE_TECH = data['sets']['STORAGE_TECH']
    LAYERS = data['sets']['LAYERS']
    PERIODS = data['sets']['PERIODS']
    TECH_NOSTORAGE = data['sets']['TECH_NOSTORAGE']
    
    # Extract parameters (these are xarray DataArrays)
    F_MAX = data['params']['F_MAX']
    F_MIN = data['params']['F_MIN']
    C_INV = data['params']['C_INV']
    C_MAINT = data['params']['C_MAINT']
    LIFETIME = data['params']['LIFETIME']
    LAYERS_IN_OUT = data['params']['LAYERS_IN_OUT']
    C_P_T = data['params']['C_P_T']
    DEMAND = data['params']['DEMAND']
    STORAGE_EFF_IN = data['params']['STORAGE_EFF_IN']
    STORAGE_EFF_OUT = data['params']['STORAGE_EFF_OUT']
    C_OP_GAS = data['params']['C_OP_GAS']
    C_OP_GRID = data['params']['C_OP_GRID']
    I_RATE = data['params']['I_RATE']
    
    # =========================================================================
    # DECISION VARIABLES
    # =========================================================================
    
    print("Creating decision variables...")
    
    # F: Installed capacity [GW] or storage capacity [GWh]
    # Shape: (tech,)
    F = m.add_variables(
        lower=F_MIN,
        upper=F_MAX,
        coords=[TECHNOLOGIES],
        name="F"
    )
    
    # F_t: Operation level at each time period [GW]
    # Shape: (tech_nostorage, period)
    F_t = m.add_variables(
        lower=0,
        coords=[TECH_NOSTORAGE, PERIODS],
        name="F_t"
    )
    
    # Storage variables
    if len(STORAGE_TECH) > 0:
        # Storage_in: Energy going into storage [GW]
        # Shape: (storage, period)
        Storage_in = m.add_variables(
            lower=0,
            coords=[STORAGE_TECH, PERIODS],
            name="Storage_in"
        )
        
        # Storage_out: Energy coming out of storage [GW]
        # Shape: (storage, period)
        Storage_out = m.add_variables(
            lower=0,
            coords=[STORAGE_TECH, PERIODS],
            name="Storage_out"
        )
        
        # Storage_level: Energy stored [GWh]
        # Shape: (storage, period)
        Storage_level = m.add_variables(
            lower=0,
            coords=[STORAGE_TECH, PERIODS],
            name="Storage_level"
        )
    
    print(f"  ✓ Created {len(m.variables)} variable groups")
    
    # =========================================================================
    # CONSTRAINTS
    # =========================================================================
    
    print("Adding constraints...")
    
    # -------------------------------------------------------------------------
    # Constraint 1: Capacity Limits (VECTORIZED)
    # F_t[tech, period] <= F[tech] * C_P_T[tech, period]
    # -------------------------------------------------------------------------
    print("  1. Capacity limits (vectorized)...")
    
    # Select only non-storage techs from F and C_P_T
    # F shape: (tech,) → select subset → (tech_nostorage,)
    # C_P_T shape: (tech, period) → select subset → (tech_nostorage, period)
    F_nostorage = F.sel(tech=TECH_NOSTORAGE)
    C_P_T_nostorage = C_P_T.sel(tech=TECH_NOSTORAGE)
    
    # Vectorized constraint using broadcasting
    # F_nostorage: (tech_nostorage,) broadcasts to (tech_nostorage, period)
    # C_P_T_nostorage: (tech_nostorage, period)
    # F_t: (tech_nostorage, period)
    m.add_constraints(
        F_t <= F_nostorage * C_P_T_nostorage,
        name='capacity_limit'
    )
    print(f"     Added {len(TECH_NOSTORAGE) * len(PERIODS)} capacity limit constraints")
    
    # -------------------------------------------------------------------------
    # Constraint 2: Energy Balance (VECTORIZED)
    # sum_tech(F_t * layers_in_out) + storage_net >= demand (by layer, period)
    # -------------------------------------------------------------------------
    print("  2. Energy balance (vectorized)...")
    
    # Calculate production by layer from technologies
    # LAYERS_IN_OUT: (tech, layer)
    # F_t: (tech_nostorage, period)
    # We need to compute: sum_tech(F_t[tech, period] * LAYERS_IN_OUT[tech, layer])
    # Result should be: (layer, period)
    
    # Select only non-storage rows from LAYERS_IN_OUT
    LAYERS_IN_OUT_nostorage = LAYERS_IN_OUT.sel(tech=TECH_NOSTORAGE)
    
    # We can't use xr.dot with linopy variables, so use multiplication and sum
    # F_t: (tech_nostorage, period)
    # LAYERS_IN_OUT_nostorage: (tech_nostorage, layer)
    # We want: sum over tech of F_t[tech, period] * LAYERS_IN_OUT[tech, layer]
    # Result: (layer, period)
    
    # Multiply F_t by each layer coefficient and sum
    # (F_t * LAYERS_IN_OUT_nostorage): creates (tech, period, layer) then sum over tech
    production_by_layer = (F_t * LAYERS_IN_OUT_nostorage).sum(dim='tech')
    
    # Create demand array matching production shape
    # DEMAND: (period,) → need (layer, period)
    # Only END_USE layer has demand
    demand_by_layer = xr.DataArray(
        np.zeros((len(LAYERS), len(PERIODS))),
        coords=[LAYERS, PERIODS],
        dims=['layer', 'period']
    )
    demand_by_layer.loc[dict(layer='END_USE')] = DEMAND
    
    # Add constraints for each layer (need to handle storage separately)
    for layer in LAYERS:
        production_layer = production_by_layer.sel(layer=layer)
        demand_layer = demand_by_layer.sel(layer=layer)
        
        # Add storage contribution only to ELECTRICITY layer
        if len(STORAGE_TECH) > 0 and layer == 'ELECTRICITY':
            # Storage net output: out * eff_out - in / eff_in
            # All shapes: (storage, period)
            storage_net_out = Storage_out * STORAGE_EFF_OUT - Storage_in / STORAGE_EFF_IN
            
            # Sum over storage dimension: (period,)
            storage_net_total = storage_net_out.sum(dim='storage')
            
            # Add to production
            m.add_constraints(
                production_layer + storage_net_total >= demand_layer,
                name=f'energy_balance_{layer}'
            )
        else:
            # No storage for this layer
            m.add_constraints(
                production_layer >= demand_layer,
                name=f'energy_balance_{layer}'
            )
    
    print(f"     Added {len(LAYERS) * len(PERIODS)} energy balance constraints")
    
    # -------------------------------------------------------------------------
    # Constraint 3: Storage Balance (VECTORIZED with temporal shift)
    # Storage_level[t] = Storage_level[t-1] + in * eff_in - out / eff_out
    # -------------------------------------------------------------------------
    if len(STORAGE_TECH) > 0:
        print("  3. Storage balance (vectorized with shift)...")
        
        # Storage flows: in * eff_in - out / eff_out
        # Shapes: (storage, period)
        storage_delta = Storage_in * STORAGE_EFF_IN - Storage_out / STORAGE_EFF_OUT
        
        # Initial period (first period): starts at 50% capacity
        # Select just the first period (PERIODS[0] = 1)
        # Syntax: .loc[:, PERIODS[0]] selects all storage, single period
        first_period = PERIODS[0]
        m.add_constraints(
            Storage_level.loc[:, first_period] == 
            0.5 * F.loc[STORAGE_TECH] + storage_delta.loc[:, first_period],
            name='storage_balance_initial'
        )
        
        # All other periods (t > 0): depends on previous period
        # Use .shift(period = 1) to shift along the period dimension
        # Then slice to PERIODS[1:] to get t=1, t=2, ... (where t-1 exists after shift)
        m.add_constraints(
            Storage_level.loc[:, PERIODS[1:]] == 
            Storage_level.shift(period=1) + storage_delta.loc[:, PERIODS[1:]],
            name='storage_balance'
        )
        
        print(f"     Added {len(STORAGE_TECH) * len(PERIODS)} storage balance constraints")
        
        # ---------------------------------------------------------------------
        # Constraint 4: Storage Capacity Limits (VECTORIZED)
        # Storage_level[storage, period] <= F[storage]
        # ---------------------------------------------------------------------
        print("  4. Storage capacity limits (vectorized)...")
        
        # F.loc[STORAGE_TECH] broadcasts to match Storage_level dimensions
        # Storage_level: (storage, period), F.loc[STORAGE_TECH]: (storage,) → broadcasts
        m.add_constraints(
            Storage_level <= F.loc[STORAGE_TECH],
            name='storage_capacity'
        )
        print(f"     Added {len(STORAGE_TECH) * len(PERIODS)} storage capacity constraints")
        
        # ---------------------------------------------------------------------
        # Constraint 5: Storage Cyclic Boundary (VECTORIZED)
        # Storage_level[storage, last_period] == 0.5 * F[storage]
        # ---------------------------------------------------------------------
        print("  5. Storage cyclic boundary (vectorized)...")
        
        # Select just the last period
        last_period = PERIODS[-1]
        m.add_constraints(
            Storage_level.loc[:, last_period] == 0.5 * F.loc[STORAGE_TECH],
            name='storage_cyclic'
        )
        print(f"     Added {len(STORAGE_TECH)} storage cyclic constraints")
    
    # =========================================================================
    # OBJECTIVE FUNCTION (VECTORIZED)
    # =========================================================================
    
    print("Adding objective function...")
    
    # -------------------------------------------------------------------------
    # Investment Cost (annualized)
    # -------------------------------------------------------------------------
    # Calculate capital recovery factor (CRF) for each technology
    # CRF = i(1+i)^n / ((1+i)^n - 1)
    # LIFETIME: (tech,) → tau: (tech,)
    tau = I_RATE * (1 + I_RATE)**LIFETIME / ((1 + I_RATE)**LIFETIME - 1)
    
    # Annualized investment cost
    # F: (tech,), C_INV: (tech,), tau: (tech,)
    # Result: scalar
    investment_cost = (F * C_INV * tau).sum()
    
    # -------------------------------------------------------------------------
    # Maintenance Cost (annual)
    # -------------------------------------------------------------------------
    # F: (tech,), C_MAINT: (tech,)
    # Result: scalar
    maintenance_cost = (F * C_MAINT).sum()
    
    # -------------------------------------------------------------------------
    # Operating Cost (resource consumption)
    # -------------------------------------------------------------------------
    # Gas consumption: F_t['GAS_PLANT'] * |layers_in_out['GAS_PLANT', 'GAS']|
    # LAYERS_IN_OUT.sel(tech='GAS_PLANT', layer='GAS') is negative, so negate it
    
    operating_cost = 0
    
    # Gas cost
    if 'GAS_PLANT' in TECH_NOSTORAGE:
        # F_t.loc['GAS_PLANT', :]: all periods for GAS_PLANT
        # LAYERS_IN_OUT.loc['GAS_PLANT', 'GAS']: scalar (= -1.0)
        gas_consumption = -F_t.loc['GAS_PLANT', :] * LAYERS_IN_OUT.loc['GAS_PLANT', 'GAS'].item()
        # Sum over periods: scalar
        operating_cost += (gas_consumption * C_OP_GAS).sum()
    
    # Grid import cost
    if 'GRID' in TECH_NOSTORAGE:
        # F_t.loc['GRID', :]: all periods for GRID
        grid_consumption = F_t.loc['GRID', :]
        operating_cost += (grid_consumption * C_OP_GRID).sum()
    
    # -------------------------------------------------------------------------
    # Total Cost
    # -------------------------------------------------------------------------
    total_cost = investment_cost + maintenance_cost + operating_cost
    
    m.add_objective(total_cost, sense="min")
    print(f"  ✓ Objective function added")
    
    print(f"\n✓ Model built: {len(m.variables)} variable groups, {len(m.constraints)} constraint groups")
    
    return m


def solve_toy_model_xarray(data: dict, solver='highs', solver_options=None):
    """
    Build and solve the toy model using xarray operations.
    
    Args:
        data: Dictionary with xarray-based data (from create_toy_data_xarray())
        solver: Solver name (e.g., 'gurobi', 'highs', 'glpk')
        solver_options: Dict of solver-specific options
        
    Returns:
        Tuple of (model, solution_status)
    """
    # Build model
    print("=" * 70)
    print("BUILDING XARRAY TOY MODEL")
    print("=" * 70)
    model = build_toy_model_xarray(data)
    
    # Solve
    print("\n" + "=" * 70)
    print(f"SOLVING WITH {solver.upper()}")
    print("=" * 70)
    
    if solver_options is None:
        solver_options = {}
    
    try:
        result = model.solve(solver_name=solver, **solver_options)
        
        # Handle different linopy versions
        if isinstance(result, tuple):
            status = result[0]
        else:
            status = result
        
        print(f"\n✓ Solution status: {status}")
        print(f"✓ Objective value: {model.objective.value:.6f} M€")
        
        return model, status
    except Exception as e:
        print(f"\n✗ Solver error: {e}")
        raise


if __name__ == "__main__":
    """Test the xarray toy model."""
    from data_loader_xarray import create_toy_data_xarray
    
    print("Loading xarray data...")
    data = create_toy_data_xarray()
    
    print("\nBuilding and solving xarray model...")
    try:
        model, status = solve_toy_model_xarray(data, solver='highs')
        
        print("\n" + "=" * 70)
        print("SOLUTION SUMMARY")
        print("=" * 70)
        
        # Display key results
        print("\n--- Installed Capacity (F) ---")
        F_solution = model.solution['F']
        for tech in data['sets']['TECHNOLOGIES']:
            val = F_solution.sel(tech=tech).values
            print(f"  {tech:15s}: {val:8.3f} GW")
        
        print(f"\n--- Total Cost ---")
        print(f"  Objective: {model.objective.value:.2f} M€")
        
        print("\n✓ XArray toy model test completed successfully!")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

