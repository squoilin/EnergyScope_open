!!! info "Overview"
    **[Prerequisites](#prerequisites):**  
    - AMPL must be installed first and be accessible from your system’s PATH.  
    - Python 3.6 or higher is required.  
    **[Installation Paths](#choose-your-path):**  
    **[Option A](#option-a-quick-start-for-beginners):** Quick Start for Beginners 😎  
        - Install EnergyScope via `pip install energyscope`.  
        - Ideal for users who want a simple setup without modifying the source code.  
    **[Option B](#option-b-editable-installation-for-experts):** Editable Installation for Experts 🏄  
        - Clone the EnergyScope repository and install in editable mode.  
        - Suitable for users who plan to modify the source code or AMPL models.

    - AMPL must be installed first and be accessible from your system’s PATH.
    - Python 3.6 or higher is required.

    **Installation Paths:**

    - **Option A:** Quick Start for Beginners 😎
        - Install EnergyScope via `pip`.
        - Ideal for users who want a simple setup without modifying the source code.
    - **Option B:** Editable Installation for Experts 🏄
        - Clone the EnergyScope repository and install in editable mode.
        - Suitable for users who plan to modify the source code or AMPL models.

Welcome to the EnergyScope library! This guide will help you set up and start using EnergyScope, whether you’re a beginner looking to run simulations or an expert aiming to modify the source code.

## Prerequisites

Before you begin, please ensure you have the following:

1. **Install AMPL**

    - EnergyScope relies on AMPL (A Mathematical Programming Language) for optimization modeling. AMPL must be installed first and be accessible from your system’s PATH.
    - See the [Installing AMPL section](#installing-ampl) below for detailed instructions.

2. **Install Python**

    - Version: Python 3.6 or higher.
    - Environment: We recommend using a virtual environment to manage dependencies.

---

## Choose Your Path

### Option A: Quick Start for Beginners 😎

If you’re new to EnergyScope and want a quick setup without delving into the source code:

1. **Install EnergyScope via `pip`**:

    ```bash
    pip install energyscope
    ```

2. **Run the Basic Tutorial**:

    Get started by following our [Basic Run Tutorial](../tutorials/basic-run.ipynb) to familiarize yourself with EnergyScope.

### Option B: Editable Installation for Experts 🏄

If you plan to customize the source code or the underlying AMPL models:

1. **Clone the EnergyScope Repository**:

    ```bash
    git clone https://gitlab.com/energyscope/energyscope.git
    ```

2. **Install EnergyScope in Editable Mode**:

    Navigate to the cloned repository and install the package in editable mode:

    ```bash
    cd energyscope
    pip install -e .
    ```

    Alternatively, if you’re working within a Jupyter notebook or an interactive environment, you can use:

    ```python
    # Clone the repository
    !git clone git@gitlab.com:energyscope/energyscope.git

    # Install the package in editable mode
    %pip install -e ./energyscope

    # Add the package to the Python path (if necessary)
    import sys
    sys.path.append('./energyscope')
    ```

3. **Modify and Run Code**:

    You’re now ready to explore and modify the source code and AMPL models according to your needs.

---

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

## Running EnergyScope

With both EnergyScope and AMPL installed, you’re ready to run simulations. Browse through the tutorials to learn how to get started with the code in this project.

- **Basic Run:**
  
    - Start with the [Basic Run Tutorial](../tutorials/basic-run.ipynb) to learn how to set up and execute a basic energy model.

- **Change Model:**
  
    - Proceed with the [Change Model](../tutorials/choose-datasets.ipynb) to learn how to switch between different models and datasets.

- **Multiple Runs:**
  
    - Once the models selected, you can run multiple times with the [Mutliple Runs Tutorial](../tutorials/multiple-runs.ipynb) to learn how to make a parametrization.

- **and many more...**
  
---

## Need Help?

If you have any questions or run into issues:

- **Documentation:** Check out the [EnergyScope Documentation](../explanation/index.md).
- **Community Support:** [Join our community](https://join.slack.com/t/energyscopecommunity/shared_invite/zt-235qev7qb-Gx1Jpr3BucKjN1Ny5LlusQ) forum for discussions and help.
- **Contact Us:** Reach out via our [contact page](https://join.slack.com/t/energyscopecommunity/shared_invite/zt-235qev7qb-Gx1Jpr3BucKjN1Ny5LlusQ).


- **Documentation:** Check out the [EnergyScope Documentation](../explanation/index.md).
- **Community Support:** [Join our community](https://join.slack.com/t/energyscopecommunity/shared_invite/zt-235qev7qb-Gx1Jpr3BucKjN1Ny5LlusQ) forum for discussions and help.
- **Contact Us:** Reach out via our [contact page](https://join.slack.com/t/energyscopecommunity/shared_invite/zt-235qev7qb-Gx1Jpr3BucKjN1Ny5LlusQ).
