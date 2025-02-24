import numpy as np
import xarray as xr

from viirs_tools.utils.types import ArrayLike, _check_data


def water_bodies_day(ri1: ArrayLike, ri2: ArrayLike, ri3: ArrayLike) -> ArrayLike:
    """
        Day reflectance water bodies test
        Based on the W.Schroeder, P.Oliva, L.Giglio, I.A.Csiszar (2014).
        The New VIIRS 375 m active fire detection data product:
            Algorithm description and initial assessment
    Args:
        ri1 (np.ndarray|xr.Dataset): I01 in reflectance calibration
        ri2 (np.ndarray|xr.Dataset): I02 in reflectance calibration
        ri3 (np.ndarray|xr.Dataset): I03 in reflectance calibration
    Returns:
        (np.ndarray|xr.Dataset): binary water bodies mask,
            0 is clear pixel, 1 is water body
            Can contain NaN values
    """
    _check_data(ri1, ri2, ri3)

    mask = xr.where(ri1 > ri2, 1, 0)
    mask[ri2 <= ri3] = 0
    nanmask = xr.ufuncs.isnan(ri1)
    return xr.where(nanmask, np.nan, mask)
