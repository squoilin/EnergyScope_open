# Energyscope Model Status Summary

This document provides a summary of the current status of the different Energyscope model implementations in this repository.

## 1. Conda Environment

*   **Name**: `dispaset`
*   **Status**: Ready to use.
*   **Activation**: `conda activate dispaset`

## 2. Model Implementations

### 2.1. AMPL Model

*   **Description**: The original implementation of the Energyscope model using AMPL.
*   **Main Implementation File(s)**: `scripts/ampl_model.py` (runner), `src/energyscope/data/models/core/td/ESTD_model_core.mod` (model logic).
*   **How to Run**: 
    ```bash
    conda activate dispaset
    python scripts/ampl_model.py
    ```
*   **Status**: **Ready**. The model runs successfully and solves with Gurobi, yielding an optimal solution.
*   **Remaining Work**: None. This model serves as the baseline for comparison.

### 2.2. Linopy Model (Non-Vectorized)

*   **Description**: A direct translation of the AMPL model to `linopy`, using loops to build constraints. This version is expected to be functional but inefficient.
*   **Main Implementation File(s)**: `src/energyscope/linopy_backend/toy_model.py` (toy model), `src/energyscope/linopy_backend/core_model.py` (core model).
*   **How to Run**: The model can be tested with two different datasets:
    *   **Toy Model**: A small, simplified dataset for quick tests.
        ```bash
        conda activate dispaset
        python scripts/linopy_model.py
        ```
    *   **Core Model**: A more comprehensive dataset that tests all constraint groups.
        ```bash
        conda activate dispaset
        python scripts/test_build_core_model.py
        ```
*   **Status**: **Ready**. Both the toy and core model versions run successfully and solve to optimality. The implementation is functional, though likely slow for large-scale problems.
*   **Remaining Work**: While functional, this version is not optimized for performance. The primary remaining work is to complete the vectorized implementation.

### 2.3. Linopy Model (Vectorized with xarray)

*   **Description**: An optimized version of the `linopy` model that uses `xarray` to build constraints in a vectorized manner, avoiding inefficient loops.
*   **Main Implementation File(s)**: `src/energyscope/linopy_backend/core_model_xarray.py`.
*   **How to Run**:
    ```bash
    conda activate dispaset
    python scripts/test_core_model_xarray.py --full
    ```
*   **Status**: **Incomplete/Not Working**. 
    *   The model's constraint groups can be built and tested *individually*, and they all pass.
    *   However, when the **full model** is assembled, the solver (HiGHS) fails with a numerical stability error (`LP matrix packed vector contains... values... greater than 1e+15`).
    *   This indicates that while the individual components are likely correct, their integration creates a numerically unstable constraint matrix.
*   **Remaining Work**:
    *   **Debug Numerical Stability**: The primary task is to identify which constraint(s) or combination of constraints are causing the large values in the matrix and refactor them. This may involve rescaling variables or reformulating constraints.
    *   **Complete Implementation**: Some constraint groups (e.g., GWP, mobility) are not fully tested due to a lack of data in the minimal test set. The model needs to be tested with a complete dataset.
    *   **Validation**: Once the model solves, its results must be validated against the AMPL and non-vectorized `linopy` versions to ensure correctness.

## 3. Objective Function Comparison

The following table summarizes the objective function values obtained from the models that solve successfully.

**Important Note**: The objective values below are **not directly comparable** because each model was run with a different dataset. The AMPL model uses the full "ESTD" dataset, while the Linopy models use small, synthetic datasets created specifically for testing purposes. A proper validation would require the Linopy models to be run with the full ESTD dataset.

| Model                             | Dataset          | Objective Value     | Notes                               |
| --------------------------------- | ---------------- | ------------------- | ----------------------------------- |
| AMPL                              | Full (ESTD)      | 47572.11            | Baseline result with full dataset.  |
| Linopy (Non-Vectorized)           | Toy              | 2548.52 M€          | Solves with a small, synthetic dataset. |
| Linopy (Non-Vectorized)           | Minimal Core     | 45.47 M€            | Solves with a minimal, synthetic dataset. |
| Linopy (Vectorized with `xarray`) | Minimal Core     | 0.0                 | **Solver failed** (numerical issues). |
