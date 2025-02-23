import numpy as np
import pytest

from tests.algs.utils import (
    IMAGE_SHAPE,
    get_data_np,
    get_data_xr,
    get_np_from_list,
    get_np_seq_from_list,
    get_xr_from_list,
    get_xr_seq_from_list,
)
from viirs_tools.algs import water


class TestWaterBodiesDay:
    def test_smoke_np(self):
        def _test(shape: tuple[int, ...]):
            ri1, ri2, ri3, _, _ = get_data_np(shape)
            water.water_bodies_day(ri1, ri2, ri3)

        _test(IMAGE_SHAPE)
        _test((2, *IMAGE_SHAPE))

    def test_smoke_xr(self):
        def _test(shape: tuple[int, ...]):
            ri1, ri2, ri3, _, _ = get_data_xr(shape)
            water.water_bodies_day(ri1, ri2, ri3)

        _test(IMAGE_SHAPE)
        _test((2, *IMAGE_SHAPE))

    @pytest.mark.parametrize(
        ("ri1", "ri2", "ri3", "expected"),
        [
            (
                # ri1
                [np.nan, 50, 20],
                # ri2
                [np.nan, 40, 40],
                # ri3
                [np.nan, 20, 50],
                # expected
                [np.nan, 0, 1],
            )
        ],
    )
    def test_alg(self, ri1, ri2, ri3, expected):
        mask = water.water_bodies_day(get_np_from_list(ri1), get_np_from_list(ri2), get_np_from_list(ri3))
        assert np.allclose(mask, get_np_from_list(expected), equal_nan=True)

        mask = water.water_bodies_day(get_np_seq_from_list(ri1), get_np_seq_from_list(ri2), get_np_seq_from_list(ri3))
        assert np.allclose(mask, get_np_seq_from_list(expected), equal_nan=True)

        mask = water.water_bodies_day(get_xr_from_list(ri1), get_xr_from_list(ri2), get_xr_from_list(ri3))
        assert mask.equals(get_xr_from_list(expected))

        mask = water.water_bodies_day(get_xr_seq_from_list(ri1), get_xr_seq_from_list(ri2), get_xr_seq_from_list(ri3))
        assert mask.equals(get_xr_seq_from_list(expected))
