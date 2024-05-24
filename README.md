# viirs-tools

`viirs-tools` is a Python library that provides basic algorithms for retrieving meteorological data from VIIRS (Visible Infrared Imaging Radiometer Suite) satellite shots. This project started as a diploma (or thesis) project, and the primary goals of the `viirs-tools` library are threefold:

1. **Faster Data Processing**: The library aims to make the process of working with VIIRS data much quicker than the standard NASA approach. The goal is to provide near-real-time (NRT) data processing capabilities, allowing researchers and scientists to access and analyze the data in a more timely manner. However, it's important to note that this speed improvement may come at the cost of reduced accuracy, as the library's algorithms may not be as thoroughly tested and validated as the NASA's standard processing pipeline.

2. **Easier VIIRS Data Utilization**: In addition to the speed improvements, the library is designed to make it easier for researchers and scientists to work with VIIRS data.

3. **Flexible Data Handling**: One of the key aims of the `viirs-tools` library is to provide users with handy access to the underlying algorithms, allowing them to work with the data in a variety of formats, including `xr.Dataset`, `xr.DataArray`, and `np.ndarray`. This flexibility ensures that the library can be seamlessly integrated into a wide range of data processing workflows.


## Installation

To install `viirs-tools`, you can use pip:
```
 pip install viirs-tools 
```

If you want to use the `Assimilator` extra module, which allows you to download data from NASA servers:
``` 
pip install viirs-tools[assimilator]
 ```
Note that this module functions rely on the [cmrfetch](https://github.com/bmflynn/cmrfetch) package, you need to install and configure it first.


## Usage

The `viirs-tools` library provides the following core modules and their main functions:

1. **CloudMask**:
   + `rsnpp_day_img`: Day reflectance/thermal I-bands cloud test. [^1]
   + `fire_day_img`, `fire_night_img`: Day and night I-bands cloud tests used in the [^2].

2. **NightMask**:
   + `naive`: Day/night mask, based on the difference between presence of reflectance and thermal data, for both I- and M-bands

3. **Water**:
   + `water_bodies_day`: Day reflectance tests for water bodies from [^2]

4. **LST**:
   + `mono_window_i05`, `mono_window_m16`, `mono_window_m15`: LST retrieval for I05 band, based on the LANDSAT-8 alg [^3]

5. **Fires**:
   + `active_fires`: Active fire detection from [^2]

6. **Utils**:
   - Just some helpful functions

7. **Assimilator** submodule:
	1. **Assimilator**:
		- `assimilate`: Retrieving data from NASA archives using [cmrfetch](https://github.com/bmflynn/cmrfetch), with support for handy data collection process management
	2. **Reading**
		- `read_npp_viaes_l1`: Reading [VIIRS/NPP Imagery Resolution 6-Min L1 Swath SDR 375m](https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/products/NPP_VIAES_L1#product-information) product files
		- `read_npp_vmaes_l1`: Reading [VIIRS/NPP Moderate Resolution 6-Min L1 Swath SDR and GEO 750m](https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/products/NPP_VMAES_L1) product files
		- `read_npp_cldmsk_l2`: Reading [VIIRS/SNPP Cloud Mask 6-Min Swath 750m](https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/products/CLDMSK_L2_VIIRS_SNPP#product-information) product files
	3. **ReadingHelpers**
		- Contains some helper functions for reading files that aren't supported by `SatPy` module (some examples of using them in the previous module)


## Demo
You can find demo Qt6 app in the `viirs-demo` folder. Note that it requires additional packages to be installed installed - `rasterio`,  `matplotlib`,  `PyQt6` and `TensorFlow`. Run `viirs-demo.py` to start it. Data for this demo can be found in the `demo-data` folder.


## References
[^1]: M.Piper, T.Bahr (2015). A RAPID CLOUD MASK ALGORITHM FOR SUOMI NPP VIIRS IMAGERY EDRS.

[^2]: W.Schroeder, P.Oliva, L.Giglio, I.A.Csiszar (2014). The New VIIRS 375 m active fire detection data product: Algorithm description and initial assessment.

[^3]: U.Avdan, G.Jovanovska (2016). Algorithm for Automated Mapping of Land Surface Temperature Using LANDSAT 8 Satellite Data
