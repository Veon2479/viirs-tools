import xarray as xr
from math import nan

from . import Utils


# Internal functions

def _water_bodies_day(ri1, ri2, ri3, nmask):
    """
        Day reflectance water bodies test
        Based on the W.Schroeder, P.Oliva, L.Giglio, I.A.Csiszar (2014).
        The New VIIRS 375 m active fire detection data product:
            Algorithm description and initial assessment
    Args:
        ri1 (list|np.ndarray|xr.Dataset): I01 in reflectance calibration
        ri2 (list|np.ndarray|xr.Dataset): I02 in reflectance calibration
        ri3 (list|np.ndarray|xr.Dataset): I03 in reflectance calibration
        nmask (list|np.ndarray|xr.Dataset): Day/night mask (1 is night)
    Returns:
        (list|np.ndarray|xr.Dataset): binary water bodies mask,
            0 is clear pixel, 1 is water body
            Can contain NaN values
    """
    mask = xr.where(ri1 > ri2, 1, 0)
    mask = xr.where(ri2 > ri3, mask, 0)
    mask = xr.where(nmask == 1, nan, mask)
    return mask


# Public wrappers:


def water_bodies_day(ri1, ri2, ri3, nmask):
    """
        Day reflectance water bodies test
        Based on the W.Schroeder, P.Oliva, L.Giglio, I.A.Csiszar (2014).
        The New VIIRS 375 m active fire detection data product:
            Algorithm description and initial assessment
    Args:
        ri1 (list|np.ndarray|xr.Dataset): I01 in reflectance calibration
        ri2 (list|np.ndarray|xr.Dataset): I02 in reflectance calibration
        ri3 (list|np.ndarray|xr.Dataset): I03 in reflectance calibration
        nmask (list|np.ndarray|xr.Dataset): Day/night mask (1 is night)
    Returns:
        (list|np.ndarray|xr.Dataset): binary water bodies mask,
            0 is clear pixel, 1 is water body
            Can contain NaN values
    """
    Utils._check_data(ri1)
    Utils._check_data(ri2)
    Utils._check_data(ri3)
    Utils._check_data(nmask)
    return _water_bodies_day(ri1, ri2, ri3)


# Public xr.Dataset wrappers:


def water_bodies_day_ds(ds, nmask):
    """
        wrapper for day reflectance water bodies test
            for xr.Dataset objects
        Based on the W.Schroeder, P.Oliva, L.Giglio, I.A.Csiszar (2014).
        The New VIIRS 375 m active fire detection data product:
            Algorithm description and initial assessment
    Args:
        ri1 (list|np.ndarray|xr.Dataset): I01 in reflectance calibration
        ri2 (list|np.ndarray|xr.Dataset): I02 in reflectance calibration
        ri3 (list|np.ndarray|xr.Dataset): I03 in reflectance calibration
        nmask (list|np.ndarray|xr.Dataset): Day/night mask (1 is night)
    Returns:
        (list|np.ndarray|xr.Dataset): binary water bodies mask,
            0 is clear pixel, 1 is water body
            Can contain NaN values
    """
    if not isinstance(ds, xr.Dataset):
        raise ValueError(
            "Incorrect input data format"
        )
    return water_bodies_day(
        ds['I01'],
        ds['I02'],
        ds['I03'],
        nmask
    )
