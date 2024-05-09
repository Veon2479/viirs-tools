import xarray as xr
from math import nan

from . import Utils


# Internal functions:


def _rsnpp_day_img(ri1, ri2, ri3, bi4, bi5, nmask):
    """
        Day reflectance/thermal I-bands cloud test
        Based on the M.Piper, T.Bahr (2015).
        A RAPID CLOUD MASK ALGORITHM FOR SUOMI NPP VIIRS IMAGERY EDRS
    Args:
        ri1 (list|np.ndarray|xr.Dataset): I01 in reflectance calibration
        ri2 (list|np.ndarray|xr.Dataset): I02 in reflectance calibration
        ri3 (list|np.ndarray|xr.Dataset): I03 in reflectance calibration
        bi4 (list|np.ndarray|xr.Dataset): I04 in BT calibration
        bi5 (list|np.ndarray|xr.Dataset): I05 in BT calibration
        nmask (list|np.ndarray|xr.Dataset): Day/night mask (1 is night)
    Returns:
        (list|np.ndarray|xr.Dataset): integer cloud mask,
            0 is cloud, 1 is clear pixel
            Can contain NaN values
    """

    t1 = xr.where(ri1 > 8, True, False)

    ndsi = (ri1 - ri3) / (ri1 + ri3)
    t2 = xr.where(ndsi < 0.7, True, False)
    t2 = xr.where(ri2 > 11, t2, False)

    t3 = xr.where(bi5 < 300, True, False)

    ri3_max = Utils.max_values(ri3)
    t4 = xr.where((ri3_max - ri3) * bi5 / 100 < 410, True, False)

    t5 = xr.where(ri2 / ri1 < 2, True, False)

    t6 = xr.where(ri2 / ri3 > 1, True, False)

    cm = xr.where(t1 & t2, 0, 1)
    cm = xr.where(cm & t3, 0, 1)
    cm = xr.where(cm & t4, 0, 1)
    cm = xr.where(cm & t5, 0, 1)
    cm = xr.where(cm & t6, 0, 1)

    cm = xr.where(nmask == 0, cm, nan)

    return cm


def _fire_day_img(ri1, ri2, bi5, nmask):
    """
        Day reflectance & termal I-bands cloud test
        Based on the W.Schroeder, P.Oliva, L.Giglio, I.A.Csiszar (2014).
        The New VIIRS 375 m active fire detection data product:
            Algorithm description and initial assessment
    Args:
        ri1 (list|np.ndarray|xr.Dataset): I01 in reflectance calibration
        ri2 (list|np.ndarray|xr.Dataset): I02 in reflectance calibration
        bi5 (list|np.ndarray|xr.Dataset): I05 in BT calibration
        nmask (list|np.ndarray|xr.Dataset): Day/night mask (1 is night)
    Returns:
        (list|np.ndarray|xr.Dataset): integer cloud mask,
            0 is cloud, 1 is clear pixel
            Can contain NaN values
    """
    cm = xr.where(bi5 < 265, 0, 1)

    sum_ri = ri1 + ri2

    t2 = xr.where(sum_ri > 90, 0, 1)
    t2 = xr.where(bi5 < 295, t2, 1)

    t3 = xr.where(sum_ri > 70, 0, 1)
    t3 = xr.where(bi5 < 285, t2, 1)

    cm = xr.where(t2 == 0, 0, cm)
    cm = xr.where(t3 == 0, 0, cm)

    cm = xr.where(nmask == 0, cm, nan)
    return cm


def _fire_night_img(bi4, bi5, nmask):
    """
        Night termal I-bands cloud test
        Based on the W.Schroeder, P.Oliva, L.Giglio, I.A.Csiszar (2014).
        The New VIIRS 375 m active fire detection data product:
            Algorithm description and initial assessment
    Args:
        bi4 (list|np.ndarray|xr.Dataset): I04 in BT calibration
        bi5 (list|np.ndarray|xr.Dataset): I05 in BT calibration
        nmask (list|np.ndarray|xr.Dataset): Day/night mask (1 is night)
    Returns:
        (list|np.ndarray|xr.Dataset): integer cloud mask,
            0 is cloud, 1 is clear pixel
            Can contain NaN values
    """
    cm = xr.where(bi4 < 265, 0, 1)
    cm = xr.where(bi5 < 295, cm, 0)
    cm = xr.where(Utils.not_nan_mask(bi4), cm, nan)

    cm = xr.where(nmask == 1, cm, nan)

    return cm


# Public wrappers:


def rsnpp_day_img(ri1, ri2, ri3, bi4, bi5, nmask):
    """
        Day reflectance/thermal I-bands cloud test
        Based on the M.Piper, T.Bahr (2015).
        A RAPID CLOUD MASK ALGORITHM FOR SUOMI NPP VIIRS IMAGERY EDRS
    Args:
        ri1 (list|np.ndarray|xr.Dataset): I01 in reflectance calibration
        ri2 (list|np.ndarray|xr.Dataset): I02 in reflectance calibration
        ri3 (list|np.ndarray|xr.Dataset): I03 in reflectance calibration
        bi4 (list|np.ndarray|xr.Dataset): I04 in BT calibration
        bi5 (list|np.ndarray|xr.Dataset): I05 in BT calibration
        nmask (list|np.ndarray|xr.Dataset): Day/night mask (1 is night)
    Returns:
        (list|np.ndarray|xr.Dataset): integer cloud mask,
            0 is cloud, 1 is clear pixel
            Can contain NaN values
    """
    Utils._check_data(ri1)
    Utils._check_data(ri2)
    Utils._check_data(ri3)
    Utils._check_data(bi4)
    Utils._check_data(bi5)
    Utils._check_data(nmask)

    return _rsnpp_day_img(
        ri1, ri2, ri3,
        bi4, bi5,
        nmask
    )


def fire_day_img(ri1, ri2, bi5, nmask):
    """
        Day reflectance & termal I-bands cloud test
        Based on the W.Schroeder, P.Oliva, L.Giglio, I.A.Csiszar (2014).
        The New VIIRS 375 m active fire detection data product:
            Algorithm description and initial assessment
    Args:
        ri1 (list|np.ndarray|xr.Dataset): I01 in reflectance calibration
        ri2 (list|np.ndarray|xr.Dataset): I02 in reflectance calibration
        bi5 (list|np.ndarray|xr.Dataset): I05 in BT calibration
        nmask (list|np.ndarray|xr.Dataset): Day/night mask (1 is night)
    Returns:
        (list|np.ndarray|xr.Dataset): integer cloud mask,
            0 is cloud, 1 is clear pixel
            Can contain NaN values
    """
    Utils._check_data(ri1)
    Utils._check_data(ri2)
    Utils._check_data(bi5)
    return _fire_day_img(ri1, ri2, bi5, nmask)


def fire_night_img(bi4, bi5, nmask):
    """
        Night termal I-bands cloud test
        Based on the W.Schroeder, P.Oliva, L.Giglio, I.A.Csiszar (2014).
        The New VIIRS 375 m active fire detection data product:
            Algorithm description and initial assessment
    Args:
        bi4 (list|np.ndarray|xr.Dataset): I04 in BT calibration
        bi5 (list|np.ndarray|xr.Dataset): I05 in BT calibration
        nmask (list|np.ndarray|xr.Dataset): Day/night mask (1 is night)
    Returns:
        (list|np.ndarray|xr.Dataset): integer cloud mask,
            0 is cloud, 1 is clear pixel
            Can contain NaN values
    """
    Utils._check_data(bi4)
    Utils._check_data(bi5)
    return _fire_night_img(bi4, bi5, nmask)


# Public xr.Dataset wrappers:


def rsnpp_day_img_ds(ds, nmask):
    """
        Wrapper for day reflectance/thermal I-bands cloud test
            for xr.Dataset objects
        Based on the M.Piper, T.Bahr (2015).
        A RAPID CLOUD MASK ALGORITHM FOR SUOMI NPP VIIRS IMAGERY EDRS
    Args:
        ds (xr.Dataset): dataset with I01-I05 bands data
        nmask (xr.Dataset): Day/night mask (1 is night)
    Returns:
        (xr.Dataset): integer cloud mask,
            0 is cloud, 1 is clear pixel
            Can contain NaN values
    """
    if not isinstance(ds, xr.Dataset):
        raise ValueError(
            "Incorrect input data format"
        )
    if not isinstance(nmask, xr.DataArray):
        raise ValueError(
            "Incorrect input data format"
        )
    return rsnpp_day_img(
        ds['I01'],
        ds['I02'],
        ds['I03'],
        ds['I04'],
        ds['I05'],
        nmask
    )


def fire_day_img_ds(ds, nmask):
    """
        Wrapper for Day reflectance & termal I-bands cloud test for xr.Dataset
        Based on the W.Schroeder, P.Oliva, L.Giglio, I.A.Csiszar (2014).
        The New VIIRS 375 m active fire detection data product:
            Algorithm description and initial assessment
    Args:
        ds (xr.Dataset): dataset with I01, I02, I05 bands data
        nmask (list|np.ndarray|xr.Dataset): Day/night mask (1 is night)
    Returns:
        (xr.Dataset): integer cloud mask,
            0 is cloud, 1 is clear pixel
            Can contain NaN values
    """
    if not isinstance(ds, xr.Dataset):
        raise ValueError(
            "Incorrect input data format"
        )
    return fire_day_img(
        ds['I01'],
        ds['I02'],
        ds['I05'],
        nmask
    )


def fire_night_img_ds(ds, nmask):
    """
        Wrapper for Night termal I-bands cloud test for xr.Dataset
        Based on the W.Schroeder, P.Oliva, L.Giglio, I.A.Csiszar (2014).
        The New VIIRS 375 m active fire detection data product:
            Algorithm description and initial assessment
    Args:
        ds (xr.Dataset): dataset with I04, I05 bands data
        nmask (list|np.ndarray|xr.Dataset): Day/night mask (1 is night)
    Returns:
        (xr.Dataset): integer cloud mask,
            0 is cloud, 1 is clear pixel
            Can contain NaN values
    """
    if not isinstance(ds, xr.Dataset):
        raise ValueError(
            "Incorrect input data format"
        )
    return fire_night_img(
        ds['I04'],
        ds['I05'],
        nmask
    )
