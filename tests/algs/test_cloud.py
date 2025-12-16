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
from viirs_tools.algs import cloud


class TestVibcmDay:
    def test_smoke_np(self):
        def _test(shape: tuple[int, ...]):
            ri1, ri2, ri3, bi4, bi5 = get_data_np(shape)
            cloud.vibcm_day(ri1, ri2, ri3, bi4, bi5)

        _test(IMAGE_SHAPE)
        _test((2, *IMAGE_SHAPE))

    def test_smoke_xr(self):
        def _test(shape: tuple[int, ...]):
            ri1, ri2, ri3, bi4, bi5 = get_data_xr(shape)
            cloud.vibcm_day(ri1, ri2, ri3, bi4, bi5)

        _test(IMAGE_SHAPE)
        _test((2, *IMAGE_SHAPE))

    @pytest.mark.parametrize(
        ("ri1", "ri2", "ri3", "bi5", "expected"),
        [
            (
                # ri1
                [np.nan, 100],
                # ri2
                [np.nan, 20],
                # ri3
                [np.nan, 10],
                # bi5
                [np.nan, 200],
                # expected
                [np.nan, 0],
            ),
            (
                # ri1
                [100, 120, 7, 9, 100],
                # ri2
                [10, 30, 12, 30, 20],
                # ri3
                [10, 25, 1, 1, 40],
                # bi5
                [200, 400, 200, 200, 200],
                # expected
                [1, 1, 1, 1, 1],
            ),
        ],
    )
    def test_alg(self, ri1, ri2, ri3, bi5, expected):
        mask = cloud.vibcm_day(get_np_from_list(ri1), get_np_from_list(ri2), get_np_from_list(ri3), get_np_from_list(bi5))
        assert np.allclose(mask, get_np_from_list(expected), equal_nan=True)

        mask = cloud.vibcm_day(get_np_seq_from_list(ri1), get_np_seq_from_list(ri2), get_np_seq_from_list(ri3), get_np_seq_from_list(bi5))
        assert np.allclose(mask, get_np_seq_from_list(expected), equal_nan=True)

        mask = cloud.vibcm_day(get_xr_from_list(ri1), get_xr_from_list(ri2), get_xr_from_list(ri3), get_xr_from_list(bi5))
        assert mask.equals(get_xr_from_list(expected))

        mask = cloud.vibcm_day(get_xr_seq_from_list(ri1), get_xr_seq_from_list(ri2), get_xr_seq_from_list(ri3), get_xr_seq_from_list(bi5))
        assert mask.equals(get_xr_seq_from_list(expected))


class TestVifcmDay:
    def test_smoke_np(self):
        def _test(shape: tuple[int, ...]):
            ri1, ri2, _, _, bi5 = get_data_np(shape)
            cloud.vifcm_day(ri1, ri2, bi5)

        _test(IMAGE_SHAPE)
        _test((2, *IMAGE_SHAPE))

    def test_smoke_xr(self):
        def _test(shape: tuple[int, ...]):
            ri1, ri2, _, _, bi5 = get_data_xr(shape)
            cloud.vifcm_day(ri1, ri2, bi5)

        _test(IMAGE_SHAPE)
        _test((2, *IMAGE_SHAPE))

    @pytest.mark.parametrize(
        ("ri1", "ri2", "bi5", "expected"),
        [
            (  # missing values
                # ri1
                [np.nan],
                # ri2
                [np.nan],
                # bi5
                [np.nan],
                # expected
                [np.nan],
            ),
            (  # all tests failed/passed
                # ri1
                [10, 50],
                # ri2
                [10, 50],
                # bi5
                [300, 260],
                # expected
                [1, 0],
            ),
            (  # single test passed
                # ri1
                [10, 50, 40],
                # ri2
                [10, 50, 40],
                # bi5
                [150, 290, 280],
                # expected
                [0, 0, 0],
            ),
        ],
    )
    def test_alg(self, ri1, ri2, bi5, expected):
        mask = cloud.vifcm_day(get_np_from_list(ri1), get_np_from_list(ri2), get_np_from_list(bi5))
        assert np.allclose(mask, get_np_from_list(expected), equal_nan=True)

        mask = cloud.vifcm_day(get_np_seq_from_list(ri1), get_np_seq_from_list(ri2), get_np_seq_from_list(bi5))
        assert np.allclose(mask, get_np_seq_from_list(expected), equal_nan=True)

        mask = cloud.vifcm_day(get_xr_from_list(ri1), get_xr_from_list(ri2), get_xr_from_list(bi5))
        assert mask.equals(get_xr_from_list(expected))

        mask = cloud.vifcm_day(get_xr_seq_from_list(ri1), get_xr_seq_from_list(ri2), get_xr_seq_from_list(bi5))
        assert mask.equals(get_xr_seq_from_list(expected))


class TestVifcmNight:
    def test_smoke_np(self):
        def _test(shape: tuple[int, ...]):
            _, _, _, bi4, bi5 = get_data_np(shape)
            cloud.vifcm_night(bi4, bi5)

        _test(IMAGE_SHAPE)
        _test((2, *IMAGE_SHAPE))

    def test_smoke_xr(self):
        def _test(shape: tuple[int, ...]):
            _, _, _, bi4, bi5 = get_data_xr(shape)
            cloud.vifcm_night(bi4, bi5)

        _test(IMAGE_SHAPE)
        _test((2, *IMAGE_SHAPE))
        _test((2, *IMAGE_SHAPE))

    @pytest.mark.parametrize(
        ("bi4", "bi5", "expected"),
        [
            (
                # bi4
                [np.nan, 100, 300, 200, 300],
                # bi5
                [np.nan, 100, 200, 300, 300],
                # expected
                [np.nan, 0, 1, 1, 1],
            )
        ],
    )
    def test_alg(self, bi4, bi5, expected):
        mask = cloud.vifcm_night(get_np_from_list(bi4), get_np_from_list(bi5))
        assert np.allclose(mask, get_np_from_list(expected), equal_nan=True)

        mask = cloud.vifcm_night(get_np_seq_from_list(bi4), get_np_seq_from_list(bi5))
        assert np.allclose(mask, get_np_seq_from_list(expected), equal_nan=True)

        mask = cloud.vifcm_night(get_xr_from_list(bi4), get_xr_from_list(bi5))
        assert mask.equals(get_xr_from_list(expected))

        mask = cloud.vifcm_night(get_xr_seq_from_list(bi4), get_xr_seq_from_list(bi5))
        assert mask.equals(get_xr_seq_from_list(expected))
