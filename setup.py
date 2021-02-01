#!/usr/bin/env python

import os
import toml
from setuptools import setup, find_packages


REQUIREMENTS_FILE = 'requirements.txt'
README_FILE = 'README.md'
PYPROJECT_FILE = 'pyproject.toml'
SETUP_KWARGS = [
    'name',
    'version',
    'description',
    'author',
    'authors',
    'author_email',
    'license',
    'url',
    'project_urls',
    'download_url',
    'keywords',
    'classifiers',
    'packages',
    'include',
    'extras_require',
    'include_package_data',
    'python_requires',
    'entry_points',
]
INCLUDE = ['pyproject.toml', 'init.py']
EXCLUDE_PACKAGE = ['tests*']


def get_requirements():
    """Build the requirements list for this project"""
    requirements_list = []

    if not os.path.isfile(REQUIREMENTS_FILE):
        # Check if requirements file did not exist.
        return requirements_list

    with open(REQUIREMENTS_FILE) as reqs:
        for install in reqs:
            requirements_list.append(install.strip())

    return requirements_list

def get_setup_kwargs(default=None):
    """Get setup kwargs"""
    with open(README_FILE, 'r', encoding='utf-8') as fd:
        kwargs = dict(
            long_description=fd.read(),
            install_requires=get_requirements(),
            include=INCLUDE,
            packages=find_packages(exclude=EXCLUDE_PACKAGE),
        )

    if isinstance(default, dict):
        kwargs.update(default)

    pyproject = toml.load(PYPROJECT_FILE)

    for k, v in dict(pyproject['tool']['poetry']).items():
        if k in SETUP_KWARGS:
            if k not in kwargs:
                kwargs[k] = v
                continue
            if isinstance(kwargs[k], list):
                kwargs[k].extend(v)
            elif isinstance(kwargs[k], dict):
                kwargs[k].update(v)

    return kwargs


def main():
    setup(**get_setup_kwargs())


if __name__ == '__main__':
    main()
