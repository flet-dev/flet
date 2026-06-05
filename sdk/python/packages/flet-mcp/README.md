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
uv run flet mcp build --docs <search_index.json> # add docs index
```

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

# Search documentation
fastmcp call packages/flet-mcp/src/flet_mcp/server.py search_docs '{"query": "TextField validation"}'

# Get control API reference
fastmcp call packages/flet-mcp/src/flet_mcp/server.py get_control_api '{"name": "TextField"}'

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

agent = Agent("claude-sonnet-4-20250514", toolsets=[MCPToolset(mcp)])
result = agent.run_sync("Create a Flet app with a login form")
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
| `get_api` | Get the API reference for a class by name — looks across controls, services, dataclass types (ButtonStyle, Padding, ...), and event classes. Async methods are marked `"async": true`. |
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

Note: enabling `EXAMPLES` or `DOCS` only registers the tools — you also need to
populate the SQLite index by running `flet mcp build --examples <path>` and/or
`--docs <search_index.json>`. Without an index the tools register cleanly but
return empty results.
