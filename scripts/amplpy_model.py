from energyscope.energyscope import Energyscope
from energyscope.models import core
from dotenv import load_dotenv
import os
from amplpy import add_to_path


load_dotenv()
ampl_path = os.environ.get("AMPL_PATH")
if ampl_path:
    add_to_path(ampl_path)
else:
    print("AMPL_PATH not found in .env file. Please set it.")
    exit()

# Import necessary libraries
PRIVATE_LICENSE_UUID = "<REPLACE_WITH_PRIVATE_LICENSE_UUID>"

es_core = Energyscope(model=core,   # here we select the core version
                        solver_options={'solver':'gurobi'}, modules=['gurobi'],
#                        license_uuid=PRIVATE_LICENSE_UUID,
#                        notebook=True
                        )

# Solve the model
results_core = es_core.calc()
