import pathlib
from importlib.resources import files
from os import PathLike
from typing import Union

from energyscope import data


class Model:
    def __init__(self, mod_files: list[Union[str, PathLike]], dat_files: list[Union[str, PathLike]]):
        self.mod_files = mod_files
        self.dat_files = dat_files or []


def __from_data(path) -> pathlib.Path:
    return files(data).joinpath('datasets').joinpath(path)


def __from_model(path) -> pathlib.Path:
    return files(data).joinpath('models').joinpath(path)


monthly = Model(mod_files=[__from_model("monthly.mod")], dat_files=[__from_data("monthly.dat")])
transition = Model(mod_files=[__from_model("transition.mod")], dat_files=[__from_data("transition.dat")])
typical_days = Model(mod_files=[__from_model("typical_days.mod")], dat_files=[__from_data("typical_days.dat")])

infrastructure_ch_2050 = Model(mod_files=[__from_model("infrastructure/switzerland/ses_main.mod")],
                               dat_files=[__from_data("infrastructure/switzerland/2050/data.dat"),
                                          __from_data("infrastructure/switzerland/2050/techs.dat")])

infrastructure_qc_2020 = Model(mod_files=[__from_model("infrastructure/quebec/QC_es_main.mod")],
                               dat_files=[__from_data("infrastructure/quebec/2020/QC_data.dat"),
                                          __from_data("infrastructure/quebec/2020/techs_B2D.dat"),
                                          __from_data("infrastructure/quebec/2020/mob_techs_dist_B2D.dat"),
                                          __from_data("infrastructure/quebec/2020/mob_params.dat")])

lca_ch_2050 = Model(mod_files=[__from_model("infrastructure/switzerland/ses_main.mod"),
                               __from_model("lca/objectives.mod")],
                    dat_files=[__from_data("infrastructure/switzerland/2050/data.dat"),
                               __from_data("infrastructure/switzerland/2050/techs.dat"),
                               __from_data("lca/switzerland/2020/techs_lcia.dat")])

lca_qc_2020 = Model(mod_files=[__from_model("infrastructure/quebec/QC_es_main.mod"),
                               __from_model("lca/objectives.mod")],
                    dat_files=[__from_data("infrastructure/quebec/2020/QC_data.dat"),
                               __from_data("infrastructure/quebec/2020/techs_B2D.dat"),
                               __from_data("infrastructure/quebec/2020/mob_techs_dist_B2D.dat"),
                               __from_data("infrastructure/quebec/2020/mob_params.dat"),
                               __from_data("lca/quebec/2020/techs_lcia.dat")])
