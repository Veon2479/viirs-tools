import numpy as np
import xarray as xr

from viirs_tools.utils.types import ArrayLike, _check_data


def water_bodies_day(ri1: ArrayLike, ri2: ArrayLike, ri3: ArrayLike) -> ArrayLike:
    """Day reflectance water bodies test
    Based on the W.Schroeder, P.Oliva, L.Giglio, I.A.Csiszar (2014).
    The New VIIRS 375 m active fire detection data product:
        Algorithm description and initial assessment

    Args:
        ri1 : I01 in reflectance calibration
        ri2 : I02 in reflectance calibration
        ri3 : I03 in reflectance calibration

    Returns:
        Binary water bodies mask, 0 is clear water body, 1 is clear pixel
            Can contain NaN values
    """
    _check_data(ri1, ri2, ri3)

    mask = (ri1 > ri2) & (ri2 > ri3)

    return 1 - xr.where(xr.ufuncs.isnan(ri1), np.nan, mask)
