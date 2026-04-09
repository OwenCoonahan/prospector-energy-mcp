# Prospector Energy MCP Server

MCP (Model Context Protocol) server that gives AI agents access to the Prospector Labs Energy Data API — 47,000+ interconnection queue projects, 5.4M distributed generation installations, 6,593 developer profiles, tax credit calculations, and ITC deal sourcing.

**Now with agent payments via MPP** — AI agents can pay per-tool-call in USDC stablecoins.

## Tools Available (35 tools)

### Projects & Search
| Tool | Description | Tier |
|------|-------------|------|
| `search_projects` | Search 47K+ utility-scale energy projects by state, ISO, type, developer, capacity | Standard ($0.01) |
| `get_project` | Full project detail with all enrichment fields | Premium ($0.05) |
| `get_project_score` | Investability score breakdown for a project | Premium ($0.05) |
| `get_queue_stats` | Aggregate interconnection queue statistics | Free |
| `get_milestone_summary` | Milestone and construction stage statistics | Free |
| `export_projects` | Export projects as CSV (up to 50K) | Pro ($0.10) |

### Deals & Investment
| Tool | Description | Tier |
|------|-------------|------|
| `find_itc_deals` | ITC-eligible investment opportunities with scoring | Premium ($0.05) |
| `get_itc_deal` | Detailed ITC deal profile | Premium ($0.05) |
| `get_itc_summary` | Aggregate ITC deal pipeline statistics | Free |
| `get_investable_projects` | Pre-screened investable projects with grades | Premium ($0.05) |
| `get_investable_summary` | Aggregate investability statistics | Free |
| `get_deal_sheet` | Formatted 1-page deal sheet (HTML, print to PDF) | Pro ($0.10) |

### Tax Credits
| Tool | Description | Tier |
|------|-------------|------|
| `calculate_tax_credits` | ITC/PTC eligibility with all IRA bonus adders | Premium ($0.05) |
| `check_domestic_content` | Domestic content ITC bonus eligibility (+10%) | Premium ($0.05) |

### Developers
| Tool | Description | Tier |
|------|-------------|------|
| `search_developers` | Search 6,593 developer profiles by name | Standard ($0.01) |
| `get_developer` | Full developer profile with track record | Premium ($0.05) |
| `get_developer_projects` | All projects by a specific developer | Standard ($0.01) |
| `get_developer_stats` | Developer aggregate statistics | Free |

### Market Data
| Tool | Description | Tier |
|------|-------------|------|
| `get_lmp_daily` | Daily locational marginal prices | Standard ($0.01) |
| `get_lmp_monthly` | Monthly average LMP trends | Standard ($0.01) |
| `get_lmp_zones` | List available LMP pricing zones | Free |
| `get_capacity_prices` | Capacity market auction prices | Standard ($0.01) |
| `get_fuel_prices` | Fuel prices by state and type | Standard ($0.01) |
| `get_technology_costs` | NREL ATB cost projections | Standard ($0.01) |
| `get_rto_generation` | RTO-level generation by fuel type | Standard ($0.01) |

### Grid Infrastructure
| Tool | Description | Tier |
|------|-------------|------|
| `get_grid_turbines` | 75K+ US wind turbines (USWTDB) | Standard ($0.01) |
| `get_grid_transmission` | 95K+ transmission lines (HIFLD) | Standard ($0.01) |
| `get_grid_substations` | 64K+ electrical substations (HIFLD) | Standard ($0.01) |
| `get_generators` | EIA generator inventory (26K+ generators) | Standard ($0.01) |

### Distributed Generation
| Tool | Description | Tier |
|------|-------------|------|
| `search_dg_projects` | Search 5.4M distributed generation installations | Standard ($0.01) |
| `get_dg_stats` | DG aggregate statistics | Free |
| `get_investable_dg_projects` | Pre-screened investable DG projects (55K+ scored) | Premium ($0.05) |
| `get_dg_investable_summary` | Aggregate investable DG statistics | Free |

### Utility
| Tool | Description | Tier |
|------|-------------|------|
| `get_pricing` | View pricing for all tools | Free |

## What's New in v0.4.0

- **Agent payments via MPP** — per-tool-call pricing in USDC stablecoins via Machine Payments Protocol
- **Tiered pricing** — Free stats/summaries, $0.01 searches, $0.05 premium lookups, $0.10 deal sheets
- **`get_pricing` tool** — Agents can discover tool costs before calling
- **Backwards compatible** — Without `MPP_RECIPIENT_ADDRESS`, everything works as before

## Setup

### Claude Desktop

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

### Claude Code

Add to your `.mcp.json`:

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

Add to Cursor Settings > MCP Servers:

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
# From PyPI
pip install prospector-energy-mcp

# With payment support
pip install prospector-energy-mcp[payments]

# Or with uv
uvx prospector-energy-mcp
```

## Configuration

| Environment Variable | Description | Default |
|---------------------|-------------|---------|
| `PROSPECTOR_API_URL` | API base URL | `https://prospector-platform-production.up.railway.app` |
| `PROSPECTOR_API_KEY` | API key for authenticated access | None (free tier) |
| `MPP_RECIPIENT_ADDRESS` | Wallet address to receive payments (enables MPP) | None (payments disabled) |
| `MPP_SECRET_KEY` | HMAC secret for payment challenge verification | Auto-generated |
| `MPP_REALM` | Server realm for payment challenges | `prospectorlabs.io` |

## Agent Payments (MPP)

This server supports the [Machine Payments Protocol (MPP)](https://mpp.dev/) for per-tool-call payments in USDC stablecoins. When enabled, AI agents with funded wallets can autonomously pay for data queries.

### How It Works

1. Agent calls a paid tool (e.g., `search_projects`)
2. Server responds with a payment challenge (HTTP 402 equivalent)
3. Agent pays in USDC on Tempo blockchain
4. Server verifies payment and returns data
5. Free tools (stats, summaries) always work without payment

### Pricing

| Tier | Cost/Call | Tools |
|------|----------|-------|
| **Free** | $0.00 | Stats, summaries, zone lists, pricing info |
| **Standard** | $0.01 | Searches, generators, market data, grid data |
| **Premium** | $0.05 | Project details, tax credits, developer profiles, investable projects |
| **Pro** | $0.10 | Deal sheets, bulk CSV exports |

### AgentCash

This server is also available on [AgentCash](https://agentcash.dev/) — agents with funded USDC wallets can discover and pay for energy data automatically.

## Example Queries

Once connected, ask your AI agent:

- "How many solar projects are in the ERCOT queue?"
- "Calculate tax credits for a 2MW solar project in West Virginia"
- "Find investable ITC deals in New Jersey with credit rates above 50%"
- "Tell me about developer NextEra Energy's track record"
- "What's the average LMP in PJM this week?"
- "Find battery storage projects over 100MW in California"
- "What does each tool cost?" (calls `get_pricing`)

## Development

```bash
# Clone and install in dev mode
cd mcp-server
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ".[payments]"

# Run with stdio transport (default)
python -m prospector_energy

# Run with SSE transport
python -m prospector_energy --sse

# Test with MCP inspector
npx @modelcontextprotocol/inspector python -m prospector_energy
```
