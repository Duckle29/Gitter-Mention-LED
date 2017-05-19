#!/usr/bin/env python3

from distutils.core import setup
from setuptools import find_packages


with open("README.rst") as readme:
    long_description = readme.read()


setup(
    name='gitterest',
    version=0.1,
    description='A simple gitter API wrapper inspired by gitterpy.',
    author='Alex Hiam, Lasse Schuirmann',
    author_email='lasse.schuirmann@gmail.com',
    maintainers={'Lasse Schuirmann'},
    packages=find_packages(exclude=["build.*", "tests", "tests.*"]),
    url='https://gitlab.com/coala/gitterest',
    long_description=long_description,
)
