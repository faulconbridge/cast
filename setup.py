#!/usr/bin/env python

import os
from setuptools import setup, find_packages

VERSION = '0.0.0'

REQUIRES = ['PyYAML']

setup(
    name='Cast',
    version=VERSION,
    package_dir={'': 'lib'},
    packages=find_packages('lib'),
    data_files=[
        '~/.castrc',
        '~/.cast/hosts.json'
    ],
    entry_points={
        'console_scripts': [
          'cast=cast.cast:main',
        ],
    },
    author='Christopher Wetherill',
    author_email='cast@tbmh.org',
    license='AGPLv3',
    platforms=['GNU/Linux', 'BSD', 'MacOSX'],
    description='Cluster management utility',
    long_description=open('doc/txt/cast.rst').read(),
    url='https://github.com/faulconbridge/cast',
    install_requires=REQUIRES
)
