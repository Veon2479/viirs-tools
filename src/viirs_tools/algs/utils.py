import numpy as np
import xarray as xr

from viirs_tools.utils.types import ArrayLike, _check_data


def merge_day_night(day, night, nmask):
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
    _check_data(day, night, nmask)
    mask = xr.where(nmask == 0, day, night)
    return mask
