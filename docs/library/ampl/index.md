# AMPL Reference

## General

This AMPL reference serves as a comprehensive reference for the EnergyScope AMPL model, providing detailed information to facilitate understanding, usage, and further development of the model.

The documentation is divided into three main sections:

- **Sets:** Defines the fundamental indices (e.g., time periods, sectors, end-uses, resources, and technologies) that form the basic structure of the model.
- **Parameters:** Presents the input data and model attributes (e.g., demand values, costs, availability, efficiencies, and emission factors) that are used within the model equations.
- **Variables:** Describes the model decision variables that are optimized (e.g., installed capacities, operation levels, costs, and shares).

Each section includes descriptions, domains, default values, bounds, units, and relevant relationships to support clarity and ease of navigation.

## About AMPL

**AMPL (A Mathematical Programming Language)** is a powerful and versatile language designed for describing and solving high-complexity optimization problems. It is widely used in operations research, economics, and engineering for modeling linear, nonlinear, and integer programming problems.

### What is AMPL?

AMPL provides a flexible environment for defining optimization models in a clear and concise manner. It separates the model (the mathematical formulation) from the data (the numerical values), allowing for easy modification and scalability. AMPL supports a wide range of problem types, including:

- **Linear Programming (LP)**
- **Integer Programming (IP)**
- **Nonlinear Programming (NLP)**
- **Mixed-Integer Nonlinear Programming (MINLP)**

EnergyScope is formulated either as **Mixed-Integer Programming (MILP)** or **Linear Programming (LP)** problem.

### How is AMPL Built?

AMPL is built upon a robust architecture that includes:

1. **Modeling Language:** Allows users to define variables, parameters, sets, and constraints using intuitive mathematical syntax.
2. **Solver Interface:** Connects with various optimization solvers (e.g., CPLEX, Gurobi, MINOS) to compute solutions efficiently.
3. **Data Management:** Facilitates the input of data through separate data files, enhancing modularity and ease of updates.
4. **Scripting and Automation:** Supports automation through scripting, enabling batch processing and iterative model adjustments.

### Learn More

For a comprehensive guide on using AMPL, refer to the official [AMPL Book](https://ampl.com/learn/ampl-book/). This resource provides in-depth tutorials, examples, and best practices to help you master AMPL for your optimization needs.

## EnergyScope AMPL Standards

To maintain consistency, readability, and ease of maintenance within the EnergyScope AMPL model, the following naming conventions and standards are established:

### Naming Conventions

#### Sets: 
  - **Format:** Full uppercase letters.  
  - **Example:** `PERIODS`, `SECTORS`, `RESOURCES`  
  - **Purpose:** Clearly distinguishes sets from parameters and variables, enhancing readability and reducing ambiguity.

#### Parameters:  
  - **Format:** Lowercase letters with underscores.  
  - **Example:** `end_uses_demand_year`, `c_inv`, `f_max`  
  - **Purpose:** Differentiates parameters from sets and variables, facilitating quick identification of data inputs and model attributes.

#### Variables:  
  - **Format:** Capitalized words with underscores.  
  - **Example:** `End_Uses`, `F_Mult`, `TotalCost`  
  - **Purpose:** Highlights decision variables that the model optimizes, making them easily identifiable within the model equations.