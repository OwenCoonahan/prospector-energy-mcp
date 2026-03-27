# Prospector Energy MCP Server

MCP (Model Context Protocol) server that gives AI agents access to the Prospector Labs Energy Data API — 47,000+ interconnection queue projects, 5.4M distributed generation installations, 6,593 developer profiles, tax credit calculations, and ITC deal sourcing.

## Tools Available (31 tools)

### Projects & Search
| Tool | Description |
|------|-------------|
| `search_projects` | Search 47K+ utility-scale energy projects by state, ISO, type, developer, capacity |
| `get_project` | Full project detail with all enrichment fields |
| `get_project_score` | Investability score breakdown for a project |
| `get_queue_stats` | Aggregate interconnection queue statistics |
| `export_projects` | Export projects as CSV (up to 50K) |

### Deals & Investment
| Tool | Description |
|------|-------------|
| `find_itc_deals` | ITC-eligible investment opportunities with scoring |
| `get_itc_deal` | Detailed ITC deal profile |
| `get_itc_summary` | Aggregate ITC deal pipeline statistics |
| `get_investable_projects` | Pre-screened investable projects with grades |
| `get_investable_summary` | Aggregate investability statistics |
| `get_deal_sheet` | Formatted 1-page deal sheet (HTML, print to PDF) |

### Tax Credits
| Tool | Description |
|------|-------------|
| `calculate_tax_credits` | ITC/PTC eligibility with all IRA bonus adders |
| `check_domestic_content` | Domestic content ITC bonus eligibility (+10%) |

### Developers
| Tool | Description |
|------|-------------|
| `search_developers` | Search 6,593 developer profiles by name |
| `get_developer` | Full developer profile with track record |
| `get_developer_projects` | All projects by a specific developer |
| `get_developer_stats` | Developer aggregate statistics |

### Market Data
| Tool | Description |
|------|-------------|
| `get_lmp_daily` | Daily locational marginal prices |
| `get_lmp_monthly` | Monthly average LMP trends |
| `get_lmp_zones` | List available LMP pricing zones |
| `get_capacity_prices` | Capacity market auction prices |
| `get_fuel_prices` | Fuel prices by state and type |
| `get_technology_costs` | NREL ATB cost projections |
| `get_rto_generation` | RTO-level generation by fuel type |

### Grid Infrastructure
| Tool | Description |
|------|-------------|
| `get_grid_turbines` | 75K+ US wind turbines (USWTDB) |
| `get_grid_transmission` | 95K+ transmission lines (HIFLD) |
| `get_grid_substations` | 64K+ electrical substations (HIFLD) |
| `get_generators` | EIA generator inventory (26K+ generators) |

### Distributed Generation
| Tool | Description |
|------|-------------|
| `search_dg_projects` | Search 5.4M distributed generation installations |
| `get_dg_stats` | DG aggregate statistics |

## Setup

### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "prospector-energy": {
      "command": "uvx",
      "args": ["prospector-energy-mcp"]
    }
  }
}
```

Or if installed locally:

```json
{
  "mcpServers": {
    "prospector-energy": {
      "command": "/path/to/venv/bin/python",
      "args": ["-m", "prospector_energy"]
    }
  }
}
```

### Claude Code

Add to your Claude Code settings or `.mcp.json`:

```json
{
  "mcpServers": {
    "prospector-energy": {
      "command": "uvx",
      "args": ["prospector-energy-mcp"]
    }
  }
}
```

### Cursor

Add to Cursor's MCP settings (Settings > MCP Servers):

```json
{
  "prospector-energy": {
    "command": "uvx",
    "args": ["prospector-energy-mcp"]
  }
}
```

### Direct Install

```bash
# From GitHub
pip install git+https://github.com/OwenCoonahan/prospector-energy-mcp.git

# From PyPI
pip install prospector-energy-mcp

# Or with uv
uvx prospector-energy-mcp

# Run directly
prospector-energy-mcp
```

## Configuration

| Environment Variable | Description | Default |
|---------------------|-------------|---------|
| `PROSPECTOR_API_URL` | API base URL | `https://prospector-platform-production.up.railway.app` |
| `PROSPECTOR_API_KEY` | API key for authenticated access | None (free tier) |

## Example Queries

Once connected, ask your AI agent:

- "How many solar projects are in the ERCOT queue?"
- "Calculate tax credits for a 2MW solar project in West Virginia"
- "Find investable ITC deals in New Jersey with credit rates above 50%"
- "Tell me about developer NextEra Energy's track record"
- "What's the average LMP in PJM this week?"
- "Find battery storage projects over 100MW in California"

## Development

```bash
# Clone and install in dev mode
cd mcp-server
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e .

# Run with stdio transport (default)
python -m prospector_energy

# Run with SSE transport
python -m prospector_energy --sse

# Test with MCP inspector
npx @modelcontextprotocol/inspector python -m prospector_energy
```
