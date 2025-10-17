"""
Example script for running EnergyScope with linopy backend.

This script demonstrates how to use the linopy backend instead of AMPL
for solving optimization models. The toy model is a simplified version
for testing and validation.
"""

from energyscope.models import core_toy_linopy
from energyscope.linopy_backend.data_loader import create_toy_data
from energyscope.linopy_backend.toy_model import solve_toy_model
from energyscope.linopy_backend.result_parser import parse_linopy_result

# Create toy data
print("Loading toy model data...")
data = create_toy_data()

print("\nModel configuration:")
print(f"  Technologies: {data.sets['TECHNOLOGIES']}")
print(f"  Layers: {data.sets['LAYERS']}")
print(f"  Time periods: {len(data.sets['PERIODS'])} hours")
print(f"  Storage technologies: {data.sets['STORAGE_TECH']}")

# Build and solve model
print("\nBuilding and solving linopy model...")
print("Solver: highs")

try:
    model, status = solve_toy_model(data, solver='highs')
    
    print(f"\nSolution status: {status}")
    print(f"Objective value: {model.objective.value:.2f} M€")
    
    # Parse results
    result = parse_linopy_result(model, data)
    
    # Display key results
    print("\n=== Installed Capacity (F) ===")
    print(result.variables['F'])
    
    print("\n=== Total Cost ===")
    print(result.objectives['TotalCost'])
    
    # Show some operational details
    print("\n=== Sample Operation (first 6 hours) ===")
    F_t = result.variables['F_t']
    print(F_t[F_t.index.get_level_values('index1') <= 6])
    
    if 'Storage_level' in result.variables:
        print("\n=== Storage Level (first 6 hours) ===")
        Storage = result.variables['Storage_level']
        print(Storage[Storage.index.get_level_values('index1') <= 6])
    
    print("\n✓ Model solved successfully!")
    
except Exception as e:
    print(f"\n✗ Error solving model: {e}")
    import traceback
    traceback.print_exc()

