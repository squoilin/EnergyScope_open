"""
Wrapper script to run the PyOptInterface full model with ESTD dataset.

This script loads the full ESTD dataset and builds/solves the model using PyOptInterface
with Gurobi solver.
"""

import time
#from energyscope.linopy_backend.data_loader_full import create_full_dataset
from energyscope.pyoptinterface_backend.data_loader import create_full_dataset
from energyscope.pyoptinterface_backend.full_model import build_full_model


if __name__ == "__main__":
    print("="*70)
    print("PyOptInterface Full Model Runner")
    print("="*70)
    
    # Load data
    print("\n[1/2] Loading ESTD dataset...")
    t_data_start = time.time()
    data = create_full_dataset()
    t_data = time.time() - t_data_start
    print(f"  ✓ Data loaded in {t_data:.2f}s\n")
    
    # Build and solve model
    print("[2/2] Building and solving model...")
    result = build_full_model(
        data,
        solver='gurobi',
        verbose=True,
        enable_output=True,
        timing=True
    )
    
    # Print final summary
    print("\n" + "="*70)
    print("FINAL SUMMARY")
    print("="*70)
    if result['status'].name == 'OPTIMAL':
        print(f"  Status: OPTIMAL ✓")
        print(f"  Objective: {result['objective']:.4f} M€")
        if 'timing' in result:
            print(f"\n  Performance:")
            print(f"    Data loading:   {t_data:>8.2f}s")
            print(f"    Model building: {result['timing']['build']:>8.2f}s")
            print(f"    Solving:        {result['timing']['solve']:>8.2f}s")
            print(f"    TOTAL:          {t_data + result['timing']['total']:>8.2f}s")
    else:
        print(f"  Status: {result['status'].name} ✗")
        print(f"  Model did not solve to optimality.")
    print("="*70)

