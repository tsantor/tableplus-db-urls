# History

All notable changes to this project will be documented in this file. This project adheres to [Semantic Versioning](http://semver.org/).

## 0.2.0 (2026-04-22)

- Modernized project packaging/tooling baseline:
  - Python `>=3.11`
  - `hatchling` build backend
  - `Justfile`, `tox.ini`, and CI parity configuration
  - updated lint/test/release workflows with `uv` + `ruff` + `pytest`
- Updated dependency model:
  - `click` moved to optional `cli` extra for consumers
  - `click` added to test dependency group for CLI test execution
- Added CLI test coverage for command help, required options, successful URL output, and error scenarios.
- Improved CLI error UX by surfacing friendly configuration errors instead of raw `KeyError` tracebacks.
- Refactored internals to a lightweight DDD structure (`domain`, `application`, `infrastructure`) and removed `tableplus.core` module path.

## 0.1.4 (2024-05-15)

- Too quick on the trigger! Bug fix with CLI implementation after `name` added.

## 0.1.3 (2024-05-15)

- Bug fix with CLI implementation after `name` added.

## 0.1.2 (2024-05-15)

- Added `name` argument to name the connection.

## 0.1.1 (2024-04-23)

- Moved from `argparse` to `click`
- Moved from `python-environ` to `python-dotenv`
- Fixed bug with production URL

## 0.1.0 (2024-04-09)

- First release
