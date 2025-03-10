from __future__ import annotations

import xarray as xr

from viirs_tools.utils.types import ArrayLike, _check_data


def merge_day_night(day: ArrayLike, night: ArrayLike, nmask: ArrayLike) -> ArrayLike:
    """Merge day and night composits

    Args:
        day_cm : day composit
        night_cm : night composit
        nmask : binary night mask

    Returns:
        Merged composit
    """
    _check_data(day, night, nmask)

    return xr.where(nmask == 0, day, night)
