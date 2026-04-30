# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2026-05-01

### Added
- **Git Shortcuts**: New module for automated Git workflow management.
- **ftwchangelog**: CLI tool for generating formatted changelogs.
- **Inheritance Diagrams**: Visual documentation support for CLI parsers and protocols.

### Changed
- **Documentation**: Overhauled `index.rst` and restructured 'Getting Started' guides.
- **README**: Added CLI tool descriptions and architecture overview.
- **Refactoring**: Cleaned up `programms.py` for better readability (adhering to 75-line limit).

### Fixed
- **Test Coverage**: Achieved 100% coverage by adding version-specific excludes for Python 3.11.
- **Environment Isolation**: Improved XDG path cleanup in `tox` to ensure isolated test runs.
- **CLI Robustness**: Replaced `sys.exit` with `ArgumentError` in `cli_parser.py` for improved testability.

## [0.1.0] - 2026-04-25

### Added
- Project documentation (README, Changelog, and Sphinx index).

## [0.0.1] - 2026-04-24

### Added
* Initial release of the `ftw-devtools` package.
* Introduced `TestHomeEnvironment` as a Testing Infrastructure Utility for physical filesystem sandboxing.
* Implemented PEP 420 namespace structure under `fitzzftw.devtools`.
* Added automated coverage reporting and Sphinx documentation boilerplate.
