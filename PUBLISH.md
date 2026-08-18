# Publishing the MCP Server

## Option 1: GitHub (fastest — do this first)

### Step 1: Create the repo

Go to https://github.com/new and create:
- **Name:** `prospector-energy-mcp`
- **Description:** MCP server for US energy infrastructure data — interconnection queue projects, distributed generation, tax credits, developer intelligence
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

# Build the CURRENT version
python3.12 -m build

# Upload ONLY this release's artifacts.
# dist/ retains artifacts from every previous build, and PyPI rejects the whole
# upload if any file in the glob is a version that already exists. Never `dist/*`.
python3.12 -m twine upload dist/*0.4.1*
# Enter: __token__ as username, paste your API token as password
```

A version on PyPI is immutable — it cannot be re-uploaded or edited, only yanked.
Confirm the README and tool list are correct BEFORE this step, not after.

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
| **Description** | Access US energy infrastructure data — interconnection queue projects across the 7 ISOs/RTOs (PJM, MISO, SPP, CAISO, ERCOT, NYISO, ISO-NE), distributed generation installations, ITC/PTC tax credit calculations with all IRA bonuses, developer profiles with track records, and ITC deal sourcing for investors. |
| **Install** | `pip install prospector-energy-mcp` (or `pip install git+https://github.com/OwenCoonahan/prospector-energy-mcp.git`) |
| **GitHub** | https://github.com/OwenCoonahan/prospector-energy-mcp |
| **Category** | Data / Finance / Energy |
| **Author** | Prospector Labs |
| **Tools** | 32 tools: search_projects, get_project, get_project_score, get_queue_stats, get_milestone_summary, export_projects, find_itc_deals, get_itc_deal, get_itc_summary, get_investable_projects, get_investable_summary, get_deal_sheet, calculate_tax_credits, check_domestic_content, search_developers, get_developer, get_developer_projects, get_developer_stats, get_lmp_monthly, get_lmp_zones, get_capacity_prices, get_fuel_prices, get_technology_costs, get_grid_turbines, get_grid_transmission, get_grid_substations, get_generators, search_dg_projects, get_dg_stats, get_investable_dg_projects, get_dg_investable_summary, get_pricing |

**Do not paste a record count into a registry listing.** Counts change daily and a
registry entry is not something anyone comes back to update. The project and DG
totals previously published here drifted far from the served values before anyone
noticed — one of them was nearly double the real number.

### Smithery.ai

Go to https://smithery.ai and submit the same info as above.

### Anthropic MCP Directory

As of March 2026, Anthropic does not have a formal public submission process for MCP servers. The README already includes Claude Desktop configuration instructions. If a directory opens, submit with the same info.

### glama.ai

Go to https://glama.ai/mcp/servers and check their submission process. Same info as above.
