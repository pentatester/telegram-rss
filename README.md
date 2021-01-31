# Github Poetry Starter

GitHub Actions starter for python with [python-poetry](https://github.com/python-poetry/poetry "Python packaging and dependency management made easy").

The [complete documentation](https://python-poetry.org/docs/ "Poetry documentation") of python-poetry is available on the [official website](https://python-poetry.org "Poetry official website").

- [Github Poetry Starter](#github-poetry-starter)
  - [Usage](#usage)
  - [Bumps version](#bumps-version)
  - [Publish to pypi](#publish-to-pypi)
    - [Publish localy](#publish-localy)
    - [Publish with github action](#publish-with-github-action)
  - [Dependency](#dependency)
    - [Update dependencies](#update-dependencies)
    - [Install dependency](#install-dependency)
    - [Remove dependency](#remove-dependency)
    - [Export requirements.txt](#export-requirementstxt)

## Usage

- [Use this template](https://github.com/pentatester/github-poetry-starter/generate "Use github-poetry-starter as template")
- [Install poetry](https://python-poetry.org/docs/#installation "Poetry Installation documentation")
- Run `poetry install --no-root`
- Run `python init.py`
- You Finished, happy coding!

## Bumps version

Bumps the version of the project and writes the new version back to `pyproject.toml` if a valid bump rule is provided.

```bash
poetry version minor
```

The new version should ideally be a valid semver string or a valid bump rule: `patch`, `minor`, `major`, `prepatch`, `preminor`, `premajor`, `prerelease`.

## Publish to pypi

You need to have [PyPI](https://pypi.org/ "PyPI - Python Package Index") account.

### Publish localy

```bash
poetry publish --build
```

### Publish with github action

Add `PYPI_USERNAME` and `PYPI_PASSWORD` to your Actions secrets, [learn more](https://docs.github.com/actions/automating-your-workflow-with-github-actions/creating-and-using-encrypted-secrets "Encrypted secrets").

Then [create a release](https://docs.github.com/en/github/administering-a-repository/managing-releases-in-a-repository#creating-a-release "Managing releases in a repository, Creating a release").

You need to create a release everytime bump to the new version.

## Dependency

### Update dependencies

```bash
poetry update
```

### Install dependency

```bash
poetry add requests
```

For dev requirement

```bash
poetry add requests --dev
```

### Remove dependency

```bash
poetry remove requests
```

For dev requirement

```bash
poetry remove requests --dev
```

### Export requirements.txt

`-o` for output.

```bash
poetry export -f requirements.txt -o requirements.txt --without-hashes
```

For dev requirements

```bash
poetry export -f requirements.txt -o requirements-dev.txt --dev --without-hashes
```
