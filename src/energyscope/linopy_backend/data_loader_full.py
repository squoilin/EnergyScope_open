"""
Data loader for converting full EnergyScope AMPL data to Python format.

This module reads the complete EnergyScope core model data from AMPL .dat files
and converts it into Python dictionaries and pandas DataFrames suitable for
the non-vectorized linopy core model.
"""

import os
import pandas as pd
from amplpy import AMPL, add_to_path
from dotenv import load_dotenv

def load_ampl_data():
    """
    Load EnergyScope core data using amplpy.
    
    Returns:
        AMPL instance with loaded data
    """
    load_dotenv()
    ampl_path = os.environ.get("AMPL_PATH")
    if ampl_path:
        add_to_path(ampl_path)
    
    ampl = AMPL()
    
    model_path = "src/energyscope/data/models/core/td/"
    data_path = "src/energyscope/data/datasets/core/td/"
    
    print("Loading AMPL model and data...")
    print(f"  Model: {model_path}ESTD_model_core.mod")
    print(f"  Data:  {data_path}ESTD_12TD.dat")
    print(f"  Data:  {data_path}ESTD_data_core.dat")
    
    ampl.read(model_path + "ESTD_model_core.mod")
    ampl.readData(data_path + "ESTD_12TD.dat")
    ampl.readData(data_path + "ESTD_data_core.dat")
    
    print("✓ AMPL data loaded successfully")
    return ampl

def extract_data_from_ampl(ampl):
    """
    Extracts sets and parameters from an AMPL instance into a Python dictionary.
    """
    print("\nExtracting data into Python format...")
    
    # Extract sets
    sets = {s[0]: list(s[1].members()) for s in ampl.getSets()}
    print(f"  ✓ Extracted {len(sets)} sets")

    # Extract parameters
    parameters = {}
    for param_tuple in ampl.getParameters():
        param_name = param_tuple[0]
        param_obj = param_tuple[1]
        try:
            df = param_obj.getValues().toPandas()
            if not df.empty:
                if df.index.nlevels > 1:
                    parameters[param_name] = df.squeeze()
                else:
                    series_or_scalar = df.squeeze()
                    if isinstance(series_or_scalar, pd.Series):
                        parameters[param_name] = series_or_scalar
                    else:
                        parameters[param_name] = df.iloc[0,0]
            else:
                # If getValues() is empty, it might be a scalar defined with 'default'
                try:
                    val = param_obj.value()
                    if val is not None:
                        parameters[param_name] = val
                    else:
                        print(f"  ⚠ Parameter '{param_name}' is empty and has no scalar value.")
                except Exception as e_val:
                    print(f"  ⚠ Could not retrieve scalar value for '{param_name}': {e_val}")

        except Exception as e:
            print(f"  ⚠ Could not process parameter '{param_name}' as DataFrame: {e}")
            # Fallback for parameters that are not indexed
            try:
                val = param_obj.value()
                if val is not None:
                    parameters[param_name] = val
                    print(f"  ✓ Extracted '{param_name}' as a scalar fallback.")
                else:
                     print(f"  ⚠ Parameter '{param_name}' could not be extracted.")
            except Exception as e_scalar:
                print(f"  ✗ Failed to extract '{param_name}' with any method: {e_scalar}")

    print(f"  ✓ Extracted {len(parameters)} parameters")

    # Assemble the final data dictionary
    data = {
        'sets': sets,
        'parameters': parameters,
        'time_series': {} # This can be populated if needed
    }
    
    # Special handling for T_H_TD which is a set of tuples
    t_h_td_set = ampl.getSet('T_H_TD')
    data['sets']['T_H_TD'] = [tuple(m) for m in t_h_td_set.members()]

    # Reconstruct t_op, which is a calculated parameter in AMPL
    print("  Reconstructing 't_op' parameter...")
    try:
        tds = data['sets']['TYPICAL_DAYS']
        hours = data['sets']['HOURS']
        t_op_data = {}

        if 'TYPICAL_DAYS_WEIGHT' in parameters:
            # Prefer using the weight parameter if it was extracted
            print("  Using 'TYPICAL_DAYS_WEIGHT' to build t_op.")
            td_weight = parameters['TYPICAL_DAYS_WEIGHT'].to_dict()
            for td_name, weight in td_weight.items():
                for h in hours:
                    td_index = tds.index(td_name) + 1 if isinstance(td_name, str) else td_name
                    t_op_data[(h, td_index)] = weight
        else:
            # Fallback to equal weights if the parameter is not found
            print("  'TYPICAL_DAYS_WEIGHT' not found. Falling back to equal weight distribution.")
            hours_in_year = 8760.0
            num_tds = len(tds)
            if num_tds > 0:
                weight = hours_in_year / (num_tds * len(hours))
                print(f"  Calculated equal weight: {weight:.2f}")
                for td in tds:
                    for h in hours:
                        td_index = tds.index(td) + 1 if isinstance(td, str) else td
                        t_op_data[(h, td_index)] = weight
        
        if t_op_data:
            t_op_series = pd.Series(t_op_data)
            t_op_series.index.names = ['hour', 'td']
            parameters['t_op'] = t_op_series
            print("  ✓ 't_op' successfully reconstructed.")
        else:
            print("  ⚠ 't_op' could not be reconstructed (no typical days?).")

    except Exception as e:
        print(f"  ✗ Failed to reconstruct 't_op': {e}")
        import traceback
        traceback.print_exc()

    return data

def create_full_dataset():
    """
    Loads and converts the full AMPL dataset for the linopy model.
    """
    ampl = load_ampl_data()
    data = extract_data_from_ampl(ampl)
    return data

if __name__ == '__main__':
    # For testing purposes
    print("="*70)
    print("Testing full data loader")
    print("="*70)
    full_data = create_full_dataset()
    print("\n" + "="*70)
    print("DATA LOADER SUMMARY")
    print("="*70)
    print(f"  Sets found: {len(full_data['sets'])}")
    print(f"  Parameters found: {len(full_data['parameters'])}")
    print(f"  Example set TECHNOLOGIES: {len(full_data['sets']['TECHNOLOGIES'])} members")
    print("✓ Data loading test complete.")
