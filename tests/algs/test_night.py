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
from viirs_tools.algs import night


class TestNaive:
    def test_smoke_np(self):
        def _test(shape: tuple[int, ...]):
            ri1, _, _, bi4, _ = get_data_np(shape)
            night.naive(ri1, bi4)

        _test(IMAGE_SHAPE)
        _test((2, *IMAGE_SHAPE))

    def test_smoke_xr(self):
        def _test(shape: tuple[int, ...]):
            ri1, _, _, bi4, _ = get_data_xr(shape)
            night.naive(ri1, bi4)

        _test(IMAGE_SHAPE)
        _test((2, *IMAGE_SHAPE))

    @pytest.mark.parametrize(
        ("ref", "bt", "expected"),
        [
            (
                # ref
                [np.nan, np.nan, 20, 30],
                # bt
                [np.nan, 40, np.nan, 1],
                # expected
                [np.nan, 1, np.nan, 0],
            )
        ],
    )
    def test_alg(self, ref, bt, expected):
        mask = night.naive(get_np_from_list(ref), get_np_from_list(bt))
        assert np.allclose(mask, get_np_from_list(expected), equal_nan=True)

        mask = night.naive(get_np_seq_from_list(ref), get_np_seq_from_list(bt))
        assert np.allclose(mask, get_np_seq_from_list(expected), equal_nan=True)

        mask = night.naive(get_xr_from_list(ref), get_xr_from_list(bt))
        assert mask.equals(get_xr_from_list(expected))

        mask = night.naive(get_xr_seq_from_list(ref), get_xr_seq_from_list(bt))
        assert mask.equals(get_xr_seq_from_list(expected))
