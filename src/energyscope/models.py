import pathlib
from dataclasses import dataclass
from importlib.resources import files as resources_files
from os import PathLike
from typing import Union, Callable

from energyscope import data  # Ensure 'data' is correctly imported


# Define the Model class first without importing it
@dataclass
class Model:
    def __init__(self, files: list[tuple[str, Union[str, PathLike]]]):
        """
        Initializes the Model class with an ordered list of files to load.

        Parameters:
            files (list[tuple[str, Union[str, PathLike]]]):
                A list of tuples where each tuple contains the file type ('mod' or 'dat')
                and the file path.
        """
        self.files = files
        self.backend = 'ampl'

    def __add__(self, other):
        return Model(self.files + other.files)


@dataclass
class LinopyModel:
    """
    Model definition for linopy-based optimization.
    
    Attributes:
        builder: Function that takes ModelData and returns a linopy.Model
        data_loader: Function that returns ModelData (or takes Dataset and returns ModelData)
        backend: Always 'linopy' to distinguish from AMPL models
    """
    def __init__(self, builder: Callable, data_loader: Callable):
        """
        Initializes a LinopyModel.
        
        Parameters:
            builder: Callable that takes ModelData and returns linopy.Model
            data_loader: Callable that returns ModelData instance
        """
        self.builder = builder
        self.data_loader = data_loader
        self.backend = 'linopy'


def __from_data(path) -> pathlib.Path:
    return resources_files(data).joinpath('datasets').joinpath(path)


def __from_model(path) -> pathlib.Path:
    return resources_files(data).joinpath('models').joinpath(path)


# Initialize other Model instances with ordered file sequences

monthly = Model([('mod', __from_model("monthly.mod")), ('dat', __from_data("monthly.dat")), ])

transition = Model([('mod', __from_model("transition.mod")), ('dat', __from_data("transition.dat")), ])

typical_days = Model([('mod', __from_model("typical_days.mod")), ('dat', __from_data("typical_days.dat")), ])

core = Model([('mod', __from_model("core/td/ESTD_model_core.mod")),
                                ('dat', __from_data("core/td/ESTD_12TD.dat")),
                                ('dat', __from_data("core/td/ESTD_data_core.dat")), ])

infrastructure_ch_2050 = Model([('mod', __from_model("infrastructure/switzerland/ses_main.mod")),
                                ('dat', __from_data("infrastructure/switzerland/2050/data.dat")),
                                ('dat', __from_data("infrastructure/switzerland/2050/techs.dat")), ])

infrastructure_qc_2020 = Model([('mod', __from_model("infrastructure/quebec/QC_es_main.mod")),
                                ('dat', __from_data("infrastructure/quebec/2020/QC_data.dat")),
                                ('dat', __from_data("infrastructure/quebec/2020/techs_B2D.dat")),
                                ('dat', __from_data("infrastructure/quebec/2020/mob_techs_dist_B2D.dat")),
                                ('dat', __from_data("infrastructure/quebec/2020/mob_params.dat")), ])

lca_qc_2020 = Model([('mod', __from_model("infrastructure/quebec/QC_es_main.mod")),
                     ('dat', __from_data("infrastructure/quebec/2020/QC_data.dat")),
                     ('dat', __from_data("infrastructure/quebec/2020/techs_B2D.dat")),
                     ('dat', __from_data("infrastructure/quebec/2020/mob_techs_dist_B2D.dat")),
                     ('dat', __from_data("infrastructure/quebec/2020/mob_params.dat")),
                     ('dat', __from_data("lca/quebec/2020/techs_lcia.dat")),
                     ('mod', __from_model("lca/objectives.mod")), ])

lca_ch_2020 = Model([('mod', __from_model("lca/ch/ses_main.mod")), ('dat', __from_data("lca/ch/data.dat")),
                     ('dat', __from_data("lca/ch/techs.dat")), ('dat', __from_data("lca/ch/techs_mob.dat")),
                     ('dat', __from_data("lca/ch/techs_pv.dat")), ('dat', __from_data("lca/ch/techs_lcia_JS.dat")),
                     ('mod', __from_model("lca/ch/scenarios.mod")), ('mod', __from_model("lca/ch/objectives.mod")), ])

# Linopy models
try:
    from energyscope.linopy_backend import build_toy_model
    from energyscope.linopy_backend.data_loader import create_toy_data
    
    core_toy_linopy = LinopyModel(
        builder=build_toy_model,
        data_loader=create_toy_data
    )
except ImportError:
    # Linopy not installed, skip linopy models
    pass
