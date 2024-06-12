from netCDF4 import Dataset  # require netcdf4 being installed, not NetCDF4

from . import ReadingHelpers as rh


def read_npp_viaes_l1(path):
    """
        Read VIIRS I-band imagery product (VIAES_L1)
    Args:
        path (string): path to the desired file
    Returns:
        dict: datasets with reflectance, radiance,
            brightness temperature data
            as masked np-arrays
    """
    data = {}
    with Dataset(path, 'r') as ifile:
        # get reflectance data
        for i in range(1, 4):
            data[f'refi{i}'] = rh.read_ref(f'I{i}', ifile)

        # get brightness temperature data
        for i in range(4, 6):
            data[f'bti{i}'] = rh.read_bt(f'I{i}', ifile)

        # get radiance data
        for i in range(1, 6):
            data[f'radi{i}'] = rh.read_rad(f'I{i}', ifile)

    return data


def read_npp_vmaes_l1(path):
    """
        Read VIIRS M-band imagery product (VMAES_L1)
    Args:
        path (string): path to the desired file
    Returns:
        dict: datasets with reflectance, radiance,
            brightness temperature data, geo-reference
            as masked np-arrays
    """
    data = {}
    geo = {}
    with Dataset(path, 'r') as mfile:
        # get reflectance data
        for i in range(1, 12):
            data[f'refm{i}'] = rh.read_ref(f'M{i}', mfile)

        # get brightness temperature data
        for i in range(12, 17):
            data[f'btm{i}'] = rh.read_bt(f'M{i}', mfile)

        # get radiance data
        for i in range(1, 17):
            data[f'radm{i}'] = rh.read_rad(f'M{i}', mfile)

        # get geo data
        geo['lat'] = rh.read_lat(mfile)
        geo['lon'] = rh.read_lon(mfile)
        geo['solza'] = rh.read_solza(mfile)
        geo['solaa'] = rh.read_solaa(mfile)
        geo['satza'] = rh.read_satza(mfile)
        geo['sataa'] = rh.read_sataa(mfile)

    return data, geo


def read_npp_cldmsk_l2(path):
    """
        Read VIIRS Cloud Mask product (CLDMSK_L2)
    Args:
        path (string): path to the desired file
    Returns:
        dict: datasets clear_conf and integer cloud mask as masked np-arrays
    """
    data = {}
    with Dataset(path, 'r') as file:
        data['clear_conf'] = file.groups['geophysical_data'].variables['Clear_Sky_Confidence'][::]
        data['cloud_mask'] = file.groups['geophysical_data'].variables['Integer_Cloud_Mask'][::]
    return data
