
from setuptools import setup, find_packages

setup(
    name = "High-resolution powder diffraction",
    version = "0.9",
    packages = find_packages(),
    install_requires = ['numpy>=1.6', 'pyside>=1.2'],
    entry_points = {'console_scripts': ['rebin = rebin.maincmd:main'],
                    'gui_scripts': ['rebin-gui = rebin.mainui:main']},
)
