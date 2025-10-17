import os
import amplpy
from amplpy import AMPL, add_to_path
from dotenv import load_dotenv

load_dotenv()
ampl_path = os.environ.get("AMPL_PATH")
if ampl_path:
    add_to_path(ampl_path)
else:
    print("AMPL_PATH not found in .env file. Please set it.")
    exit()

# Initialize AMPL
ampl = AMPL()  # or AMPL(env) if you specify an environment

# Set the path to your model and data files
model_path = "src/energyscope/data/models/core/td/"  # Adjust this to your project path
data_path = "src/energyscope/data/datasets/core/td/"

# Load model and data files
ampl.read(model_path + "ESTD_model_core.mod")  # The main AMPL model
ampl.readData(data_path + "ESTD_12TD.dat")    # The corresponding timeseries file
ampl.readData(data_path + "ESTD_data_core.dat")  # The corresponding data file

# Optionally set solver
ampl.setOption("solver", "gurobi")  # or "cplex", "gurobi", "highs", etc.

# Solve the model
ampl.solve()
