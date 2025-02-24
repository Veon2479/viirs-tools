import numpy as np

from viirs_tools.utils.types import ArrayLike, _check_data


def ndvi(nir: ArrayLike, r: ArrayLike) -> ArrayLike:
    """
        Get NDVI index from reflectance bands
        Most common use is (I2, I1) or (M7, M5) as (NIR, R)
    Args:
        nir : ArrayLike
            near-infrared reflectance band
        r : ArrayLike
            red reflectance band
    Returns:
        ArrayLike: NDVI index for each pixel,
            can contain NaN values
    """
    _check_data(nir, r)

    return (nir - r) / (nir + r)
