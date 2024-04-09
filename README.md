# TablePlus DB URLS

## Overview
Generate TablePlus DB URLs from CookieCutter Django to make setting up connections easier.

The current version is self-serving (meaning, aimed at me the intended user of this tool) at the moment. However, if you see value in it, we can adopt it to be more flexible.

It assumes you are using `django-cookiecutter` with the `use_docker=y` option and that you are connecting to your Postgres DB over SSH using your private key (`~/.ssh/config`) in production.

## Installation
```bash
pip install tableplus-db-urls
```

## Usage
```bash
$ tableplus --path="." --user="user" --host="xxx.xxx.x.x"
```

## Development
```bash
make env
make pip_install
python3 -m pip install -e .
```

## Testing
```bash
make pytest
make coverage
make open_coverage
```

## Issues

If you experience any issues, please create an [issue](https://github.com/tsantor/tableplus-db-urls/issues) on Bitbucket.
