# {{cookiecutter.project_name}}
{{cookiecutter.control_name}} control for Flet

## Installation

Add dependency to `pyproject.toml` of your Flet app:

* **Git dependency**

Link to git repository:

```
dependencies = [
  "{{cookiecutter.project_name}} @ git+https://github.com/MyGithubAccount/{{cookiecutter.project_name}}",
  "flet>={{cookiecutter.flet_version}}",
]
```

* **uv/pip dependency**

If the package is published on pypi.org:

```
dependencies = [
  "{{cookiecutter.project_name}}",
  "flet>={{cookiecutter.flet_version}}",
]
```

Build your app:
```
flet build macos -v
```

## Documentation

[Link to documentation](https://MyGithubAccount.github.io/{{cookiecutter.project_name}}/)
