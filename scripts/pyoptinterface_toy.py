"""
Wrapper script to run the PyOptInterface toy model.

This script loads toy dataset and builds/solves the model using PyOptInterface.
"""

from energyscope.pyoptinterface_backend.data_loader import create_toy_data
from energyscope.pyoptinterface_backend.toy_model import build_toy_model


if __name__ == "__main__":
    # Load toy data
    print("Loading toy dataset...")
    data = create_toy_data()
    print("  ✓ Toy data loaded.\n")
    
    # Build and solve model
    result = build_toy_model(data, solver='highs', verbose=True)
    
    # Print summary
    if result['status'].name == 'OPTIMAL':
        print(f"\nFinal objective: {result['objective']:.4f} M€")
    else:
        print(f"\nModel did not solve to optimality. Status: {result['status']}")

