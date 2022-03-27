# Flet - build real-time multi-platform apps in the language you know

__Flet__ is the next iteration of [Pglet](https://github.com/pglet/pglet) project.

Pglet demonostrated there is a strong interest to write web apps in Python.

## Why new project?

Pglet is for web apps and is based on Fluent UI React components.

Flet is for web, desktop and mobile platforms and is based on Flutter.

A lot of renamings would create a mess in a project repo - it's easier to start over in a new repository.

A lot of functionality was added to support Bash: a custom protocol via named pipes with commands serialization/deserialization, CLI support with `pglet page` and `pglet app` commands. It's not necessary anymore with high level languages such like Python which communicate with Flet server via WebSockets directly.

With Flet we are switching to monorepo storing Flet server, Flutter client and all language bindings (SDKs). Every CI build and release creates the same, unique version for all the apps and components.

## Why changing name?

* Confusing name. It's been almost a year and I haven't used to the name yet. Is it a "page-let", "p-g-let" or "piglet"? Is there connection to "PostgreSQL" or Paul Graham? On the other hand "flet" is short, simple and easy to pronounce.