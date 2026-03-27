# Publishing the MCP Server

## Option 1: GitHub (fastest — do this first)

### Step 1: Create the repo

Go to https://github.com/new and create:
- **Name:** `prospector-energy-mcp`
- **Description:** MCP server for US energy infrastructure data — 47K interconnection projects, 5.4M DG installations, tax credits, developer intelligence
- **Visibility:** Public
- **Don't** initialize with README (we already have one)

### Step 2: Push

```bash
cd "/Users/owencoonahan/Documents/Grand Library/End Suffering/prospector-platform/mcp-server"

# Initialize as standalone repo
git init
git add .
git commit -m "Initial release: prospector-energy MCP server v0.1.0"
git branch -M main
git remote add origin https://github.com/OwenCoonahan/prospector-energy-mcp.git
git push -u origin main
```

### Step 3: Users can now install via

```bash
pip install git+https://github.com/OwenCoonahan/prospector-energy-mcp.git
```

Or in Claude Desktop config:
```json
{
  "mcpServers": {
    "prospector-energy": {
      "command": "pip",
      "args": ["install", "git+https://github.com/OwenCoonahan/prospector-energy-mcp.git"],
      "installCommand": "pip install git+https://github.com/OwenCoonahan/prospector-energy-mcp.git"
    }
  }
}
```

---

## Option 2: PyPI

### Step 1: Create PyPI account

Go to https://pypi.org/account/register/ and create an account.

### Step 2: Create an API token

Go to https://pypi.org/manage/account/token/ → Create token → Scope: entire account.

### Step 3: Build and upload

```bash
cd "/Users/owencoonahan/Documents/Grand Library/End Suffering/prospector-platform/mcp-server"

# Build (already done, packages in dist/)
python3.12 -m build

# Upload
python3.12 -m twine upload dist/*
# Enter: __token__ as username, paste your API token as password
```

### Step 4: Users can now install via

```bash
pip install prospector-energy-mcp
# or
uvx prospector-energy-mcp
```

---

## MCP Registry Submissions

### mcp.so

Go to https://mcp.so and submit:

| Field | Value |
|-------|-------|
| **Name** | prospector-energy |
| **Description** | Access US energy infrastructure data — 47,000 interconnection queue projects across 9 ISOs, 5.4M distributed generation installations, ITC/PTC tax credit calculations with all IRA bonuses, 6,593 developer profiles with track records, and ITC deal sourcing for investors. |
| **Install** | `pip install prospector-energy-mcp` (or `pip install git+https://github.com/OwenCoonahan/prospector-energy-mcp.git`) |
| **GitHub** | https://github.com/OwenCoonahan/prospector-energy-mcp |
| **Category** | Data / Finance / Energy |
| **Author** | Prospector Labs |
| **Tools** | 20 tools: search_projects, get_project, calculate_tax_credits, find_itc_deals, get_itc_deal, search_developers, get_developer, get_developer_projects, get_investable_projects, get_investable_summary, get_market_stats, search_dg_projects, get_lmp_daily, get_capacity_prices, get_generators, get_technology_costs, check_domestic_content, get_grid_turbines, get_developer_stats, get_dg_stats |

### Smithery.ai

Go to https://smithery.ai and submit the same info as above.

### Anthropic MCP Directory

As of March 2026, Anthropic does not have a formal public submission process for MCP servers. The README already includes Claude Desktop configuration instructions. If a directory opens, submit with the same info.

### glama.ai

Go to https://glama.ai/mcp/servers and check their submission process. Same info as above.
