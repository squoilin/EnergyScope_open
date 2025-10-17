"""
Linopy backend for EnergyScope models.

This module provides an alternative backend to AMPL using linopy for
linear optimization modeling.
"""

from .result_parser import parse_linopy_result
from .data_loader import ModelData
from .toy_model import build_toy_model

__all__ = ['parse_linopy_result', 'ModelData', 'build_toy_model']

