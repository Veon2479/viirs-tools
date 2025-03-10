from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy import ma

if TYPE_CHECKING:
    from netCDF4 import Dataset


def _get_masked(data: np.ndarray, thr: float) -> ma.MaskedArray:
    """Do masking on the given array for specified threshold

    Args:
        data : given data array
        thr : threshold value

    Returns:
        resulting array
    """

    mask = data >= thr if thr > 0 else data <= thr
    return ma.masked_array(data, mask=mask)


def read_so_data(name: str, file: Dataset) -> ma.MaskedArray:
    """Read from NASA distributed hdf's and nc's files
    data stored in Scale-Offset model

    Args:
        name : name of the desired dataset
        file : file-like object, created with netCDF4

    Returns:
        dataset from the file
    """
    scale = 1
    offset = 0
    if "Scale" in file.variables[name].ncattrs():
        scale = file.variables[name].getncattr("Scale")
    if "Offset" in file.variables[name].ncattrs():
        offset = file.variables[name].getncattr("Offset")
    ref = file.variables[name][:]
    thr = file.variables[name].getncattr("FILL_TEST_VALUE").split("=")[1]
    return _get_masked(ref, float(thr)) * scale + offset


# Wrappers for handy extracting different types of data


def read_ref(band: str, file: Dataset) -> ma.MaskedArray:
    return read_so_data(f"Reflectance_{band}", file)


def read_rad(band: str, file: Dataset) -> ma.MaskedArray:
    return read_so_data(f"Radiance_{band}", file)


def read_bt(band: str, file: Dataset) -> ma.MaskedArray:
    return read_so_data(f"BrightnessTemperature_{band}", file)


def read_lat(file: Dataset) -> ma.MaskedArray:
    return read_so_data("Latitude", file)


def read_lon(file: Dataset) -> ma.MaskedArray:
    return read_so_data("Longitude", file)


def read_solza(file: Dataset) -> ma.MaskedArray:
    return read_so_data("SolarZenithAngle", file)


def read_solaa(file: Dataset):
    return read_so_data("SolarAzimuthAngle", file)


def read_satza(file: Dataset):
    return read_so_data("SatelliteZenithAngle", file)


def read_sataa(file: Dataset):
    return read_so_data("SatelliteAzimuthAngle", file)
