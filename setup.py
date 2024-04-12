from setuptools import setup, find_packages

setup(
    name='viirs-tools',
    description='Python library for processing VIIRS data',
    author='Andrey Shuliak',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'xarray',
    ],
    extras_require={
        'assimilator': ['netcdf4']
    }
)
