#!/usr/bin/env python
# coding=utf-8
#
#   Python Script
#
#   Copyright © Manoel Vilela
#
#

from setuptools import setup, find_packages
from codecs import open  # To use a consistent encoding
from os import path
import mreport

here = path.abspath(path.dirname(__file__))
readme = path.join(here, 'README.md')

with open(readme, encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    install_requires = list(map(str.strip, f.readlines()))

setup(
    name=mreport.__name__,
    version=mreport.__version__,
    description="A tool stats parser whose report the of dump memory analysis",
    long_description=long_description,
    classifiers=[
        "Environment :: Console",
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='mreport memory analysis pandas table stats',
    author=mreport.__author__,
    author_email=mreport.__email__,
    url=mreport.__url__,
    zip_safe=False,
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples',
                                    'tests', 'docs', '__pycache__']),
    platforms='unix',
    install_requires=install_requires,
    entry_points={  # no entry-points yet
        'console_scripts': [
            'mar = mreport.cli:main'
        ]  # mar -> memory-analysis-report
    },
)
