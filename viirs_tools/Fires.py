import xarray as xr
from math import nan

from . import Utils


# Internal functions

def _active_fires(ri1, ri2, ri3, bi4, bi5, nmask, cmask, wmask):
    """
        Fire mask from actives fire VIIRS product
        Based on the W.Schroeder, P.Oliva, L.Giglio, I.A.Csiszar (2014).
        The New VIIRS 375 m active fire detection data product:
            Algorithm description and initial assessment
    Args:
        ri1 (list|np.ndarray|xr.Dataset): I01 in reflectance calibration
        ri2 (list|np.ndarray|xr.Dataset): I02 in reflectance calibration
        ri3 (list|np.ndarray|xr.Dataset): I03 in reflectance calibration
        bi4 (list|np.ndarray|xr.Dataset): I04 in BT calibration
        bi5 (list|np.ndarray|xr.Dataset): I05 in BT calibration
        nmask (list|np.ndarray|xr.Dataset): Day/night mask (1 is night)
        cmask (list|np.ndarray|xr.Dataset): Cloud mask (1 is clear pixel)
        wmask (list|np.ndarray|xr.Dataset): water bodies mask (1 is water body)
    Returns:
        (list|np.ndarray|xr.Dataset): binary fire mask,
            0 is clear pixel, 1 is fire
            Can contain NaN values
    """
    ri12 = ri1 + ri2
    bi45 = bi4 - bi5
    saturated_bi4 = xr.where(bi4 == 367)

    # Fixed threshold tests:
    # night tests
    nt0 = xr.where(bi4 > 320, 1, 0)

    nt1 = xr.where(bi45 < 0, 1, 0)
    nt1_1 = xr.where(bi5 > 310, 1, 0)
    nt1_2 = xr.where(bi4 == 208, 1, 0)
    nt1_2 = xr.where(bi5 > 335, nt1_2, 0)
    nt1 = xr.where((nt1_1 + nt1_2) != 0, nt1, 0)

    # day tests
    dt0 = xr.where(saturated_bi4, 1, 0)
    dt0 = xr.where(bi5 > 290, dt0, 0)
    dt0 = xr.where(ri12 > 70, dt0, 0)

    dt1 = xr.where(bi45 < 0, 1, 0)
    dt1 = xr.where(bi5 > 325, dt1, 0)

    # Potential background fires:
    # night tests
    nt2 = xr.where(bi4 > 335, 1, 0)
    nt2 = xr.where(bi4 > 30, nt2, 0)

    # day tests
    dt2 = xr.where(bi4 > 300, 1, 0)
    dt2 = xr.where(bi45 > 10, dt2, 0)

    # Bright fire-free targets (daytime only):
    ft = xr.where(ri12 > 60, 1, 0)
    ft = xr.where(bi5 < 285, ft, 0)
    ft = xr.where(ri3 > 30, ft, 0)
    ft = xr.where(ri3 > ri2, ft, 0)
    ft = xr.where(ri2 > 25, ft, 0)
    ft = xr.where(bi4 <= 235, ft, 0)

    # Candidate fire pixels:
    # night test
    cnt = xr.where(bi4 > 295, 1, 0)
    cnt = xr.where(bi45 > 10, 1, cnt)

    # day test
    cdt = xr.where(bi45 > 25, 1, 0)
    M = Utils.median_values(bi4)
    bi4m = xr.where(M > 325, M, 325)
    bi4s = xr.where(bi4m < 330, bi4m, 330)
    cdt = xr.where(bi4 > bi4s, 1, cdt)

    # Results merging:
    # night
    nt = nt0 + nt1 + nt2 + cnt
    nt = xr.where(nt > 0, 1, 0)

    # day
    dt = dt0 + dt1 + dt2 + cdt
    dt = xr.where(dt > 0, 1, 0)
    dt = xr.where(ft == 1, 0, dt)

    # merge
    mask = xr.where(nmask == 1, nt, nan)
    mask = xr.where(nmask == 0, dt, mask)
    mask = xr.where(cmask == 0, nan, mask)
    mask = xr.where(wmask == 0, nan, mask)
    return mask


# Public wrappers:


def active_fires(ri1, ri2, ri3, bi4, bi5, nmask, cmask, wmask):
    """
        Fire mask from actives fire VIIRS product
        Based on the W.Schroeder, P.Oliva, L.Giglio, I.A.Csiszar (2014).
        The New VIIRS 375 m active fire detection data product:
            Algorithm description and initial assessment
    Args:
        ri1 (list|np.ndarray|xr.Dataset): I01 in reflectance calibration
        ri2 (list|np.ndarray|xr.Dataset): I02 in reflectance calibration
        ri3 (list|np.ndarray|xr.Dataset): I03 in reflectance calibration
        bi4 (list|np.ndarray|xr.Dataset): I04 in BT calibration
        bi5 (list|np.ndarray|xr.Dataset): I05 in BT calibration
        nmask (list|np.ndarray|xr.Dataset): Day/night mask (1 is night)
        cmask (list|np.ndarray|xr.Dataset): Cloud mask (1 is clear pixel)
        wmask (list|np.ndarray|xr.Dataset): water bodies mask (1 is water body)
    Returns:
        (list|np.ndarray|xr.Dataset): binary fire mask,
            0 is clear pixel, 1 is fire
            Can contain NaN values
    """
    Utils._check_data(ri1)
    Utils._check_data(ri2)
    Utils._check_data(ri3)
    Utils._check_data(bi4)
    Utils._check_data(bi5)
    Utils._check_data(nmask)
    Utils._check_data(cmask)
    return _active_fires(
        ri1, ri2, ri3,
        bi4, bi5,
        nmask, cmask, wmask
    )


# Public xr.Dataset wrappers:


def active_fires_ds(ds, nmask, cmask, wmask):
    """
        Wrapper for fire mask from actives fire VIIRS product
            for xr.Dataset objects
        Based on the W.Schroeder, P.Oliva, L.Giglio, I.A.Csiszar (2014).
        The New VIIRS 375 m active fire detection data product:
            Algorithm description and initial assessment
    Args:
        ri1 (list|np.ndarray|xr.Dataset): I01 in reflectance calibration
        ri2 (list|np.ndarray|xr.Dataset): I02 in reflectance calibration
        ri3 (list|np.ndarray|xr.Dataset): I03 in reflectance calibration
        bi4 (list|np.ndarray|xr.Dataset): I04 in BT calibration
        bi5 (list|np.ndarray|xr.Dataset): I05 in BT calibration
        nmask (list|np.ndarray|xr.Dataset): Day/night mask (1 is night)
        cmask (list|np.ndarray|xr.Dataset): Cloud mask (1 is clear pixel)
        wmask (list|np.ndarray|xr.Dataset): water bodies mask (1 is water body)
    Returns:
        (list|np.ndarray|xr.Dataset): binary fire mask,
            0 is clear pixel, 1 is fire
            Can contain NaN values
    """
    if not isinstance(ds, xr.Dataset):
        raise ValueError(
            "Incorrect input data format"
        )
    return active_fires(
        ds['I01'],
        ds['I02'],
        ds['I03'],
        ds['I04'],
        ds['I05'],
        nmask, cmask, wmask
    )
