from __future__ import annotations

from enum import Enum
from typing import Any, Union

import numpy as np
import xarray as xr


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

    return all(not (type(arg) is not target_type or arg.shape != target_shape) for arg in args[1:])


class AlgEnum(Enum):
    pass
