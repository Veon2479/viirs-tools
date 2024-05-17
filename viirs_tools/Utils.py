import xarray as xr
import numpy as np
from math import nan

# Internal functions:


def _check_data(data):
    """
        Check object for being of appropriate type
        Currently supported types:
            * np.ndarray
            * xr.DataArray
    Args:
        data (any): object to be tested
    """
    if not isinstance(data, (np.ndarray, xr.DataArray)):
        raise ValueError(
            "Input data is not array (numpy or xarray) object"
        )


def _get_da(ds, name):
    """
        Helper function for preserving datasets attributes
        that are crucial for later operations
        like saving to the geo-tiff
    Args:
        ds (xr.Dataset): desired dataset
        name (string): xr.DataArray to extract
    Returns:
        xr.DataArray
    """
    da = ds[name]
    attrs_to_copy = ['crs', 'grid_mapping']
    for attr in attrs_to_copy:
        if attr in ds.attrs:
            da.attrs[attr] = ds.attrs[attr]
    return da


# Public functions:


def max_values(data):
    """
        Single function for finding
        max values per time slice
        for various data forms
    Args:
        data (np.ndarray|xr.DataArray):
            slice or set of slices for searching for max values
    Returns
        (xr.DataArray|dtype of data vales):
            max value for given slice or xr.Datarray of such values
            with time dimension
    """
    if isinstance(data, np.ndarray):
        return np.nanmax(data)
    elif isinstance(data, xr.DataArray):
        dims = list(data.dims)
        data_max = None
        if 'time' in dims:
            dims.pop(dims.index('time'))
            data_max = data.max(dim=dims)
        else:
            data_max = data.max(dim=dims).item()
    else:
        raise ValueError(
            "Input data is not array (numpy or xarray) object"
        )
    return data_max


def median_values(data):
    """
        Single function for finding
        median values per time slice
        for various data forms
    Args:
        data (np.ndarray|xr.DataArray):
            slice or set of slices for searching for max values
    Returns
        (xr.DataArray|dtype of data vales):
            median value for given slice or xr.Datarray of such values
            with time dimension
    """
    if isinstance(data, np.ndarray):
        return np.nanmedian(data)
    elif isinstance(data, xr.DataArray):
        dims = list(data.dims)
        data_max = None
        if 'time' in dims:
            dims.pop(dims.index('time'))
            data_max = data.median(dim=dims)
        else:
            data_max = data.median(dim=dims).item()
    else:
        raise ValueError(
            "Input data is not array (numpy or xarray) object"
        )
    return data_max


def nan_mask(data):
    """
        Performs type-independent Nan-checking
    Args:
        data(np.ndarray|xr.DataArray|xr.Dataset):
            object to be tested
    """
    if isinstance(data, np.ndarray):
        return np.isnan(data)
    elif isinstance(data, (xr.DataArray, xr.Dataset)):
        return data.isnull()
    else:
        raise ValueError(
            "Input data is not array (numpy or xarray) object"
        )


def not_nan_mask(data):
    """
        Performs type-independent not-Nan-checking
    Args:
        data(np.ndarray|xr.DataArray|xr.Dataset):
            object to be tested
    """
    if isinstance(data, np.ndarray):
        return np.logical_not(np.isnan(data))
    elif isinstance(data, (xr.DataArray, xr.Dataset)):
        return data.notnull()
    else:
        raise ValueError(
            "Input data is not array (built-in, np or xr) object"
        )


def merge_day_night(day, night, nm):
    """
        Merge day and night composits
    Args:
        day_cm(np.ndarray|xr.DataArray):
            day composit
        night_cm(np.ndarray|xr.DataArray):
            night composit
        nm(np.ndarray|xr.DataArray):
            binary night mask
    Returns:
        (np.ndarray|xr.DataArray):
            merged composit
    """
    mask = xr.where(nm == 0, day, night)
    return mask


def ndvi(NIR, R):
    """
        Get NDVI index from reflectance bands
        Most common use is (I2, I1) or (M7, M5) as (NIR, R)
    Args:
        NIR(np.ndarray|xr.DataArray): near-infrared reflectance band
        R(np.ndarray|xr.DataArray): red reflectance band
    Returns:
        (np.ndarray|xr.DataArray): NDVI index for each pixel,
            can contain NaN values
    """
    i = (NIR - R) / (NIR + R)
    mask = nan_mask(NIR)
    return xr.where(mask, nan, i)
