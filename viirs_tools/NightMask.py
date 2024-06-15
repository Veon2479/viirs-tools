import xarray as xr
import math

from . import Utils

# Public functions:


def naive(refband, btband):
    """
        Get night mask from any reflectance and brightness bands
        Day/Night state here meets the condition SZA < 90 deg
        Assumed that data was loaded in the reflectance or
            brightness-temperature, not radiance calibration
    Args:
        refband (np.ndarray|xr.DataArray):
            any reflectance data
        btband (np.ndarray|xr.DataArray):
            any brightness-temperature data
    Returns:
        (np.ndarray|xr.DataArray): integer mask,
            1 means night state, 0 means day state,
            Can contain NaN values in case of missing data in BT band
    """
    bmask = Utils.not_nan_mask(btband)
    rmask = Utils.nan_mask(refband)
    return xr.where(bmask, rmask, math.nan).astype(float)


# Internal wrappers:


def _naive_ds(ds, refbands, btbands):
    """
        Internal wrapper for getting night mask from xr.Dataset
        Day/Night state here meets the condition SZA < 90 deg
        Assumed that data was loaded in the reflectance or
            brightness-temperature, not radiance calibration
    Args:
        ds (xr.Dataset): original data
        refbands (list of strings): names of reflectance datasets
        btbands (list of strings): names of BT datasets
    Returns:
        (xr.DataArray): integer mask,
            1 means night state, 0 means day state,
            Can contain NaN values in case of missing data in BT band
    """
    if not isinstance(ds, xr.Dataset):
        raise ValueError(
            "Incorrect input data format"
        )
    refband = None
    btband = None
    for b in refbands:
        if b in ds.data_vars:
            refband = b
            break
    for b in btbands:
        if b in ds.data_vars:
            btband = b
            break
    if refband is None or btband is None:
        raise ValueError(
            "Input data does not contain both ref and bt data"
        )
    rd = Utils._get_da(ds, refband)
    bd = Utils._get_da(ds, btband)
    return naive(rd, bd)


# Public xr.Dataset wrappers:


def naive_ds_img(ds):
    """
        Wrapper for getting night mask from xr.Dataset directly
            using imagery resolution (I-bands)
        Day/Night state here meets the condition SZA < 90 deg
        Assumed that data was loaded in the reflectance or
            brightness-temperature, not radiance calibration
    Args:
        ds (xr.Dataset): contains both reflectance and
            brightness-temperature data
    Returns:
        (xr.DataArray): integer mask,
            1 means night state, 0 means day state,
            Can contain NaN values in case of missing data in BT band
    """
    rbands = ['I{:02d}'.format(i) for i in range(1, 3 + 1)]
    bbands = ['I{:02d}'.format(i) for i in range(4, 5 + 1)]
    return _naive_ds(ds, rbands, bbands)


def naive_ds_mod(ds):
    """
        Wrapper for getting night mask from xr.Dataset directly
            using moderate resolution (M-bands)
        Day/Night state here meets the condition SZA < 90 deg
        Assumed that data was loaded in the reflectance or
            brightness-temperature, not radiance calibration
    Args:
        ds (xr.Dataset): contains both reflectance and
            brightness-temperature data
    Returns:
        (xr.DataArray): integer mask,
            1 means night state, 0 means day state,
            Can contain NaN values in case of missing data in BT band
    """
    rbands = ['M{:02d}'.format(i) for i in range(1, 11 + 1)]
    bbands = ['M{:02d}'.format(i) for i in range(12, 16 + 1)]
    return _naive_ds(ds, rbands, bbands)
