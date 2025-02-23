from viirs_tools.utils.types import ArrayLike, _check_data


def ndvi(nir: ArrayLike, r: ArrayLike) -> ArrayLike:
    """Get Normalized Difference Vegetation Index from reflectance bands
    Most common use is (I2, I1) or (M7, M5) as (NIR, R)

    Args:
        nir : near-infrared reflectance band
        r : red reflectance band

    Returns:
        NDVI index for each pixel, can contain NaN values
    """
    _check_data(nir, r)

    return (nir - r) / (nir + r)


def ndsi(ri1: ArrayLike, ri3: ArrayLike) -> ArrayLike:
    """Get Normalized Difference Snow Index from I01 and I03 reflectance bands

    Args:
        ri1 : I01 in reflectance calibration
        ri3 : I03 in reflectance calibration

    Returns:
        NDVI index for each pixel, can contain NaN values
    """
    _check_data(ri1, ri3)

    return (ri1 - ri3) / (ri1 + ri3)
