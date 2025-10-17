"""
Data loading utilities for linopy models.

This module handles loading and preprocessing data from various sources
(AMPL .dat files, JSON, CSV, etc.) into Python data structures suitable
for linopy model building.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Union
import pandas as pd
import numpy as np


@dataclass
class ModelData:
    """
    Container for model data (sets, parameters, time series).
    
    This class provides a unified interface for model data that can be
    loaded from various sources.
    """
    sets: dict[str, list] = field(default_factory=dict)
    parameters: dict[str, Union[pd.DataFrame, dict, float, int]] = field(default_factory=dict)
    time_series: dict[str, pd.DataFrame] = field(default_factory=dict)
    
    @classmethod
    def from_ampl_dat(cls, dat_files: list[Path]):
        """
        Parse AMPL .dat files and extract data.
        
        This is a placeholder implementation. In practice, you would either:
        1. Use amplpy to load the data and extract it
        2. Write a custom .dat file parser
        3. Pre-process .dat files into a more convenient format (JSON, pickle)
        
        Args:
            dat_files: List of paths to AMPL .dat files
            
        Returns:
            ModelData instance with loaded data
        """
        # TODO: Implement AMPL .dat file parsing
        # For now, return empty data structure
        raise NotImplementedError(
            "AMPL .dat parsing not yet implemented. "
            "Please use from_dict() with manually prepared data."
        )
    
    @classmethod
    def from_dict(cls, data_dict: dict):
        """
        Create ModelData from a dictionary.
        
        Expected structure:
        {
            'sets': {'TECHNOLOGIES': ['PV', 'WIND', ...], ...},
            'parameters': {'f_max': {'PV': 10, 'WIND': 5, ...}, ...},
            'time_series': {'demand': pd.DataFrame(...), ...}
        }
        
        Args:
            data_dict: Dictionary containing model data
            
        Returns:
            ModelData instance
        """
        return cls(
            sets=data_dict.get('sets', {}),
            parameters=data_dict.get('parameters', {}),
            time_series=data_dict.get('time_series', {})
        )
    
    @classmethod
    def from_json(cls, json_file: Union[str, Path]):
        """
        Load data from JSON file.
        
        Args:
            json_file: Path to JSON file
            
        Returns:
            ModelData instance
        """
        import json
        with open(json_file, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)
    
    def to_json(self, json_file: Union[str, Path]):
        """
        Save data to JSON file.
        
        Note: DataFrames are converted to dict format.
        
        Args:
            json_file: Path to output JSON file
        """
        import json
        
        # Convert DataFrames to serializable format
        data = {
            'sets': self.sets,
            'parameters': {},
            'time_series': {}
        }
        
        for key, value in self.parameters.items():
            if isinstance(value, pd.DataFrame):
                data['parameters'][key] = value.to_dict()
            else:
                data['parameters'][key] = value
        
        for key, value in self.time_series.items():
            data['time_series'][key] = value.to_dict()
        
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=2)


def create_toy_data() -> ModelData:
    """
    Create a simple toy dataset for testing.
    
    This creates a minimal energy system with:
    - 5 technologies (PV, Wind, Gas, Battery, Grid)
    - 3 layers (Electricity, Gas, End-use)
    - 24 time periods (1 day, hourly)
    
    Returns:
        ModelData instance with toy data
    """
    # Sets
    technologies = ['PV', 'WIND', 'GAS_PLANT', 'BATTERY', 'GRID']
    storage_tech = ['BATTERY']
    layers = ['ELECTRICITY', 'GAS', 'END_USE']
    periods = list(range(1, 25))  # 24 hours
    
    # Technology parameters
    f_max = {
        'PV': 10.0,
        'WIND': 5.0,
        'GAS_PLANT': 8.0,
        'BATTERY': 2.0,  # GWh storage capacity
        'GRID': 3.0
    }
    
    f_min = {tech: 0.0 for tech in technologies}
    
    # Investment costs (M€/GW)
    c_inv = {
        'PV': 100.0,
        'WIND': 150.0,
        'GAS_PLANT': 80.0,
        'BATTERY': 50.0,  # M€/GWh for storage
        'GRID': 10.0
    }
    
    # Maintenance costs (M€/GW/year)
    c_maint = {
        'PV': 2.0,
        'WIND': 3.0,
        'GAS_PLANT': 5.0,
        'BATTERY': 1.0,
        'GRID': 0.5
    }
    
    # Operating costs for resources (M€/GWh)
    c_op = {
        'GAS': 50.0,
        'GRID': 100.0
    }
    
    # Layers in/out matrix
    # Positive = output, Negative = input
    layers_in_out = pd.DataFrame({
        'PV': {'ELECTRICITY': 1.0, 'GAS': 0.0, 'END_USE': 0.0},
        'WIND': {'ELECTRICITY': 1.0, 'GAS': 0.0, 'END_USE': 0.0},
        'GAS_PLANT': {'ELECTRICITY': 0.4, 'GAS': -1.0, 'END_USE': 0.0},  # 40% efficiency
        'BATTERY': {'ELECTRICITY': 0.0, 'GAS': 0.0, 'END_USE': 0.0},  # Storage handled separately
        'GRID': {'ELECTRICITY': -1.0, 'GAS': 0.0, 'END_USE': 1.0},  # Grid delivers to end-use
    }).T
    
    # Capacity factors (time-varying)
    # Simplified: PV has solar pattern, Wind is constant, rest are dispatchable
    c_p_t = pd.DataFrame({
        'PV': [0.0]*6 + [0.1, 0.3, 0.5, 0.7, 0.8, 0.9, 0.9, 0.8, 0.7, 0.5, 0.3, 0.1] + [0.0]*6,
        'WIND': [0.6]*24,
        'GAS_PLANT': [1.0]*24,
        'BATTERY': [1.0]*24,
        'GRID': [1.0]*24,
    }, index=periods)
    
    # Demand time series (GW)
    demand = pd.Series([
        0.5, 0.4, 0.4, 0.4, 0.5, 0.6,  # Night/early morning
        0.8, 1.0, 1.2, 1.3, 1.4, 1.5,  # Morning/midday
        1.4, 1.3, 1.2, 1.3, 1.5, 1.8,  # Afternoon/evening peak
        1.6, 1.4, 1.2, 1.0, 0.8, 0.6   # Evening/night
    ], index=periods, name='END_USE')
    
    # Storage parameters
    storage_efficiency = {'BATTERY': 0.9}  # Round-trip efficiency
    storage_charge_eff = {'BATTERY': 0.95}
    storage_discharge_eff = {'BATTERY': 0.95}
    
    # Other parameters
    i_rate = 0.05  # 5% discount rate
    lifetime = {tech: 25.0 for tech in technologies}
    lifetime['BATTERY'] = 15.0
    
    return ModelData(
        sets={
            'TECHNOLOGIES': technologies,
            'STORAGE_TECH': storage_tech,
            'LAYERS': layers,
            'PERIODS': periods,
        },
        parameters={
            'f_max': f_max,
            'f_min': f_min,
            'c_inv': c_inv,
            'c_maint': c_maint,
            'c_op': c_op,
            'layers_in_out': layers_in_out,
            'c_p_t': c_p_t,
            'storage_efficiency': storage_efficiency,
            'storage_charge_eff': storage_charge_eff,
            'storage_discharge_eff': storage_discharge_eff,
            'i_rate': i_rate,
            'lifetime': lifetime,
        },
        time_series={
            'demand': demand,
        }
    )

