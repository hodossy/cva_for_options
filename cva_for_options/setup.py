#!/usr/bin/python

from setuptools import setup

setup(name='cva_for_options',
      version='0.1.0',
      packages=['cva_for_options'],
      entry_points={
          'console_scripts': [
              'cva_for_options = cva_for_options.__main__:main'
          ]
      },
      install_requires=[
          'numpy'
      ],
      zip_safe=False)