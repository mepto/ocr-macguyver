#! /usr/bin/python
# coding: utf-8

from distutils.core import setup
import distutils.text_file
from pathlib import Path
from os import path
from typing import List


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


def parse_requirements(filename: str) -> List[str]:
    """Return requirements from requirements file."""
    # Ref: https://stackoverflow.com/a/42033122/
    return distutils.text_file.TextFile(
        filename=str(Path(__file__).with_name(filename))).readlines()


setup(
    name="macgyver",
    version="0.0.1dev",
    packages=["macgyver"],
    package_dir={'macgyver': 'macgyver'},
    long_description=long_description,
    install_requires=parse_requirements("requirements.txt"),
    python_requires=">=3.5",
    entry_points={
        'console_scripts': [
            'macgyver=macgyver/__init__:main',
        ],
    },
)
