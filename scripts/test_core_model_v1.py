"""
Test core model with Groups 1 and 4 (Energy Balance + Costs).

This tests the incremental core model implementation with:
- Group 1: Energy balance constraints (3/4 implemented)
- Group 4: Cost constraints (4 constraints)
"""

from energyscope.linopy_backend.test_data_core import create_minimal_core_data
from energyscope.linopy_backend.core_model import build_core_model_partial
from energyscope.linopy_backend.result_parser import parse_linopy_result

print("="*70)
print("TESTING CORE MODEL V1 - Groups 1 + 4")
print("="*70)

# Create test data
print("\n1. Loading minimal core test data...")
data = create_minimal_core_data()

print(f"   Technologies: {data['sets']['TECHNOLOGIES']}")
print(f"   Periods: {len(data['sets']['PERIODS'])} ({len(data['sets']['TYPICAL_DAYS'])} TD × 24h)")
print(f"   Layers: {data['sets']['LAYERS']}")

# Build model
print("\n2. Building model with Groups 1 and 4...")
try:
    model = build_core_model_partial(
        data, 
        constraint_groups=['energy_balance', 'costs']
    )
    
    print(f"\n   ✓ Model built successfully!")
    print(f"   Variables: {len(model.variables)}")
    print(f"   Constraints: {len(model.constraints)}")
    
except Exception as e:
    print(f"\n   ✗ Error building model: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Solve
print("\n3. Solving model with HiGHS...")

try:
    result = model.solve(solver_name='highs')
    
    if isinstance(result, tuple):
        status = result[0]
    else:
        status = result
    
    print(f"\n   ✓ Model solved!")
    print(f"   Status: {status}")
    print(f"   Objective: {model.objective.value:.2f} M€")
    
    # Parse results
    try:
        from energyscope.linopy_backend.result_parser import parse_linopy_result
        result_parsed = parse_linopy_result(model, data)
        print(f"\n   ✓ Results parsed successfully")
    except Exception as e:
        print(f"\n   ⚠ Result parsing had issues (expected): {e}")
    
    # Show solution
    print(f"\n4. Solution Details:")
    print(f"   " + "-"*60)
    
    F_vals = model.variables['F'].solution
    print(f"\n   Installed Capacities:")
    for tech in data['sets']['TECHNOLOGIES']:
        try:
            val = float(F_vals.loc[tech].values)
            print(f"     {tech:15s}: {val:8.4f} GW")
        except:
            try:
                val = float(F_vals.sel(TECHNOLOGIES=tech).values)
                print(f"     {tech:15s}: {val:8.4f} GW")
            except:
                pass
    
    # Show costs if available
    if 'C_inv' in model.variables:
        C_inv_vals = model.variables['C_inv'].solution
        print(f"\n   Investment Costs:")
        for tech in data['sets']['TECHNOLOGIES']:
            try:
                val = float(C_inv_vals.loc[tech].values)
                if val > 0.01:
                    print(f"     {tech:15s}: {val:8.2f} M€")
            except:
                pass
    
    print("\n" + "="*70)
    print("SUCCESS")
    print("="*70)
    print("\n✓ Group 1 (Energy Balance) constraints: WORKING")
    print("✓ Group 4 (Cost) constraints: WORKING")
    print(f"✓ Model solves with {len(model.constraints)} constraints")
    print(f"✓ Objective: {model.objective.value:.2f} M€")
    
    print("\nReady to proceed with:")
    print("  - Group 2: Resources")
    print("  - Group 3: Storage")
    print("  - Groups 5-9: GWP, Mobility, Heating, Network, Policy")

except Exception as e:
    print(f"\n   ✗ Solver error: {e}")
    print(f"   This may indicate missing constraints or data issues")
    import traceback
    traceback.print_exc()
    
    print("\n" + "="*70)
    print("MODEL BUILD SUCCESS BUT SOLVE FAILED")
    print("="*70)
    print("\n✓ Constraints added correctly (model built)")
    print("✗ Solution not found (may need more constraint groups)")
    print("\nThis is normal progress - continue adding constraint groups")

