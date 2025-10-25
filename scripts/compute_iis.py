"""
Load the LP file and compute IIS using Gurobi directly.
"""
import gurobipy as gp

print("Loading model...")
model = gp.read("pyopt_full_model.lp")

print("Computing IIS...")
model.computeIIS()

print("Writing IIS...")
model.write("pyopt_full_model.ilp")

print("\nIIS Summary:")
print(f"Number of constraints in IIS: {sum(1 for c in model.getConstrs() if c.IISConstr)}")
print(f"Number of bounds in IIS: {sum(1 for v in model.getVars() if v.IISLB or v.IISUB)}")

print("\nFirst 20 constraints in IIS:")
count = 0
for c in model.getConstrs():
    if c.IISConstr and count < 20:
        print(f"  {c.ConstrName}")
        count += 1

print("\nFirst 10 variable bounds in IIS:")
count = 0
for v in model.getVars():
    if (v.IISLB or v.IISUB) and count < 10:
        bound_type = "LB" if v.IISLB else "UB"
        print(f"  {v.VarName} ({bound_type})")
        count += 1

print("\n✓ IIS written to pyopt_full_model.ilp")

