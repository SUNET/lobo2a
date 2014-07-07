#!/usr/bin/env python

import os

from setuptools import setup, find_packages

__author__ = 'leifj'

here = os.path.abspath(os.path.dirname(__file__))
README_fn = os.path.join(here, 'README.rst')
README = 'aria2c-based lobo2 storage node'
if os.path.exists(README_fn):
    README = open(README_fn).read()

version = '0.1dev'

install_requires = [
    'requests'
]

testing_extras = [
    'nose==1.2.1',
    'nosexcover==1.0.8',
    'coverage==3.6',
]

setup(
    name='lobo2a',
    version=version,
    description="aria2c-based lobo2 storage node",
    long_description=README,
    classifiers=[
        # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords='aria2 bittorrent storage',
    author='Leif Johansson',
    author_email='leifj@sunet.se',
    url='http://blogs.mnt.se',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    package_data={
    },
    entry_points={
        'console_scripts':
            ['lobo2a=lobo2a:main']
    },
    zip_safe=False,
    install_requires=install_requires,
    extras_require={
        'testing': testing_extras,
    },
    test_suite='lobo2a',
)
