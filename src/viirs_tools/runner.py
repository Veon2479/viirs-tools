from collections.abc import Callable
from enum import Enum
from types import MappingProxyType

from viirs_tools.algs import cloud, index, lst, night, utils, water
from viirs_tools.utils.types import AlgEnum


class AlgsCloud(AlgEnum):
    VIBCM_DAY = "AlgsCloud.VIBCM_DAY: VIIRS I-Band Cloud Mask, day time, [default]"
    VIFCM_DAY = "AlgsCloud.VIFCM: VIIRS Active Fire Cloud Mask, day time"
    VIFCM_NIGHT = "AlgsCloud.VIFCM: VIIRS Active Fire Cloud Mask, night time"


class AlgsIndex(AlgEnum):
    NDVI = "AlgsIndex.NDVI: NDVI, day time, [default]"
    NDSI = "AlgsIndex.NDSI: NDSI, day time"


class AlgsLST(AlgEnum):
    MONO_WINDOW_I05 = "AlgsLST.MONO_WINDOW_I05: Mono-window at I05 band, day time, [default]"
    MONO_WINDOW_M15 = "AlgsLST.MONO_WINDOW_M15: Mono-window at M15 band, day time"
    MONO_WINDOW_M16 = "AlgsLST.MONO_WINDOW_M16: Mono-window at M16 band, day time"


class AlgsNight(AlgEnum):
    NAIVE = "AlgsNight.NAIVE: Naive, any time, [default]"


class AlgsWater(AlgEnum):
    WBODIES_DAY = "AlgsWater.WBODIES_DAY: Water bodies, day time, [default]"


class AlgsUtils(AlgEnum):
    MERGE_DAY_NIGHT = "AlgsUtils.MERGE_DAY_NIGHT: Merge data by day-night mask, [default]"


class Runner:
    _IMPL_AlgsIndex = MappingProxyType({AlgsIndex.NDVI: index.ndvi, AlgsIndex.NDSI: index.ndsi})
    _IMPL_AlgsNight = MappingProxyType({AlgsNight.NAIVE: night.naive})
    _IMPL_AlgsCloud = MappingProxyType(
        {
            AlgsCloud.VIBCM_DAY: cloud.vibcm_day,
            AlgsCloud.VIFCM_DAY: cloud.vifcm_day,
            AlgsCloud.VIFCM_NIGHT: cloud.vifcm_night,
        }
    )
    _IMPL_AlgsLST = MappingProxyType(
        {
            AlgsLST.MONO_WINDOW_I05: lst.mono_window_i05,
            AlgsLST.MONO_WINDOW_M15: lst.mono_window_m15,
            AlgsLST.MONO_WINDOW_M16: lst.mono_window_m16,
        }
    )
    _IMPL_AlgsWater = MappingProxyType({AlgsWater.WBODIES_DAY: water.water_bodies_day})
    _IMPL_AlgsUtils = MappingProxyType({AlgsUtils.MERGE_DAY_NIGHT: utils.merge_day_night})

    _IMPLS = MappingProxyType(
        {
            AlgsIndex: _IMPL_AlgsIndex,
            AlgsNight: _IMPL_AlgsNight,
            AlgsCloud: _IMPL_AlgsCloud,
            AlgsLST: _IMPL_AlgsLST,
            AlgsWater: _IMPL_AlgsWater,
            AlgsUtils: _IMPL_AlgsUtils,
        }
    )

    def __init__(self):
        pass

    def _show_algs(self, algs: dict[Enum, Callable]):
        print("<Key>: <Description>")
        for item in algs.items():
            print(item)

    def show_algs_index(self):
        self._show_algs(Runner._IMPL_AlgsIndex)

    def show_algs_night(self):
        self._show_algs(Runner._IMPL_AlgsNight)

    def show_algs_cloud(self):
        self._show_algs(Runner._IMPL_AlgsCloud)

    def show_algs_lst(self):
        self._show_algs(Runner._IMPL_AlgsLST)

    def show_algs_water(self):
        self._show_algs(Runner._IMPL_AlgsWater)

    def show_algs_utils(self):
        self._show_algs(Runner._IMPL_AlgsUtils)

    def show_algs_all(self):
        for impl in Runner._IMPLS.values():
            self._show_algs(impl)
            print()

    def _get_alg(self, impls, algs, alg=None) -> Callable:
        if alg is None:
            alg = next(iter(algs))
        return impls[alg]

    def get_alg_index(self, alg: AlgsIndex | None = None) -> Callable:
        return self._get_alg(Runner._IMPL_AlgsIndex, AlgsIndex, alg=alg)

    def get_alg_night(self, alg: AlgsNight | None = None) -> Callable:
        return self._get_alg(Runner._IMPL_AlgsNight, AlgsNight, alg=alg)

    def get_alg_cloud(self, alg: AlgsCloud | None = None) -> Callable:
        return self._get_alg(Runner._IMPL_AlgsCloud, AlgsCloud, alg=alg)

    def get_alg_lst(self, alg: AlgsLST | None = None) -> Callable:
        return self._get_alg(Runner._IMPL_AlgsLST, AlgsLST, alg=alg)

    def get_alg_water(self, alg: AlgsWater | None = None) -> Callable:
        return self._get_alg(Runner._IMPL_AlgsWater, AlgsWater, alg=alg)

    def get_alg_utils(self, alg: AlgsUtils | None = None) -> Callable:
        return self._get_alg(Runner._IMPL_AlgsUtils, AlgsUtils, alg=alg)
