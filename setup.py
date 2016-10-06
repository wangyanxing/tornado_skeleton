#!/usr/bin/env python

from setuptools import setup, find_packages

__version__ = "0.1"

setup(
    name="bootcamp",
    version=__version__,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'bootcamp-web = bootcamp.bootcamp:serve_web',
        ]
    },
)
