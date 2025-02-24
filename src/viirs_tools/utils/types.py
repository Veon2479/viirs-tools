import numpy as np
import xarray as xr

from enum import Enum
from typing import Any, TypeVar, Union


ArrayLike = Union[np.ndarray, xr.DataArray]


def _check_data(*args: Any):
    if len(args) == 0:
        return True

    if type(args[0]) is not ArrayLike:
        return False

    if len(args) == 1:
        return True

    target_type = type(args[0])
    target_shape = args[0].shape

    for arg in args[1:]:
        if type(arg) is not target_type or arg.shape != target_shape:
            return False

    return True


class AlgEnum(Enum):
    pass
