import numpy as np
import numpy.ma as ma


def _get_masked(data, thr):
    """
        Do masking on the given array for specified threshold
    Args:
        data (list|np.ndarray): given data array
        thr (data values type): threshold value
    Returns:
        (np.ma.MaskedArray): resulting array
    """
    if thr > 0:
        mask = np.where(data >= thr, 1, 0)
    else:
        mask = np.where(data <= thr, 1, 0)
    masked = ma.masked_array(data, mask=mask)
    return masked


def read_so_data(name, file):
    """
        Read from NASA distributed hdf's ans nc's files
            data stored in Scale-Offset model
    Args:
        name (string): name of the desired dataset
        file (string): path to the file
    Returns:
        np.ma.array: dataset from the file
    """
    scale = 1
    offset = 0
    if 'Scale' in file.variables[name].ncattrs():
        scale = file.variables[name].getncattr('Scale')
    if 'Offset' in file.variables[name].ncattrs():
        offset = file.variables[name].getncattr('Offset')
    ref = file.variables[name][:]
    thr = file.variables[name].getncattr('FILL_TEST_VALUE').split('=')[1]
    r = _get_masked(ref, float(thr)) * scale + offset
    return r


# Wrappers for handy extracting different types of data


def read_ref(band, file):
    return read_so_data(f'Reflectance_{band}', file)


def read_rad(band, file):
    return read_so_data(f'Radiance_{band}', file)


def read_bt(band, file):
    return read_so_data(f'BrightnessTemperature_{band}', file)


def read_lat(file):
    return read_so_data('Latitude', file)


def read_lon(file):
    return read_so_data('Longitude', file)


def read_solza(file):
    return read_so_data('SolarZenithAngle', file)


def read_solaa(file):
    return read_so_data('SolarAzimuthAngle', file)


def read_satza(file):
    return read_so_data('SatelliteZenithAngle', file)


def read_sataa(file):
    return read_so_data('SatelliteAzimuthAngle', file)
