---
slug: flet-versioning-and-pre-releases
title: Flet versioning and pre-releases
authors: feodor
tags: [news]
---

Flet is a fast-evolving framework with a new functionality and bug fixes being committed every other day.

The development model with one pull request per release didn't work well for the project as users waited for weeks to get hands on a new release and, honestly, from development perspective producing large "heroic" releases takes a lot of energy 🫠.

From now on we'll be breaking releases into multiple pull requests with one feature/bugfix per PR.

Every PR merged into `main` branch will be publishing pre-release (developmental release) package to [pypi.org](https://pypi.org/project/flet/) having version format of `X.Y.Z.devN`.

<!-- truncate -->

## Installing pre-releases

To install Flet pre-release package use the following command:

```
pip install flet --pre
```

:::info
We recommend installing pre-release builds into a virtual environment.
:::

## Flet versioning

Flet is switching to [Semanting Versioning](https://semver.org/) with a version number `MAJOR.MINOR.PATCH`:

1. `MAJOR` will be incremented when there are "incompatible API changes". Right now it's `0` and we expect to make it `1` when we feel that Flet API is stable enough.
2. `MINOR` will be incremented when a new functionality added in a backwards compatible manner.
3. `PATCH` will be incremented when we make backward compatible bug fixes.

According to that rule, upcoming Flet release will have version `0.2.0`. Bug fixes for that release will be labeled as `0.2.1`, `0.2.2`, etc. The release after that release will be `0.3.0` and so on.

Flet pre-releases will have a format of `MAJOR.{LAST_MINOR + 1}.0.dev{BUILD}` where `LAST_MINOR` is `MINOR` version of the last release and `{BUILD}` is a build number set by [CI](https://ci.appveyor.com/project/flet-dev/flet). For example, if the last published release is `0.1.65` pre-releases will have versions `0.2.0.dev{BUILD}`. Pre-releases after `0.2.0` release will be labeled as `0.3.0.dev{BUILD}`.