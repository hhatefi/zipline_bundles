import os
from setuptools import setup, find_packages

setup(
    name="zipline_bundles",
    version="0.1",
    packages=[".", "zipline-bundles"],
    entry_points = {
        'console_scripts': ['zipline-bundles-install=install:main'],
    },
    install_requires=[
        'yahoofinancials',
        'iexfinance',
        'python-binance',
        'logbook',
   ]
)
