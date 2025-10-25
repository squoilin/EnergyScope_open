"""
Wrapper script to run the PyOptInterface full model with core/minimal dataset.

This script demonstrates that the full model equations can work with a smaller
dataset by using the minimal core data instead of the full ESTD dataset.
"""

from energyscope.pyoptinterface_backend.data_loader import create_minimal_core_data
from energyscope.pyoptinterface_backend.full_model import build_full_model


if __name__ == "__main__":
    print("="*70)
    print("PyOptInterface Core Model Runner")
    print("(Full model equations with minimal core dataset)")
    print("="*70)
    
    # Load minimal core data
    print("\nLoading minimal core dataset...")
    data = create_minimal_core_data()
    print("  ✓ Minimal core data loaded.\n")
    
    # Build and solve model
    # Note: Some constraints may not be active due to missing data in minimal dataset
    result = build_full_model(
        data,
        solver='gurobi',
        verbose=True,
        enable_output=False,  # Less output for minimal model
        timing=True
    )
    
    # Print summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    if result['status'].name == 'OPTIMAL':
        print(f"  Status: OPTIMAL ✓")
        print(f"  Objective: {result['objective']:.4f} M€")
        print(f"\n  Note: This demonstrates that the full model equations")
        print(f"        work correctly even with a minimal dataset.")
        print(f"        Some constraints may not be active due to missing data.")
    else:
        print(f"  Status: {result['status'].name} ✗")
    print("="*70)

