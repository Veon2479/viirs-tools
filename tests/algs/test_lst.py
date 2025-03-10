from __future__ import annotations

from tests.algs.utils import IMAGE_SHAPE, get_data_np, get_data_xr
from viirs_tools.algs import index, lst


class TestLst:
    def test_smoke_np(self):
        def _test(shape: tuple[int, ...]):
            ri1, ri2, _, _, bi05 = get_data_np(shape)
            ndvi = index.ndvi(ri2, ri1)
            lst.mono_window_i05(bi05, ndvi)

        _test(IMAGE_SHAPE)
        _test((2, *IMAGE_SHAPE))

    def test_smoke_xr(self):
        def _test(shape: tuple[int, ...]):
            ri1, ri2, _, _, bi05 = get_data_xr(shape)
            ndvi = index.ndvi(ri2, ri1)
            lst.mono_window_i05(bi05, ndvi)

        _test(IMAGE_SHAPE)
        _test((2, *IMAGE_SHAPE))
