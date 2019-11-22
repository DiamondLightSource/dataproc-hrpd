from setuptools import setup, find_packages

setup(
    name="hrpdrebin",
    version="1.0",
    description='High-resolution powder diffraction rebin',
    author="Peter Chang",
    author_email="scientificsoftware@diamond.ac.uk",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.7",
    ],
    packages=find_packages(),
    install_requires=['numpy>=1.6', 'scisoftpy>=2.16'],
    entry_points={'console_scripts': ['rebin = rebin.maincmd:main'],
                    'gui_scripts': ['rebin-gui = rebin.mainui:main']},
    url='https://github.com/DiamondLightSource/python-hrpd-rebin',
)
