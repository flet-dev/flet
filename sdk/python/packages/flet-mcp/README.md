# flet-mcp

MCP (Model Context Protocol) server that gives LLM agents access to Flet examples, documentation, and API reference.

## Installation

```bash
pip install flet-mcp
```

## Building the data files

The MCP server reads a Griffe-introspected `api.json` and (optionally) a
SQLite index of examples and docs. Build them from inside the flet SDK
workspace so every Flet extension package (`flet-audio`, `flet-map`, …) is
importable — the workspace declares them all as members, but you need the
`mcp-build` dependency group to pick up the build-time deps (`markdownify`,
`griffe`):

```bash
cd sdk/python
uv sync --group mcp-build
uv run flet mcp build                            # api.json only
uv run flet mcp build --examples ./examples      # add examples index
```

The icon search metadata (`data/icons.json`) is a *committed* file, not a
build product — it is generated from Google's fonts.google.com icon
metadata (names, synonym tags, popularity; Apache-2.0, the same data that
powers the fonts.google.com icon search) and only changes when Google
ships new icons. Refresh it with:

```bash
uv run python -m flet_mcp.build.icons
```

> **Docs index is currently deferred.** The `--docs` flag still expects a mkdocs
> `search_index.json`, which the site no longer produces after the migration to
> Docusaurus + Algolia. The `DOCS` tool group stays off by default; rebuilding
> docs search against Docusaurus is tracked as follow-up work.

Running the build from elsewhere (a downstream project's venv that only
installs core `flet`) works too, but the resulting `api.json` will be missing
controls from every extension package not installed in that venv — the
indexer logs a "Failed to load" line per missing package and skips it.

## Usage

### Start the MCP server

```bash
# stdio transport (default, for use with Claude Desktop, Cursor, etc.)
flet mcp

# HTTP transport
flet mcp --transport streamable-http --port 8000
```

### Configure in Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "flet": {
      "command": "flet",
      "args": ["mcp"]
    }
  }
}
```

### List available tools

```bash
fastmcp list packages/flet-mcp/src/flet_mcp/server.py
```

### Call tools from the command line

```bash
# Search examples
fastmcp call packages/flet-mcp/src/flet_mcp/server.py search_examples '{"query": "dropdown"}'

# Get full example code
fastmcp call packages/flet-mcp/src/flet_mcp/server.py get_example '{"example_id": "controls_dropdown_styled"}'

# Get API reference for any symbol (control, service, type, event, enum)
fastmcp call packages/flet-mcp/src/flet_mcp/server.py get_api '{"name": "TextField"}'

# Find an icon
fastmcp call packages/flet-mcp/src/flet_mcp/server.py find_icon '{"query": "settings"}'

# Search large enums
fastmcp call packages/flet-mcp/src/flet_mcp/server.py search_enum_members '{"name": "Icons", "query": "arrow"}'

# Get CLI help
fastmcp call packages/flet-mcp/src/flet_mcp/server.py get_cli_help '{"command": "run"}'
```

### Use with Pydantic AI

```python
from pydantic_ai import Agent
from pydantic_ai.toolsets import MCPToolset
from flet_mcp import mcp

agent = Agent("anthropic:claude-sonnet-4-6", toolsets=[MCPToolset(mcp)])
result = agent.run_sync("Create a Flet app with a login form")
```

### Use in-process via a FastMCP client

The exported `mcp` is a `FastMCP` instance, so a custom agent can talk to it
in-process (no subprocess, no transport) by handing it to a `fastmcp.Client`.
Set the `FLET_MCP_ENABLE_*` env vars before importing `flet_mcp` so the desired
tool groups register. The client deserializes structured results onto `.data`:

```python
import asyncio
from fastmcp import Client
from flet_mcp import mcp

async def main():
    async with Client(mcp) as client:
        api = (await client.call_tool("get_api", {"name": "TextField"})).data
        print(api["kind"], api["package"], len(api["properties"]))

asyncio.run(main())
```

## Tools

Tools are organized into groups that can be toggled at server startup. Defaults
focus on the hallucination-reduction starter set: **API** and **icons** are on;
**examples**, **docs**, and **CLI** are off.

| Group | Default | Tools |
|---|---|---|
| `API` | on | `list_controls`, `get_api`, `get_enum`, `search_enum_members`, `enum_has_member` |
| `ICONS` | on | `find_icon` |
| `EXAMPLES` | off | `search_examples`, `get_example` |
| `DOCS` | off | `search_docs`, `get_doc` |
| `CLI` | off | `get_cli_help` |

| Tool | Description |
|------|-------------|
| `list_controls` | Browse controls and services, with optional filtering |
| `get_api` | Get the API reference for a class by name — looks across controls, services, dataclass types (ButtonStyle, Padding, ...), and event classes. Async methods are marked `"async": true`; every entry carries a `"package"` field naming the pip-installable source package (`"flet"` = core, anything else needs adding to deps). |
| `get_enum` | Get enum members |
| `search_enum_members` | Search large enums (Icons, CupertinoIcons) |
| `enum_has_member` | Check if an enum value exists |
| `find_icon` | Search Material and Cupertino icons by keyword |
| `search_examples` | Search example projects by keyword |
| `get_example` | Get full source code for an example |
| `search_docs` | Search documentation by keyword |
| `get_doc` | Get full content of a doc section |
| `get_cli_help` | Get structured CLI command options |

### Toggling groups

Each group is gated by an environment variable read at server startup:

| Variable | Default | Effect |
|---|---|---|
| `FLET_MCP_ENABLE_API` | `1` | Register the API tool group |
| `FLET_MCP_ENABLE_ICONS` | `1` | Register `find_icon` |
| `FLET_MCP_ENABLE_EXAMPLES` | `0` | Register example search/get tools |
| `FLET_MCP_ENABLE_DOCS` | `0` | Register docs search/get tools |
| `FLET_MCP_ENABLE_CLI` | `0` | Register `get_cli_help` |

Accepted truthy values: `1`, `true`, `yes` (case-insensitive). The active
groups are also surfaced in the server's `initialize` instructions, so MCP
clients that forward those instructions to the model (e.g. Pydantic AI's
`MCPToolset(..., include_instructions=True)`) keep the model's guidance
in sync with what's actually registered.

Examples:

```bash
# Default starter surface (API + icons only)
flet mcp

# Add examples and docs once their indexes have been built
FLET_MCP_ENABLE_EXAMPLES=1 FLET_MCP_ENABLE_DOCS=1 flet mcp

# Narrow further: API tools only, drop icons
FLET_MCP_ENABLE_ICONS=0 flet mcp
```

Note: enabling `EXAMPLES` only registers the tools — you also need to populate
the SQLite index by running `flet mcp build --examples <path>`. Without an index
the tools register cleanly but return empty results. `DOCS` is deferred (see
"Building the data files" above): the tools register and degrade gracefully to
empty results, but no docs index is built yet.
