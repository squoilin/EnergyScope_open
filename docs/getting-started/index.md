# Getting Started

This guide will help you set up and start using a basic version of EnergyScope, which we call the "core" version and which is documented [here](../explanation/core_version_documentation.md). EnergyScope is written in AMPL (A Mathematical Programming Language, see the documentation [here](https://dev.ampl.com/ampl/books/index.html#ampl-a-modeling-language-for-mathematical-programming)). AMPL is free for academics and students, and includes licences for commercial solvers (e.g., Gurobi). Once you have familiarized yourself with AMPL and the core version, you can adapt these instructions to run other [model versions](../models/index.md) of EnergyScope.

---

## Prerequisites

To start with, please:

1. **Install Python**

    - Version: Python 3.6 or higher.
    - Environment: We recommend using a virtual environment to manage package dependencies.

2. **(Optional) Install AMPL manually**

    - This step is **only required if you plan to use EnergyScope directly with AMPL (Option A)**.
    - Visit the [AMPL webpage](https://dev.ampl.com/ampl/install.html) to download and install the appropriate version for your operating system. 
    - For MacOS and Linux users, make sure to add AMPL to your system PATH. You can provide the path to your license file in a `.env` file located at the root of your project, containing the following line:  
      `AMPL_PATH="path_to_your_license"`

---

!!! info "Options for using EnergyScope"

	There are two options for using EnergyScope: 

    - **Option A:** Directly using AMPL and `amplpy`
    	  - Allows running any version of EnergyScope and offers full flexibility to customize inputs, constraints, or model structure. 
    	  - Does **not** include built-in tools for preprocessing or postprocessing. 
    	  - Requires a manual AMPL installation.

    - **Option B:** Using the `energyscope` Python Library
    	  - The `energyscope` Python Library makes it easier to run EnergyScope models and includes helpers for postprocessing results and visualizing outputs.  
    	  - AMPL is **automatically installed and configured** when installing the library — no manual AMPL setup is required.  
    	  - May be less flexible and not compatible with all EnergyScope versions.

	If you are not sure which option to choose, don't worry! Both options will allow you to get your first results in a few minutes.

---

## Running your first model

### Option A: Using AMPL and `amplpy`

1. **Download the core version AMPL files**:

    <div style="text-align: center;">
  <a href='https://gitlab.com/energyscope/energyscope/-/raw/main/docs/assets/ES-core.zip?ref_type=heads&inline=false' target="_blank" 
     style="padding: 10px 20px; background-color:rgb(58, 113, 223); color: white; 
            text-decoration: none; border-radius: 4px; display: inline-block;">
    Download AMPL files
  </a>
</div>

	Move the files into your working folder. 

2. **Run the core model**:
    
    - Make sure you have installed the [amplpy package](https://amplpy.ampl.com/en/latest/). You can do this using pip: 

    ```bash
    pip install amplpy
    ```

    - Load and solve the model using the following python code. The code reads in the model and data files and solves them using the open-source solver Highs. 

    ```python
    import amplpy

    # Initialize AMPL
    ampl = AMPL()  # or AMPL(env) if you specify an environment

    # Set the path to your model and data files
    model_path = "path/to/your_project/"  # Adjust this to your project path

    # Load model and data files
    ampl.read(model_path + "ESTD_model_core.mod")  # The main AMPL model
    ampl.readData(model_path + "ESTD_12TD.dat")    # The corresponding timeseries file
    ampl.readData(model_path + "ESTD_data_core.dat")  # The corresponding data file

    # Optionally set solver
    ampl.setOption("solver", "highs")  # or "cplex", "gurobi", etc.

    # Solve the model
    ampl.solve()
    ```
    
    - After solving the model, you can print, export and manipulate the solution using `amplpy` commands. 
    
    ```python
    # Get results (example: TotalCost)
    TotalCost = ampl.getVariable("TotalCost")
    print("Total cost:", TotalCost.get().value())
    ```


### Option B: Using the Python Library

1. **Install the `energyscope` library (AMPL included automatically)**:

    ```bash
    pip install energyscope
    ```

    > 📝 *This installation will automatically install and configure AMPL, so you don’t need to install it separately.*

2. **Run the core model**:

    - Load and solve the core version using library. Make sure to replace the license UUID with your own, you can access it directly from the [AMPL portal](https://portal.ampl.com/user/ampl/license/list). If you don't have an account please create one, and favor your academic address to get access to the free academic license.
    
    ```python
    from energyscope.energyscope import Energyscope
    from energyscope.models import core

    # Import necessary libraries
    PRIVATE_LICENSE_UUID = "<REPLACE_WITH_PRIVATE_LICENSE_UUID>"

    es_core = Energyscope(model=core,   # here we select the core version
                          solver_options={'solver':'gurobi','gurobi_options':'outlev=1'}, modules=['gurobi'],
                            license_uuid=PRIVATE_LICENSE_UUID,
                            notebook=True)

    # Solve the model
    results_core = es_core.calc()
    ```
    
    - After solving the model, you can print, export and manipulate the solution using library commands. 

    ```python
    # Access results
    results_core.variables['TotalCost']
    ```

---

## Want to learn more?

- **Documentation:** Check out the EnergyScope [Documentation](../explanation/index.md) to understand the model formulation.
- **Community Support:** Find the FAQ on the [forum page](https://forum.energyscope.net/).
- **EnergyScope Model Versions:** Explore the various developments on the [Model Versions](../models/index.md) page.
- **Python Library:** Check out the tutorials for the [energyscope Python Library](../library/index.md).
