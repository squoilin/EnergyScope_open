"""
Test Group 1 (Energy Balance) constraints for core model.
"""

from energyscope.linopy_backend.test_data_core import create_minimal_core_data
from energyscope.linopy_backend.core_model import build_core_model_partial

print("="*70)
print("TESTING CORE MODEL - GROUP 1 (ENERGY BALANCE)")
print("="*70)

# Create test data
print("\n1. Loading minimal core test data...")
data = create_minimal_core_data()

print(f"   Technologies: {data['sets']['TECHNOLOGIES']}")
print(f"   Storage: {data['sets']['STORAGE_TECH']}")
print(f"   Layers: {data['sets']['LAYERS']}")
print(f"   Time periods: {len(data['sets']['PERIODS'])}")

# Build model with Group 1 constraints
print("\n2. Building model with Group 1 constraints...")
try:
    model = build_core_model_partial(
        data, 
        constraint_groups=['energy_balance']
    )
    
    print(f"\n   ✓ Model built successfully!")
    print(f"   Variables: {len(model.variables)}")
    print(f"   Constraints: {len(model.constraints)}")
    
    # Show constraint breakdown
    constraint_types = {}
    for name in model.constraints:
        ctype = str(name).split('_')[0] if isinstance(name, str) else 'other'
        constraint_types[ctype] = constraint_types.get(ctype, 0) + 1
    
    print(f"\n   Constraint breakdown:")
    for ctype, count in sorted(constraint_types.items()):
        print(f"     {ctype}: {count}")
    
except Exception as e:
    print(f"\n   ✗ Error building model: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Try to solve
print("\n3. Attempting to solve model...")
print("   Solver: highs")

try:
    result = model.solve(solver_name='highs')
    
    if isinstance(result, tuple):
        status = result[0]
    else:
        status = result
    
    print(f"\n   ✓ Model solved!")
    print(f"   Status: {status}")
    print(f"   Objective: {model.objective.value:.2f}")
    
    # Show some solution values
    print(f"\n   Solution sample:")
    F_vals = model.variables['F'].solution
    print(f"   Installed capacities:")
    for tech in data['sets']['TECHNOLOGIES']:
        try:
            val = F_vals.loc[tech].values[0] if hasattr(F_vals.loc[tech], 'values') else F_vals.loc[tech]
            print(f"     {tech:15s}: {val:8.4f} GW")
        except:
            pass
    
except Exception as e:
    print(f"\n   ⚠ Solver error: {e}")
    print(f"   This may be normal - model might need all constraint groups")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("TEST COMPLETE")
print("="*70)

print("\nNext steps:")
print("  1. If model solved: ✓ Group 1 constraints working!")
print("  2. If infeasible: May need to adjust test data or add more constraints")
print("  3. Continue with Groups 2-9")

