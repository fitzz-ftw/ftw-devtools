# Changelog

All notable changes to this project will be documented in this file.

## [0.3.2] - 2026-06-19

### Added
- Add documentation for doctest utilities and git program guides
- Add coverage test database assets

### Changed
- Restructure git logging and development infrastructure
- Update pyproject.toml and core testinfra components
- Refactor doctest_utils and git shortcut command modules
- Update git-commands test suite

### Removed
- Delete deprecated coverage_script.py

## [0.3.1] - 2026-06-17

### Added
- Expand test infrastructure and utility scripts
- Add doctest_utils.py to devtools core
- Implement updates for testinfra API

### Changed
- Optimize testinfra and CLI scripts for better performance
- Update pyproject.toml metadata and dependencies
- Refactor coverage_script.py logic

### Removed
- Delete temporary git-diff-devtools.txt file


## [0.3.0] - 2026-05-16

### Added
- `TestHomeEnvironment` now supports `appname` and `appauthor` as instance properties for platform-independent path resolution (crucial for Windows systems).
- Automatic creation of missing parent directories (`mkdir -p`) within `copy2cwd()` and `cwd2doc_inc()` methods.
- New `TestHomeEnvironment.clean_output()` method to programmatically purge the test sandbox output directory.

### Changed
- **Breaking Change (API Refactoring):** The `copy2config()`, `copy2data()`, and `copy2cache()` methods no longer accept an explicit application name parameter, relying on the centralized instance properties instead.
- Renamed documentation and CLI reference files for Git shortcuts from `ftw_changelog` to `cli_ftw_changelog`.

### Fixed
- Stabilized CI test execution by introducing a dedicated `tox -e ci` target to prevent the test runner from processing local `*.noci.rst` documentation examples.

## [0.2.1]

### Fixed
- **Documentation**: Fixed wrong filename.


## [0.2.0] - 2026-05-01

### Removed
- **TestHomeEnvironment**: Die Property `input_readonly` wurde vollständig entfernt, da sie 
    unter Windows für Verzeichnisse unzuverlässig ist und bei einem `fail-fast` Testabbruch das 
    saubere Löschen der Testverzeichnisse blockierte.

### Added
- **Git Shortcuts**: New module for automated Git workflow management.
- **ftwchangelog**: CLI tool for generating formatted changelogs.
- **Inheritance Diagrams**: Visual documentation support for CLI parsers and protocols.

### Changed
- **Documentation**: Overhauled `index.rst` and restructured 'Getting Started' guides.
- **README**: Added CLI tool descriptions and architecture overview.
- **Refactoring**: Cleaned up `programms.py` for better readability (adhering to 75-line limit).

### Fixed
- **CI/Windows**: Die Stabilität der GitHub-Runner wurde durch den Einsatz von radikalen Ellipsis
    (`...`) in den Doctest-Tracebacks sichergestellt, um absolute, systemspezifische Pfade 
    zu neutralisieren.
- **TestHomeEnvironment**: Die Plattformkompatibilität unter Windows wurde durch die Umstellung 
    von `os.chmod` auf `Path.chmod` verbessert, bevor die Logik final entfernt wurde.
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
