"""
Tests for linopy backend implementation.

This module tests the toy model implementation and verifies that
the linopy backend produces sensible results.
"""

import pytest
import numpy as np
import pandas as pd

# Skip all tests if linopy is not installed
pytest.importorskip("linopy")

from energyscope.linopy_backend.data_loader import create_toy_data, ModelData
from energyscope.linopy_backend.toy_model import build_toy_model, solve_toy_model
from energyscope.linopy_backend.result_parser import parse_linopy_result


class TestToyModel:
    """Test suite for the toy model."""
    
    @pytest.fixture
    def toy_data(self):
        """Create toy data for testing."""
        return create_toy_data()
    
    def test_data_creation(self, toy_data):
        """Test that toy data is created correctly."""
        assert 'TECHNOLOGIES' in toy_data.sets
        assert 'LAYERS' in toy_data.sets
        assert 'PERIODS' in toy_data.sets
        
        assert len(toy_data.sets['TECHNOLOGIES']) == 5
        assert len(toy_data.sets['LAYERS']) == 3
        assert len(toy_data.sets['PERIODS']) == 24
        
        assert 'f_max' in toy_data.parameters
        assert 'c_inv' in toy_data.parameters
        assert 'demand' in toy_data.time_series
    
    def test_model_building(self, toy_data):
        """Test that model builds without errors."""
        model = build_toy_model(toy_data)
        
        assert model is not None
        assert 'F' in model.variables
        assert 'F_t' in model.variables
        assert model.objective is not None
    
    @pytest.mark.skipif(
        not pytest.config.getoption("--run-solver-tests", default=False),
        reason="Solver tests skipped (use --run-solver-tests to enable)"
    )
    def test_model_solving(self, toy_data):
        """Test that model solves successfully."""
        model, solution = solve_toy_model(toy_data, solver='highs')
        
        assert solution is not None
        assert solution.status == 'ok'
        assert model.objective.value > 0
    
    @pytest.mark.skipif(
        not pytest.config.getoption("--run-solver-tests", default=False),
        reason="Solver tests skipped (use --run-solver-tests to enable)"
    )
    def test_result_parsing(self, toy_data):
        """Test that results are parsed correctly."""
        model, solution = solve_toy_model(toy_data, solver='highs')
        result = parse_linopy_result(model, toy_data)
        
        # Check structure
        assert hasattr(result, 'variables')
        assert hasattr(result, 'objectives')
        assert hasattr(result, 'parameters')
        assert hasattr(result, 'sets')
        
        # Check variables
        assert 'F' in result.variables
        assert 'F_t' in result.variables
        
        # Check objective
        assert 'TotalCost' in result.objectives
        
        # Check that values are sensible
        F = result.variables['F']
        assert len(F) == 5  # 5 technologies
        assert (F['F'] >= 0).all()  # Non-negative capacities
    
    @pytest.mark.skipif(
        not pytest.config.getoption("--run-solver-tests", default=False),
        reason="Solver tests skipped (use --run-solver-tests to enable)"
    )
    def test_energy_balance(self, toy_data):
        """Test that energy balance is satisfied in solution."""
        model, solution = solve_toy_model(toy_data, solver='highs')
        result = parse_linopy_result(model, toy_data)
        
        # Get operation levels
        F_t = result.variables['F_t'].reset_index()
        demand = toy_data.time_series['demand']
        layers_in_out = toy_data.parameters['layers_in_out']
        
        # For each time period, check that supply >= demand
        for t in toy_data.sets['PERIODS']:
            # Get operation at time t
            ops_t = F_t[F_t['index1'] == t]
            
            # Calculate END_USE supply
            supply = 0
            for _, row in ops_t.iterrows():
                tech = row['index0']
                f_val = row['F_t']
                layer_coef = layers_in_out.loc[tech, 'END_USE']
                supply += f_val * layer_coef
            
            demand_val = demand.loc[t]
            
            # Supply should meet or exceed demand (within tolerance)
            assert supply >= demand_val - 1e-6, \
                f"At period {t}, supply {supply} < demand {demand_val}"


class TestModelData:
    """Test suite for ModelData class."""
    
    def test_from_dict(self):
        """Test creating ModelData from dictionary."""
        data_dict = {
            'sets': {'TECH': ['A', 'B']},
            'parameters': {'cost': {'A': 10, 'B': 20}},
            'time_series': {}
        }
        
        data = ModelData.from_dict(data_dict)
        
        assert data.sets['TECH'] == ['A', 'B']
        assert data.parameters['cost'] == {'A': 10, 'B': 20}
    
    def test_to_from_json(self, tmp_path):
        """Test JSON serialization."""
        # Create data
        data = create_toy_data()
        
        # Save to JSON
        json_file = tmp_path / "test_data.json"
        data.to_json(json_file)
        
        assert json_file.exists()
        
        # Load from JSON
        loaded_data = ModelData.from_json(json_file)
        
        assert loaded_data.sets['TECHNOLOGIES'] == data.sets['TECHNOLOGIES']
        assert loaded_data.parameters['f_max'] == data.parameters['f_max']


def pytest_addoption(parser):
    """Add command line options for pytest."""
    parser.addoption(
        "--run-solver-tests",
        action="store_true",
        default=False,
        help="Run tests that require solver"
    )


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])

