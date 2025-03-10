from __future__ import annotations

import numpy as np
import xarray as xr

from viirs_tools.utils.types import ArrayLike, _check_data


def naive(refband: ArrayLike, btband: ArrayLike) -> ArrayLike:
    """Get night mask from any reflectance and brightness bands
    Day/Night state here meets the condition SZA < 90 deg
    Assumed that data was loaded in the reflectance or
        brightness-temperature, not radiance calibration

    Args:
        refband : any reflectance data
        btband : any brightness-temperature data

    Returns:
        Integer mask, 1 means night state, 0 means day state,
            Can contain NaN values in case of missing data in BT band
    """
    _check_data(refband, btband)

    bmask = ~xr.ufuncs.isnan(btband)
    rmask = xr.ufuncs.isnan(refband)
    return xr.where(bmask, rmask, np.nan)
