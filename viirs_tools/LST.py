import xarray as xr
import numpy as np
from math import nan

from . import Utils


# Internal functions:


def _mono_window(bm15, ndvi, cmask=None):
    """
        LST retrieval algorithm for day conditions
        Based on the U.Adam, G.Jovanoska (2016).
        Algorithm for Automated Mapping of
            Land Surface Temperature Using LANDSAT 8 Satellite Data
    Args:
        bm15: (np.ndarray|xr.Dataset): M15 in BT calibration
        ndvi: (np.ndarray|xr.Dataset): NDVI in corresponding resolution
        cmask: (np.ndarray|xr.Dataset, optional): integer cloud mask,
            1 is clear sky pixel
    Returns:
        (np.ndarray, xr.Dataset): array containing LST,
            Can contain NaN values
    """
    bm15 -= 273.15  # to Celsius

    ndvi_s = 0.2
    ndvi_v = 0.5
    p_v = ((ndvi - ndvi_s) / (ndvi_v - ndvi_s))**2

    c = 0.005  # represents surface roughness

    e_s = 0.966  # soil emissivity
    e_v = 0.973  # vegetation emissivity
    e_w = 0.991  # water emmisivity

    e_l = e_v*p_v + e_s*(1-p_v) + c
    e_l = xr.where(ndvi < ndvi_s, e_s, e_l)
    e_l = xr.where(ndvi < 0, e_w, e_l)  # ndvi < 0 indicates water
    e_l = xr.where(ndvi > ndvi_v, e_v, e_l)

    p = 1.438e-2
    band_lambda = 10.76  # avg for m15 range (10.26 - 11.26 um)

    lst = bm15 / (1 + (band_lambda*bm15/p) * np.log(e_l))
    if cmask is not None:
        lst = xr.where(cmask == 1, lst, nan)
    return lst


# Public wrappers:


def mono_window(bm15, ndvi, cmask=None):
    """
        LST retrieval algorithm for day conditions
        Based on the U.Adam, G.Jovanoska (2016).
        Algorithm for Automated Mapping of
            Land Surface Temperature Using LANDSAT 8 Satellite Data
    Args:
        bm15: (np.ndarray|xr.Dataset): M15 in BT calibration
        ndvi: (np.ndarray|xr.Dataset): NDVI in corresponding resolution
        cmask: (np.ndarray|xr.Dataset, optional): integer cloud mask,
            1 is clear sky pixel
    Returns:
        (np.ndarray, xr.Dataset): array containing LST,
            Can contain NaN values
    """
    Utils._check_data(bm15)
    Utils._check_data(ndvi)
    if cmask is not None:
        Utils._check_data(cmask)
    return _mono_window(
        bm15, ndvi,
        cmask=cmask
    )


# Public xr.Dataset wrappers:


def mono_window_ds(ds, ndvi, cmask=None):
    """
        Wrapper for LST retrieval algorithm for day conditions
        Based on the U.Adam, G.Jovanoska (2016).
        Algorithm for Automated Mapping of
            Land Surface Temperature Using LANDSAT 8 Satellite Data
    Args:
        ds (xr.Dataset): dataset with M15 band data
        ndvi: (np.ndarray|xr.Dataset): NDVI in corresponding resolution
        cmask: (np.ndarray|xr.Dataset, optional): integer cloud mask,
            1 is clear sky pixel
    Returns:
        (np.ndarray, xr.Dataset): array containing LST,
            Can contain NaN values
    """
    if not isinstance(ds, xr.Dataset):
        raise ValueError(
            "Incorrect input data format"
        )
    return mono_window(
        ds['M15'], ndvi,
        cmask=cmask
    )
