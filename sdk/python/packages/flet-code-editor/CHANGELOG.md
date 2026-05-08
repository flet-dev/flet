# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## 0.85.0

### Added

- `issues` property on `CodeEditor` for displaying code analysis error markers in the gutter, along with new `Issue` and `IssueType` types. Analysis is performed on the Python side via `on_change` and pushed to the editor.

### Fixed

- `CodeEditor` background not filling the entire area when `expand=True`.

## 0.1.0

Initial release.
