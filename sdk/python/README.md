# Python SDK for Flet

Package relationships:

```mermaid
graph TD;
    flet-core-->flet-runtime;
    flet-core-->flet-pyodide;
    flet-runtime-->flet-embed;
    flet-runtime-->flet;
```