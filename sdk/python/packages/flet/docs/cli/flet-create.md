---
title: flet create
---

The `flet create` command scaffolds a new Flet project using a predefined template. It sets up the initial directory structure, metadata, and required files to help you get started quickly.

## Usage

```
flet create [OPTIONS] [OUTPUT_DIRECTORY]
```

## Arguments

### `OUTPUT_DIRECTORY`

Directory where the new Flet project will be created.  
If omitted, the project is created in the current directory.

## Options

### `--project-name PROJECT_NAME`

Name of the new Flet project. This will be used in metadata files such as `pyproject.toml`.

### `--description DESCRIPTION`

Short description of the new Flet project. This will appear in generated metadata.

### `--template {app,extension}`

Type of project to create:

- `app`: Standard Flet application (default)
- `extension`: Flet extension project

### `--template-ref TEMPLATE_REF`

Git reference (branch, tag, or commit ID) of the Flet templates repository to use.  
Useful when using a custom or development version of templates.

### `--help`, `-h`

Show help information and exit.

### `--verbose`, `-v`

Enable verbose output. Use `-v` for standard verbose logging and `-vv` for even more detailed output.