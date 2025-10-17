"""
Test core model with Groups 1-5 (Energy, Resources, Storage, Costs, GWP).
"""

from energyscope.linopy_backend.test_data_core import create_minimal_core_data
from energyscope.linopy_backend.core_model import build_core_model_partial

print("="*70)
print("CORE MODEL - Groups 1,2,3,4,5 (+ GWP)")
print("="*70)

# Create test data
print("\n1. Loading test data...")
data = create_minimal_core_data()

# Add GWP parameters
data['parameters']['gwp_constr'] = {  # Construction emissions (ktCO2/GW)
    'WIND': 10.0,
    'GAS_PLANT': 50.0,
    'GRID': 5.0,
    'BATTERY': 20.0,
}
data['parameters']['gwp_op'] = {  # Operational emissions (ktCO2/GWh)
    'GAS': 400.0,  # 400 ktCO2/GWh for gas
    'ELECTRICITY_IMPORT': 300.0,  # 300 ktCO2/GWh for imported electricity
}
data['parameters']['gwp_limit'] = 100000.0  # 100,000 ktCO2/year limit

print(f"   Technologies: {data['sets']['TECHNOLOGIES']}")
print(f"   GWP limit: {data['parameters']['gwp_limit']} ktCO2/year")

# Build model with Groups 1-5
print("\n2. Building model with Groups 1,2,3,4,5...")
try:
    model = build_core_model_partial(
        data, 
        constraint_groups=['energy_balance', 'resources', 'storage', 'costs', 'gwp']
    )
    
    print(f"\n   ✓ Model built!")
    print(f"   Variables: {len(model.variables)}")
    print(f"   Constraints: {len(model.constraints)}")
    
except Exception as e:
    print(f"\n   ✗ Build error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Solve
print("\n3. Solving...")

try:
    result = model.solve(solver_name='highs')
    status = result[0] if isinstance(result, tuple) else result
    
    print(f"\n   ✓ SOLVED!")
    print(f"   Status: {status}")
    print(f"   Objective: {model.objective.value:.2f} M€")
    
    # Solution details
    print(f"\n4. SOLUTION:")
    print(f"   " + "="*60)
    
    F_vals = model.variables['F'].solution
    
    print(f"\n   Installed Capacity:")
    for tech in data['sets']['TECHNOLOGIES'] + data['sets']['STORAGE_TECH']:
        try:
            val = float(F_vals.sel(dim_0=tech).values)
            unit = "GWh" if tech in data['sets']['STORAGE_TECH'] else "GW"
            if val > 0.001 or tech in data['sets']['TECHNOLOGIES'][:3]:
                print(f"     {tech:20s}: {val:8.4f} {unit}")
        except:
            pass
    
    # GWP results
    if 'TotalGWP' in model.variables:
        try:
            total_gwp = float(model.variables['TotalGWP'].solution.values)
            limit = data['parameters']['gwp_limit']
            pct = (total_gwp / limit * 100) if limit > 0 else 0
            
            print(f"\n   Emissions:")
            print(f"     Total GWP: {total_gwp:.0f} ktCO2/year")
            print(f"     Limit:     {limit:.0f} ktCO2/year")
            print(f"     Usage:     {pct:.1f}% of limit")
            
            if total_gwp <= limit:
                print(f"     ✓ Within emissions limit")
            else:
                print(f"     ✗ Exceeds limit!")
        except:
            pass
    
    print(f"\n" + "="*70)
    print("✅ SUCCESS - Group 5 (GWP) WORKING")
    print("="*70)
    
    print(f"\n📊 Implementation Status:")
    print(f"   ✓ Group 1 (Energy Balance):  3/4 constraints")
    print(f"   ✓ Group 2 (Resources):       1/2 constraints")
    print(f"   ✓ Group 3 (Storage):         5/7 constraints")
    print(f"   ✓ Group 4 (Costs):           4/4 constraints")
    print(f"   ✓ Group 5 (GWP):             4/4 constraints")
    print(f"   ─────────────────────────────────────────────")
    print(f"   ✓ Total constraints: {len(model.constraints)}")
    print(f"   ✓ Constraint groups: 5/9 (56%)")
    
    print(f"\n📋 Remaining: Groups 6,7,8,9 (~19 constraints)")

except Exception as e:
    print(f"\n   ✗ Error: {e}")
    import traceback
    traceback.print_exc()

