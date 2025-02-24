import numpy as np
import xarray as xr

from viirs_tools.utils.types import ArrayLike, _check_data


def _mono_window(bt, band_lambda, ndvi, cmask=None):
    """
        LST retrieval algorithm for day conditions
        Based on the U.Adam, G.Jovanoska (2016).
        Algorithm for Automated Mapping of
            Land Surface Temperature Using LANDSAT 8 Satellite Data
    Args:
        bt: (np.ndarray|xr.Dataset): band at ~10-12 um in BT calibration
        band_lambda: (float) wavelength of emitted radiance in used band
            (the peak response or average of the limiting wavelength)
            Unit is um
        ndvi: (np.ndarray|xr.Dataset): NDVI in corresponding resolution
        cmask: (np.ndarray|xr.Dataset, optional): integer cloud mask,
            1 is clear sky pixel
    Returns:
        (np.ndarray, xr.Dataset): array containing LST,
            Can contain NaN values
    """
    if cmask is not None:
        _check_data(bt, ndvi, cmask)
    else:
        _check_data(bt, ndvi)

    bt_c = bt - 273.15  # to Celsius

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

    lst = bt_c / (1 + (band_lambda*bt_c/p) * np.log(e_l) * 1e-12)
    if cmask is not None:
        lst = xr.where(cmask == 1, lst, nan)
    return lst


def mono_window_i05(bi05, ndvi, cmask=None):
    """
        LST retrieval algorithm for day conditions
        Based on the U.Adam, G.Jovanoska (2016).
        Algorithm for Automated Mapping of
            Land Surface Temperature Using LANDSAT 8 Satellite Data
    Args:
        bi05: (np.ndarray|xr.Dataset): I05 in BT calibration
        ndvi: (np.ndarray|xr.Dataset): NDVI in corresponding resolution
        cmask: (np.ndarray|xr.Dataset, optional): integer cloud mask,
            1 is clear sky pixel
    Returns:
        (np.ndarray, xr.Dataset): array containing LST,
            Can contain NaN values
    """
    return _mono_window(bi05, (10.5+12.4)/2, ndvi, cmask=cmask)


def mono_window_m15(bm15, ndvi, cmask=None):
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
    return _mono_window(bm15, (10.263+11.263)/2, ndvi, cmask=cmask)


def mono_window_m16(bm16, ndvi, cmask=None):
    """
        LST retrieval algorithm for day conditions
        Based on the U.Adam, G.Jovanoska (2016).
        Algorithm for Automated Mapping of
            Land Surface Temperature Using LANDSAT 8 Satellite Data
    Args:
        bm16: (np.ndarray|xr.Dataset): M16 in BT calibration
        ndvi: (np.ndarray|xr.Dataset): NDVI in corresponding resolution
        cmask: (np.ndarray|xr.Dataset, optional): integer cloud mask,
            1 is clear sky pixel
    Returns:
        (np.ndarray, xr.Dataset): array containing LST,
            Can contain NaN values
    """
    return _mono_window(bm16, (11.538+12.488)/2, ndvi, cmask=cmask)
