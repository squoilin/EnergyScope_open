"""
A simple test script to verify that pyoptinterface is installed correctly
and can solve a basic optimization problem using the highs solver,
following the official documentation.
"""

import pyoptinterface as poi
from pyoptinterface import highs

def run_test():
    """
    Defines and solves a simple Linear Programming problem:
    Minimize: 3x + 4y
    Subject to:
        x + 2y <= 14
        3x - y >= 0
        x - y <= 2
    With:
        x, y >= 0
    """
    print("="*70)
    print("Testing PyOptInterface with highs (Documentation-based)")
    print("="*70)

    try:
        # 1. Create a model using the highs-specific backend
        model = highs.Model()
        print("  Model created with highs backend.")

        # 2. Define variables
        x = model.add_variable(lb=0, name="x")
        y = model.add_variable(lb=0, name="y")
        print(f"  Variables created: x, y")

        # 3. Add constraints
        model.add_linear_constraint(x + 2*y <= 14)
        model.add_linear_constraint(3*x - y >= 0)
        model.add_linear_constraint(x - y <= 2)
        print("  Constraints added successfully.")

        # 4. Define the objective function
        model.set_objective(3*x + 4*y, poi.ObjectiveSense.Minimize)
        print("  Objective function set.")

        # 5. Solve the model
        print("\nSolving the model...")
        model.optimize()

        # 6. Print the results
        term_status = model.get_model_attribute(poi.ModelAttribute.TerminationStatus)
        
        print("\n" + "="*70)
        print("RESULTS")
        print("="*70)
        print(f"  Termination status: {term_status}")
        
        if term_status == poi.TerminationStatusCode.OPTIMAL:
            obj_val = model.get_model_attribute(poi.ModelAttribute.ObjectiveValue)
            x_val = model.get_value(x)
            y_val = model.get_value(y)
            
            print(f"  Objective value: {obj_val:.4f}")
            print(f"  Value of x: {x_val:.4f}")
            print(f"  Value of y: {y_val:.4f}")
            print("\n✓ PyOptInterface and highs are working correctly.")
        else:
            print("\n✗ Could not find the optimal solution.")

    except Exception as e:
        print(f"\n✗ An error occurred: {e}")
        print("  Please ensure highs is correctly installed and licensed.")
        print("  Note: The 'pyoptinterface' highs backend may require the 'highspy' package.")

if __name__ == "__main__":
    run_test()
