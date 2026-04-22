set shell := ["bash", "-cu"]

# List all available recipes
default:
  @just --list

# -----------------------------------------------------------------------------
# Variables
# -----------------------------------------------------------------------------

python_version := "3.12"
aws_profile := "xstudios"
s3_bucket := "xstudios-pypi"
package_name := "tableplus"
cov_fail_under := "90"

# Dynamic variables (evaluated at runtime - DO NOT EDIT)
wheel_name := `basename $(ls dist/*.whl 2>/dev/null | head -n 1) 2>/dev/null || echo ""`
package_url := "https://" + s3_bucket + ".s3.amazonaws.com/" + wheel_name

# Show variable values
[group('help')]
show-vars:
  @echo "Python Version: {{python_version}}"
  @echo "AWS Profile: {{aws_profile}}"
  @echo "S3 Bucket: {{s3_bucket}}"
  @echo "Coverage Fail Under: {{cov_fail_under}}"
  @echo "Package Name: {{package_name}}"
  @echo "Wheel Name: {{wheel_name}}"
  @echo "Package URL: {{package_url}}"

# -----------------------------------------------------------------------------
# Environment
# -----------------------------------------------------------------------------

[group('environment')]
env:
  uv venv --python {{python_version}}

[group('environment')]
env-remove:
  rm -rf .venv/

[group('environment')]
env-recreate: env-remove env pip-install-editable

# -----------------------------------------------------------------------------
# Pip
# -----------------------------------------------------------------------------

[group('uv')]
pip-install-editable:
  uv sync --all-groups
  uv pip install -e .

[group('uv')]
uv-add-dev-dependencies:
  uv add twine hatch xapp-tools ruff pre-commit --group dev

[group('uv')]
uv-add-test-dependencies:
  uv add pytest-cov pytest-mock tox-uv --group test

[group('uv')]
pip-list:
  uv pip list

[group('pip')]
pip-tree:
  uv pip tree

[group('uv')]
uv-sync:
  uv sync

[group('uv')]
uv-install-dev:
  uv sync --no-default-groups --group test --group dev

[group('uv')]
uv-lock:
  uv lock

[group('uv')]
uv-lock-upgrade:
  uv lock --upgrade

[group('uv')]
uv-lock-check:
  uv lock --check

# -----------------------------------------------------------------------------
# Testing
# -----------------------------------------------------------------------------

[group('testing')]
pytest:
  uv run pytest -vx --cov={{package_name}} --cov-report=html

[group('testing')]
pytest-verbose:
  uv run pytest -vvs --cov={{package_name}} --cov-report=html

[group('testing')]
coverage:
  uv run pytest -q --cov={{package_name}} --cov-report=term --cov-report=html

[group('testing')]
coverage-verbose:
  uv run pytest -vs --cov={{package_name}} --cov-report=term --cov-report=html

[group('testing')]
coverage-skip:
  uv run pytest -vs --cov={{package_name}} --cov-report=term:skip-covered --cov-report=html

[group('testing')]
pytest-cov-gate:
  uv run pytest -q --cov={{package_name}} --cov-report=term --cov-fail-under={{cov_fail_under}}

[group('testing')]
open-coverage:
  open htmlcov/index.html

[group('testing')]
tox:
  uv run tox

# -----------------------------------------------------------------------------
# Linting
# -----------------------------------------------------------------------------

[group('linting')]
ruff-format:
  uv run ruff format

[group('linting')]
ruff-check:
  uv run ruff check

[group('linting')]
ruff-check-fix:
  uv run ruff check --fix

[group('linting')]
ruff-clean:
  uv run ruff clean

# -----------------------------------------------------------------------------
# Workflow
# -----------------------------------------------------------------------------

[group('workflow')]
check: uv-lock-check ruff-check pytest-cov-gate

[group('workflow')]
fix: ruff-format ruff-check-fix check

[group('workflow')]
ci: release-check

[group('workflow')]
doctor:
  uv --version
  uv run python --version
  uv pip list --strict
  uv lock --check

[group('workflow')]
outdated:
  uv tree --outdated --all-groups

# -----------------------------------------------------------------------------
# Cleanup
# -----------------------------------------------------------------------------

[group('cleanup')]
clean-build:
  rm -fr build/ dist/ .eggs/
  find . -name '*.egg-info' -o -name '*.egg' -exec rm -fr {} +

[group('cleanup')]
clean-pyc:
  find . \( -name '*.pyc' -o -name '*.pyo' -o -name '*~' -o -name '__pycache__' \) -exec rm -fr {} +

[group('cleanup')]
clean: clean-build clean-pyc

[group('cleanup')]
clean-pytest-cache:
  rm -rf .pytest_cache

[group('cleanup')]
clean-ruff-cache:
  rm -rf .ruff_cache

[group('cleanup')]
clean-tox-cache:
  rm -rf .tox

[group('cleanup')]
clean-coverage:
  rm .coverage
  rm -rf htmlcov

[group('cleanup')]
clean-tests: clean-pytest-cache clean-ruff-cache clean-tox-cache clean-coverage

[group('cleanup')]
clean-all: clean clean-tests

# -----------------------------------------------------------------------------
# Miscellaneous
# -----------------------------------------------------------------------------

[group('misc')]
tree:
  tree src -I '__pycache__'

[group('misc')]
tree-root:
  tree -I '.tmp|.coverage|htmlcov|dist|build|.eggs|*.egg-info|__pycache__|.pytest_cache|.ruff_cache|.tox|.vscode|node_modules|*.csv'

# -----------------------------------------------------------------------------
# Deploy
# -----------------------------------------------------------------------------

[group('deploy')]
dist: clean
  uv run hatch build

[group('deploy')]
metadata:
  uv run hatch project metadata

[group('deploy')]
release-check: ruff-check pytest-cov-gate twine-check

[group('deploy')]
twine-upload-test: dist
  uv run twine upload dist/* -r pypitest

[group('deploy')]
twine-upload: dist
  uv run twine upload dist/*

[group('deploy')]
twine-check: dist
  uv run twine check dist/*

[group('deploy')]
twine-fix:
  uv pip install -U twine pkginfo

# -----------------------------------------------------------------------------
# X Studios S3 PyPi
# -----------------------------------------------------------------------------

[group('s3')]
push-to-s3:
  aws s3 sync --profile={{aws_profile}} --acl public-read ./dist/ s3://{{s3_bucket}}/ \
    --exclude "*" --include "*.whl"
  echo "{{package_url}}"
