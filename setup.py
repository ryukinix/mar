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
import mar

here = path.abspath(path.dirname(__file__))
readme = path.join(here, 'README.md')

with open(readme, encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    install_requires = list(map(str.strip, f.readlines()))

setup(
    name=mar.__name__,
    version=mar.__version__,
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
    keywords='mar memory analysis pandas table stats',
    author=mar.__author__,
    author_email=mar.__email__,
    url=mar.__url__,
    zip_safe=False,
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples',
                                    'tests', 'docs', '__pycache__']),
    platforms='unix',
    install_requires=install_requires,
    entry_points={  # no entry-points yet
        'console_scripts': [
            'mar = mar.main:main'
        ]  # mar -> memory-analysis-report
    },
)
