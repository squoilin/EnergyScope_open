"""
Result parser for linopy models.

Converts linopy model solutions into EnergyScope Result format
for compatibility with existing analysis and plotting tools.
"""

import pandas as pd
import numpy as np
from energyscope.result import Result


def parse_linopy_result(linopy_model, data, id_run=None) -> Result:
    """
    Convert linopy model solution to EnergyScope Result format.
    
    Args:
        linopy_model: Solved linopy.Model instance
        data: ModelData instance used to build the model
        id_run: Optional run ID for multi-run scenarios
        
    Returns:
        Result instance compatible with EnergyScope analysis tools
    """
    # Check if model has been solved
    if linopy_model.solution is None or linopy_model.solution.empty:
        raise ValueError("Model has not been solved or solution is empty")
    
    # Extract variables
    variables = {}
    for var_name in linopy_model.variables:
        var = linopy_model.variables[var_name]
        # Convert to DataFrame
        df = var.solution.to_pandas()
        
        # Ensure it's a DataFrame (not Series) and has consistent structure
        if isinstance(df, pd.Series):
            df = df.to_frame(name=var_name)
        
        # Reset index to match AMPL output format
        df = df.reset_index()
        
        # Rename index columns to match AMPL convention (index0, index1, etc.)
        index_cols = [col for col in df.columns if col != var_name]
        rename_map = {col: f'index{i}' for i, col in enumerate(index_cols)}
        df = df.rename(columns=rename_map)
        
        # Set the multi-index back
        if len(index_cols) > 0:
            df = df.set_index(list(rename_map.values()))
        
        variables[var_name] = df
    
    # Extract objective value
    objectives = {
        'TotalCost': pd.DataFrame({
            'TotalCost': [linopy_model.objective.value]
        })
    }
    
    # Extract parameters from data (these are input parameters, not computed)
    parameters = {}
    for param_name, param_value in data.parameters.items():
        if isinstance(param_value, pd.DataFrame):
            parameters[param_name] = param_value.copy()
        elif isinstance(param_value, dict):
            # Convert dict to DataFrame
            df = pd.Series(param_value, name=param_name).to_frame()
            df.index.name = 'index0'
            parameters[param_name] = df
        else:
            # Scalar parameter
            parameters[param_name] = pd.DataFrame({param_name: [param_value]})
    
    # Extract sets
    sets = data.sets.copy()
    
    # Add Run column if id_run is specified
    if id_run is not None:
        for df in objectives.values():
            df['Run'] = id_run
        for df in variables.values():
            df['Run'] = id_run
        for df in parameters.values():
            df['Run'] = id_run
    
    return Result(
        objectives=objectives,
        variables=variables,
        parameters=parameters,
        sets=sets
    )


def compare_results(result_ampl: Result, result_linopy: Result, rtol=1e-4, atol=1e-6):
    """
    Compare AMPL and linopy results for verification.
    
    Args:
        result_ampl: Result from AMPL solve
        result_linopy: Result from linopy solve
        rtol: Relative tolerance for numerical comparison
        atol: Absolute tolerance for numerical comparison
        
    Returns:
        dict with comparison results and any discrepancies
    """
    comparison = {
        'objectives': {},
        'variables': {},
        'success': True,
        'messages': []
    }
    
    # Compare objectives
    for obj_name in result_ampl.objectives.keys():
        if obj_name not in result_linopy.objectives:
            comparison['success'] = False
            comparison['messages'].append(f"Objective {obj_name} missing in linopy result")
            continue
        
        val_ampl = result_ampl.objectives[obj_name].iloc[0, 0]
        val_linopy = result_linopy.objectives[obj_name].iloc[0, 0]
        
        rel_diff = abs(val_ampl - val_linopy) / (abs(val_ampl) + atol)
        
        comparison['objectives'][obj_name] = {
            'ampl': val_ampl,
            'linopy': val_linopy,
            'relative_difference': rel_diff,
            'match': rel_diff < rtol
        }
        
        if rel_diff >= rtol:
            comparison['success'] = False
            comparison['messages'].append(
                f"Objective {obj_name}: relative difference {rel_diff:.6f} exceeds tolerance {rtol}"
            )
    
    # Compare variables
    for var_name in result_ampl.variables.keys():
        if var_name not in result_linopy.variables:
            comparison['success'] = False
            comparison['messages'].append(f"Variable {var_name} missing in linopy result")
            continue
        
        df_ampl = result_ampl.variables[var_name].sort_index()
        df_linopy = result_linopy.variables[var_name].sort_index()
        
        # Get the value column (should be the first non-index column)
        val_col_ampl = [c for c in df_ampl.columns if c != 'Run'][0]
        val_col_linopy = [c for c in df_linopy.columns if c != 'Run'][0]
        
        vals_ampl = df_ampl[val_col_ampl].values
        vals_linopy = df_linopy[val_col_linopy].values
        
        if vals_ampl.shape != vals_linopy.shape:
            comparison['success'] = False
            comparison['messages'].append(
                f"Variable {var_name}: shape mismatch {vals_ampl.shape} vs {vals_linopy.shape}"
            )
            continue
        
        # Compute element-wise relative differences
        abs_diff = np.abs(vals_ampl - vals_linopy)
        rel_diff = abs_diff / (np.abs(vals_ampl) + atol)
        max_rel_diff = np.max(rel_diff)
        
        comparison['variables'][var_name] = {
            'max_relative_difference': max_rel_diff,
            'mean_relative_difference': np.mean(rel_diff),
            'match': max_rel_diff < rtol
        }
        
        if max_rel_diff >= rtol:
            comparison['success'] = False
            comparison['messages'].append(
                f"Variable {var_name}: max relative difference {max_rel_diff:.6f} exceeds tolerance {rtol}"
            )
    
    return comparison

