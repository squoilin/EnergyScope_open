!!! info "Overview"
    **Prerequisites:**  
    - AMPL must be installed first and be accessible from your system’s PATH.  
    - Python 3.6 or higher is required.  

    **Utilisation methods:**  

    - **Option A:** AMPL files
        - Download the AMPL files of the model.  
        - Suitable for users who plan to modify the source code or AMPL models.
    - **Option B:** Python library
        - Install EnergyScope via `pip install energyscope`.  
        - Ideal for users who want a simple setup without modifying the source code.  

Welcome to the EnergyScope library! This guide will help you set up and start using EnergyScope, whether you’re a beginner looking to run optimizations or an expert aiming to modify the source code.

## Prerequisites

Before you begin, please ensure you have the following:

1. **Install AMPL**

    - EnergyScope relies on AMPL (A Mathematical Programming Language) for optimization modeling. AMPL must be installed first and be accessible from your system’s PATH.
    - See the [Installing AMPL section](#installing-ampl) below for detailed instructions.

2. **Install Python**

    - Version: Python 3.6 or higher.
    - Environment: We recommend using a virtual environment to manage package dependencies.

---

## Choose Your Path

### Option A: AMPL files

If you plan to customize the source code or the underlying AMPL models:

1. **Download the AMPL files**:

    <div style="text-align: center;">
  <a href='https://gitlab.com/energyscope/energyscope/-/raw/main/docs/assets/ES-core.zip?ref_type=heads&inline=false' target="_blank" 
     style="padding: 10px 20px; background-color:rgb(58, 113, 223); color: white; 
            text-decoration: none; border-radius: 4px; display: inline-block;">
    Download AMPL files
  </a>
</div>


2. **Solve AMPL using [AMPLpy](https://amplpy.ampl.com/en/latest/) **:

    - Make sure you have installed the AMPLpy package. You can do this using pip: 

    ```bash
    pip install amplpy
    ```

    - Load and solve the model using the following code:

    ```python
    import amplpy

    # Initialize AMPL
    ampl = AMPL()  # or AMPL(env) if you specify an environment

    # Set the path to your model and data files
    model_path = "path/to/your_project/"  # Adjust this to your project path

    # Load model and data files
    ampl.read(model_path + "ESTD_model_core.mod")  # The main AMPL model
    ampl.readData(model_path + "ESTD_12TD.dat")  # The corresponding timeseries file
    ampl.readData(model_path + "ESTD_data_core.dat")  # The corresponding data file

    # Optionally set solver
    ampl.setOption("solver", "highs")  # or "cplex", "gurobi", etc.

    # Solve the model
    ampl.solve()

    # Get results (example: TotalCost)
    TotalCost = ampl.getVariable("TotalCost")
    print("Total cost:", TotalCost.get().value())

    ```


### Option B: Python library

If you’re new to EnergyScope and want a quick setup without delving into the source code:

1. **Install EnergyScope via `pip`**:

    ```bash
    pip install energyscope
    ```

2. **Run the core model**:

    ```python
    # Import necessary libraries
    from energyscope.energyscope import Energyscope
    from energyscope.models import core

    # Load the model
    es_core = Energyscope(model=core)

    # Solve the model
    results_core = es_core.calc()

    # Access results
    results_core.variables['TotalCost']
    ```

## Installing AMPL

EnergyScope uses AMPL for optimization modeling. Follow these steps to install AMPL on your system:

1. **Download AMPL**

    - Visit the [AMPL Community Edition](https://ampl.com/ce/) page to download the appropriate version for your operating system.

2. **Install AMPL**

    - **Windows**:
    
        - Run the installer and follow the on-screen instructions.
    
    - **Linux and macOS**:
    
        - Extract the downloaded archive to a directory where you have read and write permissions (e.g., your home directory).

3. **Activate Your License**

    - AMPL Community Edition requires a free license.
    - During installation, you’ll receive a license UUID.
    - Activate your license by running the following command in the AMPL command prompt:

        ```bash
        shell "amplkey activate --uuid <license-uuid>";
        ```

      Replace `<license-uuid>` with your actual license UUID.

    !!! warning 
        Restart AMPL after activation to start using the new license.

4. **Add AMPL to PATH**

    - **Windows**:
    
        - Add the AMPL installation directory (e.g., `C:\AMPL`) to your system’s PATH environment variable.
    
    - **Linux and macOS**:
    
        - Open your terminal and add the following line to your `.bashrc` or `.bash_profile`:

        ```bash
        export PATH="/path/to/ampl:$PATH"
        ```

      Replace `/path/to/ampl` with the actual path to your AMPL directory.

5. **Verify AMPL Installation**

    To confirm that AMPL is correctly installed:

    - Open Command Prompt or Terminal:
    
        - Open a new command prompt (Windows) or terminal window (Linux/macOS).
    
    - Run AMPL:

        ```bash
        ampl
        ```

    - If installed correctly, you should see the `ampl:` prompt. You can quit with the command:

        ```
        quit;
        ```

---

## Want to Learn More?

- **Basic Documentation:** Check out the [EnergyScope Conceptual Formulation](../explanation/index.md).
- **Community Support:** Find the FAQ on the [forum page](https://forum.energyscope.net/).
- **EnergyScope Models:** Explore the various developement on the [model page](../models/index.md).
