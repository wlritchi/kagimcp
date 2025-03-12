# Kagi MCP server

[![smithery badge](https://smithery.ai/badge/kagimcp)](https://smithery.ai/server/kagimcp)

<a href="https://glama.ai/mcp/servers/xabrrs4bka">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/xabrrs4bka/badge" alt="Kagi Server MCP server" />
</a>

## Features

This MCP server provides two main tools for integrating Kagi's services with LLMs:

1. **Search** - Perform web searches using Kagi's search API (requires search API access)
2. **Summarize** - Use Kagi's FastGPT to summarize web search results for a query (available to all Kagi users)

Each tool can be enabled/disabled independently using environment variables, allowing you to use only the features you need or have access to.

## Setup Intructions
> For the search functionality, ensure you have access to the search API. It is currently in closed beta and available upon request. Please reach out to support@kagi.com for an invite.
>
> The FastGPT summarize functionality is available to all Kagi users with an API key.

Install uv first.

MacOS/Linux:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows:
```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Setup with Claude Desktop
```json
# claude_desktop_config.json
# Can find location through:
# Hamburger Menu -> File -> Settings -> Developer -> Edit Config
{
  "mcpServers": {
    "kagi": {
      "command": "uvx",
      "args": ["kagimcp"],
      "env": {
        "KAGI_API_KEY": "YOUR_API_KEY_HERE",
        "KAGI_ENABLE_SEARCH": "true",
        "KAGI_ENABLE_FASTGPT": "true"
      }
    }
  }
}
```

### Installing via Smithery

Alternatively, you can install Kagi for Claude Desktop automatically via [Smithery](https://smithery.ai/server/kagimcp):

```bash
npx -y @smithery/cli install kagimcp --client claude
```

### Ask Claude a question requiring search
e.g. "Who was time's 2024 person of the year?"

### Debugging
Run:
```bash
npx @modelcontextprotocol/inspector uvx kagimcp
```

## Local/Dev Setup Instructions

### Clone repo
`git clone https://github.com/kagisearch/kagimcp.git`

### Install dependencies
Install uv first.

MacOS/Linux:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows:
```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then install MCP server dependencies:
```bash
cd kagimcp

# Create virtual environment and activate it
uv venv

source .venv/bin/activate # MacOS/Linux
# OR
.venv/Scripts/activate # Windows

# Install dependencies
uv sync
```
### Setup with Claude Desktop

#### Using MCP CLI SDK
```bash
# `pip install mcp[cli]` if you haven't
mcp install /ABSOLUTE/PATH/TO/PARENT/FOLDER/kagimcp/src/kagimcp/server.py -v "KAGI_API_KEY=API_KEY_HERE"
```

#### Manually
```json
# claude_desktop_config.json
# Can find location through:
# Hamburger Menu -> File -> Settings -> Developer -> Edit Config
{
  "mcpServers": {
    "kagi": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/PARENT/FOLDER/kagimcp",
        "run",
        "kagimcp"
      ],
      "env": {
        "KAGI_API_KEY": "YOUR_API_KEY_HERE",
        "KAGI_ENABLE_SEARCH": "true",
        "KAGI_ENABLE_FASTGPT": "true"
      }
    }
  }
}
```
### Ask Claude a question requiring search
e.g. "Who was time's 2024 person of the year?"
### Debugging
Run:
```bash
# If mcp cli installed (`pip install mcp[cli]`)
mcp dev /ABSOLUTE/PATH/TO/PARENT/FOLDER/kagimcp/src/kagimcp/server.py

# If not
npx @modelcontextprotocol/inspector \
      uv \
      --directory /ABSOLUTE/PATH/TO/PARENT/FOLDER/kagimcp \
      run \
      kagimcp
```
Then access MCP Inspector at `http://localhost:5173`. You may need to add your Kagi API key in the environment variables in the inspector under `KAGI_API_KEY`.

# Environment Variables

- `KAGI_API_KEY` - Your Kagi API key (required)
- `KAGI_ENABLE_SEARCH` - Enable/disable the search functionality (default: "true")
- `KAGI_ENABLE_FASTGPT` - Enable/disable the FastGPT functionality (default: "true")
- `FASTMCP_LOG_LEVEL` - Adjust logging level (e.g. "ERROR", "INFO", "DEBUG")
  - Relevant issue: https://github.com/kagisearch/kagimcp/issues/4