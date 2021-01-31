#!/usr/bin/env python
"""This script will setup"""

import argparse
import os
import re
import shutil

BASE_DIR = os.getcwd()

NAME = 'github-poetry-starter'
SNAME = 'github_poetry_starter'
VERSION = "0.1.0"
DESCRIPTION = "GitHub Actions starter for python with python-poetry"
AUTHOR = 'hexatester'
EMAIL = 'hexatester@protonmail.com'

PDIR = os.path.join(BASE_DIR, 'github_poetry_starter')
TFILE = os.path.join(BASE_DIR, 'tests', 'test_github_poetry_starter.py')


def snake_case(text):
    return text.lower().replace(' ', '_')


def kebab_case(text):
    return text.lower().replace(' ', '-')


def remove(path):
    """param <path> could either be relative or absolute."""
    # thanks https://stackoverflow.com/a/41789397
    if os.path.isfile(path) or os.path.islink(path):
        os.remove(path)  # remove the file
    elif os.path.isdir(path):
        shutil.rmtree(path)  # remove dir and all contains
    else:
        raise ValueError("file {} is not a file or dir.".format(path))


parser = argparse.ArgumentParser(description='Setup Poetry Starter.')

parser.add_argument('--name', dest='name', help='Project name', required=True)
parser.add_argument('--version', dest='version', help='Project version', default=VERSION)
parser.add_argument('--description', dest='description', help='Project description', required=True)
parser.add_argument('--author', dest='author', help='Author name / username', required=True)
parser.add_argument('--author-email', dest='email', help='Author-email', required=True)

parser.add_argument('--module', dest='module', action='store_true')
parser.add_argument('--no-module', dest='module', action='store_false')
parser.set_defaults(module=True)


args = parser.parse_args()

if args.module:
    NS_NAME = snake_case(args.name)
    NDIR = os.path.join(BASE_DIR, NS_NAME)
    TNFILE = os.path.join(BASE_DIR, 'tests', f'test_{NS_NAME}.py')

    if os.path.isdir(PDIR):
        os.rename(PDIR, NDIR)

    if os.path.isfile(TFILE):
        os.rename(PDIR, TNFILE)

    with open(TNFILE, 'r+') as f:
        text = f.read()
        text = re.sub(SNAME, NS_NAME, text)
        f.seek(0)
        f.write(text)
        f.truncate()
else:
    remove(PDIR)
    remove(TFILE)
    with open('setup.py', 'w+') as f:
        f.write("#!/usr/bin/env python\n")


with open('pyproject.toml', 'r+') as f:
    text = f.read()
    text = re.sub(NAME, kebab_case(args.name), text)
    text = re.sub(VERSION, args.version, text)
    text = re.sub(DESCRIPTION, args.description, text)
    text = re.sub(AUTHOR, args.author, text)
    text = re.sub(EMAIL, args.email, text)
    f.seek(0)
    f.write(text)
    f.truncate()


with open('setup.py', 'r+') as f:
    text = f.read()
    text = re.sub(", 'init.py'", '', text)
    f.seek(0)
    f.write(text)
    f.truncate()

print("Please delete init.py file")
