"""
Test script for running the non-vectorized Linopy core model with the full dataset.

This script loads the complete dataset from the AMPL .dat files,
builds the Linopy model, and attempts to solve it.

Warning: Model building with the full dataset is extremely slow due to the
inefficient, loop-based model formulation. It may take a very long time
or exhaust available memory. It is expected that you may need to terminate
this script manually.
"""

import sys
from pathlib import Path

# Add src to path for local imports
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.energyscope.linopy_backend.data_loader_full import create_full_dataset
from src.energyscope.linopy_backend.core_model import build_core_model


def run_test():
    """Load data, build, and solve the model."""
    print("="*70)
    print("RUNNING LINOPY CORE MODEL WITH FULL DATASET")
    print("="*70)

    # Load the full dataset
    print("\nStep 1: Loading and converting full AMPL dataset...")
    try:
        data = create_full_dataset()
        print("\n✓ Full dataset loaded and converted successfully.")
    except Exception as e:
        print(f"\n✗ Data loading failed: {e}")
        import traceback
        traceback.print_exc()
        return

    # Build the core model
    print("\n" + "="*70)
    print("Step 2: Building the Linopy core model...")
    print("This is the highly inefficient step. Please be patient.")
    print("It is normal for this to take a very long time or run out of memory.")
    print("="*70)
    try:
        model = build_core_model(data)
        print("\n✓ Model built successfully!")
        print(f"  Variables: {len(model.variables)}")
        print(f"  Constraints: {len(model.constraints)}")
    except Exception as e:
        print(f"\n✗ Model building failed: {e}")
        import traceback
        traceback.print_exc()
        return

    # Solve the model
    print("\n" + "="*70)
    print("Step 3: Solving the model...")
    print("="*70)
    try:
        model.solve(solver_name='gurobi')
        print("\n✓ Model solved successfully!")
        print(f"  Status: {model.solution.status}")
        print(f"  Objective: {model.objective.value:.2f}")
    except Exception as e:
        print(f"\n✗ Model solving failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_test()
