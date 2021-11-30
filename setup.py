# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='sudoku',
    version='0.1.0',
    description='Parallel Sudoku Solver',
    long_description=readme,
    author='Mahmoud Komaiha, Ning Lu',
    author_email='mkomaiha@umich.edu, ninglu@umich.edu',
    url='https://github.com/mkomaiha/NERS570-Sudoku',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
