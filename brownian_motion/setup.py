#!/usr/bin/python

from setuptools import setup

setup(name='brownian_motion',
      version='0.1.0',
      packages=['brownian_motion'],
      install_requires=[
          'numpy',
          'pandas'
      ],
      zip_safe=False)