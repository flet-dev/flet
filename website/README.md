# Website

This website is built using [Docusaurus 2](https://v2.docusaurus.io/), a modern static website generator.

View the live site at [https://flet.dev](https://flet.dev).

### Installation

```
$ yarn
```

### Local Development

```
$ yarn start
```

This command runs CrocoDocs generation and starts a local development server.
If CrocoDocs generation fails (for example while offline), `yarn start` reuses existing generated files from previous successful runs.

If this is the very first run, keep an internet connection and run:

```
$ yarn crocodocs:generate
```

Most changes are reflected live without having to restart the server.

### Build

```
$ yarn build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.
