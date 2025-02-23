import numpy as np
import xarray as xr

IMAGE_SHAPE = (3, 3)


def get_data_np(shape):
    def _get_band(shape):
        return np.random.rand(*shape) * 100

    mask = _get_band(shape) < 50
    ri1 = _get_band(shape)
    ri2 = _get_band(shape)
    ri3 = _get_band(shape)
    bi4 = _get_band(shape)
    bi5 = _get_band(shape)

    ri1[mask] = np.nan
    ri2[mask] = np.nan
    ri3[mask] = np.nan
    bi4[mask] = np.nan
    bi5[mask] = np.nan

    return ri1, ri2, ri3, bi4, bi5


def _np2xr(arr):
    dims = ("time", "x", "y") if len(arr.shape) == 3 else ("x", "y")
    coords = {"x": np.arange(arr.shape[-2]), "y": np.arange(arr.shape[-1])}
    if len(arr.shape) == 3:
        coords["time"] = np.arange(arr.shape[0])
    return xr.DataArray(arr, dims=dims, coords=coords)


def get_data_xr(shape):
    ri1, ri2, ri3, bi4, bi5 = get_data_np(shape)

    return (
        _np2xr(ri1),
        _np2xr(ri2),
        _np2xr(ri3),
        _np2xr(bi4),
        _np2xr(bi5),
    )


def get_np_from_list(data: list) -> np.ndarray:
    image = np.array(data)
    dims = len(image.shape)
    assert 1 <= dims < 3
    if len(image.shape) == 1:
        image = image[..., None]
    return image


def get_np_seq_from_list(data: list, layers: int = 3) -> np.ndarray:
    layer = get_np_from_list(data)
    return np.stack(layers * [layer])


def get_xr_from_list(data: list) -> xr.DataArray:
    return _np2xr(get_np_from_list(data))


def get_xr_seq_from_list(data: list, layers: int = 3) -> xr.DataArray:
    return _np2xr(get_np_seq_from_list(data, layers=layers))
