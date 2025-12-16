import numpy as np
import xarray as xr

from viirs_tools.algs import index
from viirs_tools.utils.types import ArrayLike, _check_data


def vibcm_day(
    ri1: ArrayLike, ri2: ArrayLike, ri3: ArrayLike, bi5: ArrayLike, ndsi: ArrayLike | None = None, *, use_alt_thresholds: bool = False
) -> ArrayLike:
    """Day reflectance/thermal I-bands cloud test
    Based on the M.Piper, T.Bahr (2015).
    A RAPID CLOUD MASK ALGORITHM FOR SUOMI NPP VIIRS IMAGERY EDRS

    Args:
        ri1 : I01 in reflectance calibration
        ri2 : I02 in reflectance calibration
        ri3 : I03 in reflectance calibration
        bi5 : I05 in BT calibration
        use_alt_thresholds : flag to use alternative threshold values for tests

    Returns:
        Integer cloud mask, 0 is cloud, 1 is clear pixel
            Can contain NaN values
    """
    if ndsi is None:
        _check_data(ri1, ri2, ri3, bi5)
    else:
        _check_data(ri1, ri2, ri3, bi5, ndsi)

    # Test 1
    cm = xr.where(ri1 > 8, True, False)

    # Test 2
    snow_mask = index.ndsi(ri1, ri3) > 0.7 if ndsi is None else ndsi > 0.7
    mask = xr.where(ri2 > 11, snow_mask, False)
    cm = xr.where(mask, cm, xr.where(snow_mask, False, cm))

    # Test 3
    t3_thr = 300 if use_alt_thresholds else 312
    cm = xr.where(bi5 < t3_thr, cm, False)

    # Test 4
    t4_thr = 225 if use_alt_thresholds else 410
    ri3_max = np.nanmax(ri3, axis=(-2, -1), keepdims=True)
    cm = xr.where((ri3_max - ri3) * bi5 / 100 < t4_thr, cm, False)

    # Test 5
    cm = xr.where(ri2 / ri1 < 2, cm, False)

    # Test 6
    cm = xr.where(ri2 / ri3 > 1, cm, False)

    return 1 - xr.where(xr.ufuncs.isnan(ri1), np.nan, cm)


def vifcm_day(ri1: ArrayLike, ri2: ArrayLike, bi5: ArrayLike) -> ArrayLike:
    """Day reflectance & termal I-bands cloud test
    Based on the W.Schroeder, P.Oliva, L.Giglio, I.A.Csiszar (2014).
    The New VIIRS 375 m active fire detection data product:
        Algorithm description and initial assessment

    Args:
        ri1 : I01 in reflectance calibration
        ri2 : I02 in reflectance calibration
        bi5 : I05 in BT calibration

    Returns:
        Integer cloud mask, 0 is cloud, 1 is clear pixel
            Can contain NaN values
    """
    _check_data(ri1, ri2, bi5)

    # Test 1
    cm = xr.where(bi5 < 265, True, False)

    sum_ri = ri1 + ri2

    # Test 2
    cm = xr.where((sum_ri > 90) & (bi5 < 295), True, cm)

    # Test 3
    cm = xr.where((sum_ri > 70) & (bi5 < 285), True, cm)

    return 1 - xr.where(xr.ufuncs.isnan(ri1), np.nan, cm)


def vifcm_night(bi4: ArrayLike, bi5: ArrayLike, nmask: ArrayLike | None = None) -> ArrayLike:
    """Night termal I-bands cloud test
    Based on the W.Schroeder, P.Oliva, L.Giglio, I.A.Csiszar (2014).
    The New VIIRS 375 m active fire detection data product:
        Algorithm description and initial assessment

    Args:
        bi4 : I04 in BT calibration
        bi5 : I05 in BT calibration
        nmask : Day/night mask (1 is night)

    Returns:
        Integer cloud mask, 0 is cloud, 1 is clear pixel
            Can contain NaN values
    """
    if nmask is not None:
        _check_data(bi4, bi5, nmask)
    else:
        _check_data(bi4, bi5)

    cm = (bi5 < 265) & (bi4 < 295)

    if nmask is not None:
        cm = xr.where(nmask, cm, np.nan)

    return 1 - xr.where(xr.ufuncs.isnan(bi4), np.nan, cm)
