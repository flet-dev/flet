# flet-mcp

MCP (Model Context Protocol) server that gives LLM agents access to Flet examples, documentation, and API reference.

## Installation

```bash
pip install flet-mcp
```

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

| Tool | Description |
|------|-------------|
| `search_examples` | Search example projects by keyword |
| `get_example` | Get full source code for an example |
| `search_docs` | Search documentation by keyword |
| `get_doc` | Get full content of a doc section |
| `list_controls` | List controls and services, with optional filtering |
| `get_control_api` | Get properties, events, and methods for a control |
| `get_type_api` | Get fields and methods for a type (ButtonStyle, Padding, etc.) |
| `get_enum` | Get enum members |
| `search_enum_members` | Search large enums (Icons, CupertinoIcons) |
| `enum_has_member` | Check if an enum value exists |
| `find_icon` | Search Material and Cupertino icons by keyword |
| `get_cli_help` | Get structured CLI command options |
