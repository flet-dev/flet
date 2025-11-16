# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [0.2.0] - Unreleased

## Added

- Deployed online documentation: https://docs.flet.dev/datatable2/
- New enums: `DataColumnSize`

### Changed

- Refactored all controls to use `@flet.control` dataclass-style definition.
- Additionally, they are now all based on their flet counterparts:
    - `DataTable2` is now based on `flet.DataTable`
    - `DataColumn2` is now based on `flet.DataColumn`
    - `DataRow2` is now based on `flet.DataRow`

## [0.1.0] - 2025-03-16

Initial release.


[0.2.0]: https://github.com/flet-dev/flet-datatable2/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/flet-dev/flet-datatable2/releases/tag/0.1.0
