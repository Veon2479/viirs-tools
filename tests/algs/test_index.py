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
from viirs_tools.algs import index


class TestNdvi:
    def test_smoke_np(self):
        def _test(shape: tuple[int, ...]):
            ri1, ri2, _, _, _ = get_data_np(shape)
            index.ndvi(ri2, ri1)

        _test(IMAGE_SHAPE)
        _test((2, *IMAGE_SHAPE))

    def test_smoke_xr(self):
        def _test(shape: tuple[int, ...]):
            ri1, ri2, _, _, _ = get_data_xr(shape)
            index.ndvi(ri2, ri1)

        _test(IMAGE_SHAPE)
        _test((2, *IMAGE_SHAPE))

    @pytest.mark.parametrize(
        ("ri1", "ri2", "expected"),
        [
            (
                # ri1
                [np.nan, 5, 5],
                # ri2
                [np.nan, 5, 15],
                # expected
                [np.nan, 0, 0.5],
            )
        ],
    )
    def test_alg(self, ri1, ri2, expected):
        mask = index.ndvi(get_np_from_list(ri2), get_np_from_list(ri1))
        assert np.allclose(mask, get_np_from_list(expected), equal_nan=True)

        mask = index.ndvi(get_np_seq_from_list(ri2), get_np_seq_from_list(ri1))
        assert np.allclose(mask, get_np_seq_from_list(expected), equal_nan=True)

        mask = index.ndvi(get_xr_from_list(ri2), get_xr_from_list(ri1))
        assert mask.equals(get_xr_from_list(expected))

        mask = index.ndvi(get_xr_seq_from_list(ri2), get_xr_seq_from_list(ri1))
        assert mask.equals(get_xr_seq_from_list(expected))


class TestNdsi:
    def test_smoke_np(self):
        def _test(shape: tuple[int, ...]):
            ri1, _, ri3, _, _ = get_data_np(shape)
            index.ndsi(ri1, ri3)

        _test(IMAGE_SHAPE)
        _test((2, *IMAGE_SHAPE))

    def test_smoke_xr(self):
        def _test(shape: tuple[int, ...]):
            ri1, _, ri3, _, _ = get_data_xr(shape)
            index.ndsi(ri1, ri3)

        _test(IMAGE_SHAPE)
        _test((2, *IMAGE_SHAPE))

    @pytest.mark.parametrize(
        ("ri1", "ri3", "expected"),
        [
            (
                # ri1
                [np.nan, 5, 15],
                # ri3
                [np.nan, 5, 5],
                # expected
                [np.nan, 0, 0.5],
            )
        ],
    )
    def test_alg(self, ri1, ri3, expected):
        mask = index.ndvi(get_np_from_list(ri1), get_np_from_list(ri3))
        assert np.allclose(mask, get_np_from_list(expected), equal_nan=True)

        mask = index.ndvi(get_np_seq_from_list(ri1), get_np_seq_from_list(ri3))
        assert np.allclose(mask, get_np_seq_from_list(expected), equal_nan=True)

        mask = index.ndvi(get_xr_from_list(ri1), get_xr_from_list(ri3))
        assert mask.equals(get_xr_from_list(expected))

        mask = index.ndvi(get_xr_seq_from_list(ri1), get_xr_seq_from_list(ri3))
        assert mask.equals(get_xr_seq_from_list(expected))
