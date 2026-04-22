# TablePlus DB URLs

![Coverage](https://img.shields.io/badge/coverage-98.96%25-brightgreen)

## Overview

Generate TablePlus DB URLs from CookieCutter Django to make setting up connections easier.

Plays nice with [cookiecutter-django](https://github.com/cookiecutter/cookiecutter-django).

## Installation

Core/library install:

```bash
uv add tableplus-db-urls
```

CLI install:

```bash
uv add "tableplus-db-urls[cli]"
```

## Usage

The `--path` parameter should be your Django project root.

```bash
tableplus generate --path "." --name "DB Name" --ssh-user "user" --ssh-host "127.0.0.1"
```

> **NOTE:** For help run `tableplus --help` or for command help run `tableplus generate --help`.

In TablePlus, right-click and choose `New` > `Connection from URL...` and paste the generated URL.

## Development

```bash
just --list
just env
just pip-install-editable
```

## Testing

```bash
just pytest
just coverage
just open-coverage
```

For quick local quality checks:

```bash
just check
```

## Issues

If you experience any issues, please create one in the
[issue tracker](https://bitbucket.org/xstudios/tableplus-db-urls/issues).
