from enum import Enum
from typing import Callable, Dict, Optional, Type, TypeVar

from viirs_tools.algs import cloud, index, lst, night, utils, water
from viirs_tools.utils.types import AlgEnum


class ALGS_CLOUD(AlgEnum):
    VIBCM_DAY = "ALGS_CLOUD.VIBCM_DAY: VIIRS I-Band Cloud Mask, day time"
    VIFCM_DAY = "ALGS_CLOUD.VIFCM: VIIRS Active Fire Cloud Mask, day time"
    VIFCM_NIGHT = "ALGS_CLOUD.VIFCM: VIIRS Active Fire Cloud Mask, night time"


class ALGS_INDEX(AlgEnum):
    NDVI = "ALGS_INDEX.NDVI: NDVI, day time"


class ALGS_LST(AlgEnum):
    MONO_WINDOW_I05 = "ALGS_LST.MONO_WINDOW_I05: Mono-window at I05 band, day time"
    MONO_WINDOW_M15 = "ALGS_LST.MONO_WINDOW_M15: Mono-window at M15 band, day time"
    MONO_WINDOW_M16 = "ALGS_LST.MONO_WINDOW_M16: Mono-window at M16 band, day time"


class ALGS_NIGHT(AlgEnum):
    NAIVE = "ALGS_NIGHT.NAIVE: Naive, any time"


class ALGS_WATER(AlgEnum):
    WBODIES_DAY = "ALGS_WATER.WBODIES_DAY: Water bodies, day time"


class ALGS_UTILS(AlgEnum):
    MERGE_DAY_NIGHT = "ALGS_UTILS.MERGE_DAY_NIGHT: Merge data by day-night mask"


class Runner:
    _IMPL_ALGS_INDEX = {ALGS_INDEX.NDVI: index.ndvi}
    _IMPL_ALGS_NIGHT = {ALGS_NIGHT.NAIVE: night.naive}
    _IMPL_ALGS_CLOUD = {ALGS_CLOUD.VIBCM_DAY: cloud.vibcm_day,
                        ALGS_CLOUD.VIFCM_DAY: cloud.vifcm_day,
                        ALGS_CLOUD.VIFCM_NIGHT: cloud.vifcm_night}
    _IMPL_ALGS_LST = {ALGS_LST.MONO_WINDOW_I05: lst.mono_window_i05,
                      ALGS_LST.MONO_WINDOW_M15: lst.mono_window_m15,
                      ALGS_LST.MONO_WINDOW_M16: lst.mono_window_m16}
    _IMPL_ALGS_WATER = {ALGS_WATER.WBODIES_DAY: water.water_bodies_day}
    _IMPL_ALGS_UTILS = {ALGS_UTILS.MERGE_DAY_NIGHT: utils.merge_day_night}

    def __init__(self):
        pass

    def _show_algs(self, algs: Dict[Enum, Callable]):
        print("<Key>: <Description>")
        for key in algs.keys():
            print(key.value)

    def show_algs_index(self):
        _show_algs(Runner._IMPL_ALGS_INDEX)

    def show_algs_night(self):
        _show_algs(Runner._IMPL_ALGS_NIGHT)

    def show_algs_cloud(self):
        _show_algs(Runner._IMPL_ALGS_CLOUD)

    def show_algs_lst(self):
        _show_algs(Runner._IMPL_ALGS_LST)

    def show_algs_water(self):
        _show_algs(Runner._IMPL_ALGS_WATER)

    def show_algs_utils(self):
        _show_algs(Runner._IMPL_ALGS_UTILS)

    def _get_alg(self, impls, algs, alg=None) -> Callable:
        if alg is None:
            alg = list(algs)[0]
        return impls[alg]

    def get_alg_index(self, alg: Optional[ALGS_INDEX] = None) -> Callable:
        return self._get_alg(Runner._IMPL_ALGS_INDEX, ALGS_INDEX, alg=alg)

    def get_alg_night(self, alg: Optional[ALGS_NIGHT] = None) -> Callable:
        return self._get_alg(Runner._IMPL_ALGS_NIGHT, ALGS_NIGHT, alg=alg)

    def get_alg_cloud(self, alg: Optional[ALGS_CLOUD] = None) -> Callable:
        return self._get_alg(Runner._IMPL_ALGS_CLOUD, ALGS_CLOUD, alg=alg)

    def get_alg_lst(self, alg: Optional[ALGS_LST] = None) -> Callable:
        return self._get_alg(Runner._IMPL_ALGS_LST, ALGS_LST, alg=alg)

    def get_alg_water(self, alg: Optional[ALGS_WATER] = None) -> Callable:
        return self._get_alg(Runner._IMPL_ALGS_WATER, ALGS_WATER, alg=alg)

    def get_alg_utils(self, alg: Optional[ALGS_UTILS] = None) -> Callable:
        return self._get_alg(Runner._IMPL_ALGS_UTILS, ALGS_UTILS, alg=alg)
