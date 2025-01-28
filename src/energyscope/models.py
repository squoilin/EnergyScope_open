import pathlib
from importlib.resources import files
from os import PathLike
from typing import Union, List, Tuple
import tempfile
import shutil

from energyscope import data  # Ensure 'data' is correctly imported
import amplpy


# Define the Model class first without importing it
class Model:
    def __init__(self, file_sequence: List[Tuple[str, Union[str, PathLike]]]):
        """
        Initializes the Model class with an ordered list of files to load.

        Parameters:
            file_sequence (List[Tuple[str, Union[str, PathLike]]]):
                A list of tuples where each tuple contains the file type ('mod' or 'dat')
                and the file path.
        """
        self.file_sequence = file_sequence
        self.temp_dir = tempfile.mkdtemp(prefix="model_files_")
        self.main_mod_path = pathlib.Path(self.temp_dir) / "main.mod"
        self._generate_main_mod()
        self.mod_files = [str(self.main_mod_path)]
        self.dat_files = []  # No separate dat_files needed

    def _generate_main_mod(self):
        """
        Generates a main.mod file that includes other mod files and executes dat files
        in the specified order.
        """
        with open(self.main_mod_path, 'w') as f:
            first_mod = True
            for file_type, file_path in self.file_sequence:
                file_path = str(file_path)
                if file_type == 'mod':
                    if first_mod:
                        f.write(f'model "{file_path}";\n')
                        first_mod = False
                    else:
                        f.write(f'include "{file_path}";\n')
                elif file_type == 'dat':
                    f.write(f'data "{file_path}";\n')
                else:
                    raise ValueError(f"Unknown file type '{file_type}'. Only 'mod' and 'dat' are supported.")
        # Removed the print statement to eliminate the generation message
        # print(f"Generated main.mod at {self.main_mod_path}")

    def cleanup(self):
        """
        Cleans up the temporary directory and files created.
        """
        shutil.rmtree(self.temp_dir)
        # Optionally remove or comment out the print statement if desired
        # print(f"Cleaned up temporary directory {self.temp_dir}")

    def __del__(self):
        """
        Ensures that temporary files are cleaned up when the Model instance is deleted.
        """
        self.cleanup()

def __from_data(path) -> pathlib.Path:
    return files(data).joinpath('datasets').joinpath(path)


def __from_model(path) -> pathlib.Path:
    return files(data).joinpath('models').joinpath(path)


# Initialize other Model instances with ordered file sequences

monthly = Model(
    file_sequence=[
        ('mod', __from_model("monthly.mod")),
        ('dat', __from_data("monthly.dat")),
    ]
)

transition = Model(
    file_sequence=[
        ('mod', __from_model("transition.mod")),
        ('dat', __from_data("transition.dat")),
    ]
)

typical_days = Model(
    file_sequence=[
        ('mod', __from_model("typical_days.mod")),
        ('dat', __from_data("typical_days.dat")),
    ]
)

infrastructure_ch_2050 = Model(
    file_sequence=[
        ('mod', __from_model("infrastructure/switzerland/ses_main.mod")),
        ('dat', __from_data("infrastructure/switzerland/2050/data.dat")),
        ('dat', __from_data("infrastructure/switzerland/2050/techs.dat")),
    ]
)

infrastructure_qc_2020 = Model(
    file_sequence=[
        ('mod', __from_model("infrastructure/quebec/QC_es_main.mod")),
        ('dat', __from_data("infrastructure/quebec/2020/QC_data.dat")),
        ('dat', __from_data("infrastructure/quebec/2020/techs_B2D.dat")),
        ('dat', __from_data("infrastructure/quebec/2020/mob_techs_dist_B2D.dat")),
        ('dat', __from_data("infrastructure/quebec/2020/mob_params.dat")),
    ]
)

lca_qc_2020 = Model(
    file_sequence=[
        ('mod', __from_model("infrastructure/quebec/QC_es_main.mod")),
        ('dat', __from_data("infrastructure/quebec/2020/QC_data.dat")),
        ('dat', __from_data("infrastructure/quebec/2020/techs_B2D.dat")),
        ('dat', __from_data("infrastructure/quebec/2020/mob_techs_dist_B2D.dat")),
        ('dat', __from_data("infrastructure/quebec/2020/mob_params.dat")),
        ('dat', __from_data("lca/quebec/2020/techs_lcia.dat")),
        ('mod', __from_model("lca/objectives.mod")),
    ]
)

lca_ch_2020 = Model(
    file_sequence=[
        ('mod', __from_model("lca/ch/ses_main.mod")),
        ('dat', __from_data("lca/ch/data.dat")),
        ('dat', __from_data("lca/ch/techs.dat")),
        ('dat', __from_data("lca/ch/techs_mob.dat")),
        ('dat', __from_data("lca/ch/techs_pv.dat")),
        ('dat', __from_data("lca/ch/techs_lcia_JS.dat")),
        ('mod', __from_model("lca/ch/scenarios.mod")),
        ('mod', __from_model("lca/ch/objectives.mod")),
    ]
)



