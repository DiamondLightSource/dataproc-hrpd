from setuptools import setup, find_packages

install_deps = ['numpy>=1.6', 'scisoftpy>=2.16']
try:
    import PySide
except ImportError:
    install_deps.append('PyQt4>=4')

setup(
    name = "hrpd_rebin",
    version = "0.9",
    packages = find_packages(),
    install_requires = install_deps,
    entry_points = {'console_scripts': ['rebin = rebin.maincmd:main'],
                    'gui_scripts': ['rebin-gui = rebin.mainui:main']},
)
