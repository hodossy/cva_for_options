#!/usr/bin/python

from setuptools import setup

setup(name='option_pricer',
      version='0.1.0',
      packages=['option_pricer'],
      entry_points={
          'console_scripts': [
              'option_pricer = option_pricer.__main__:main'
          ]
      },
      install_requires=[
          'numpy'
      ],
      zip_safe=False)