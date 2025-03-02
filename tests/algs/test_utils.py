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
from viirs_tools.algs import night, utils


class TestMerge:
    def test_smoke_np(self):
        def _test(shape: tuple[int, ...]):
            ri1, _, _, bi4, _ = get_data_np(shape)
            nmask = night.naive(ri1, bi4)
            utils.merge_day_night(ri1, bi4, nmask)

        _test(IMAGE_SHAPE)
        _test((2, *IMAGE_SHAPE))

    def test_smoke_xr(self):
        def _test(shape: tuple[int, ...]):
            ri1, _, _, bi4, _ = get_data_xr(shape)
            nmask = night.naive(ri1, bi4)
            utils.merge_day_night(ri1, bi4, nmask)

        _test(IMAGE_SHAPE)
        _test((2, *IMAGE_SHAPE))

    @pytest.mark.parametrize(
        ("day", "night", "nmask", "expected"),
        [
            (
                # day
                [1, 1, 1],
                # night
                [5, 5, 5],
                # nmask
                [np.nan, 0, 1],
                # expected
                [5, 1, 5],
            )
        ],
    )
    def test_alg(self, day, night, nmask, expected):
        mask = utils.merge_day_night(get_np_from_list(day), get_np_from_list(night), get_np_from_list(nmask))
        assert np.allclose(mask, get_np_from_list(expected), equal_nan=True)

        mask = utils.merge_day_night(get_np_seq_from_list(day), get_np_seq_from_list(night), get_np_seq_from_list(nmask))
        assert np.allclose(mask, get_np_seq_from_list(expected), equal_nan=True)

        mask = utils.merge_day_night(get_xr_from_list(day), get_xr_from_list(night), get_xr_from_list(nmask))
        assert mask.equals(get_xr_from_list(expected))

        mask = utils.merge_day_night(get_xr_seq_from_list(day), get_xr_seq_from_list(night), get_xr_seq_from_list(nmask))
        assert mask.equals(get_xr_seq_from_list(expected))
