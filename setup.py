from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

with open('LICENSE', 'r') as f:
    license_text = f.read()

setup(
    name='viirs-tools',
    description='Python library for processing VIIRS data',
    long_description_content_type='text/markdown',
    long_description=long_description,
    url='https://github.com/Veon2479/viirs-tools',
    license=license_text,
    author='Andrey Shuliak',
    version='1.0.1',
    packages=find_packages(),
    install_requires=[
        'xarray',
    ],
    extras_require={
        'assimilator': ['netcdf4']
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Scientific/Engineering :: Atmospheric Science'
    ],
    keywords=['viirs', 'satellite', 'remote sensing', 'meteorology'],

)
