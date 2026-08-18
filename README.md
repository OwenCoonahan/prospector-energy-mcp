# Prospector Energy MCP Server

MCP (Model Context Protocol) server that gives AI agents access to the Prospector Labs Energy Data API — US interconnection queue projects with milestone tracking, distributed generation installations, developer profiles and track records, ITC/PTC tax credit calculations, and ITC deal sourcing.

Counts change daily and are not published here. For current coverage call `get_queue_stats`, `get_dg_stats` and `get_developer_stats`, or see <https://api.prospectorlabs.io/catalog>.

## Quick start

Add this to your MCP client. The package ships with the production API as its default base URL, so no environment variables are required:

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

Try the API in one line first:

```bash
curl https://api.prospectorlabs.io/stats
```

Get a free API key in about 30 seconds, self-serve: **<https://api.prospectorlabs.io/start>**

## Tools Available (32 tools)

The **Tier** column is the plan a tool needs, as published at <https://api.prospectorlabs.io/plans>. It is a capability, not a price. Free covers every tool except bulk export, subject to a per-request row cap and a monthly query allowance.

### Projects & Search
| Tool | Description | Tier |
|------|-------------|------|
| `search_projects` | Search utility-scale energy projects by state, ISO, type, developer, capacity | Free |
| `get_project` | Full project detail with all enrichment fields | Free |
| `get_project_score` | Investability score breakdown for a project | Free |
| `get_queue_stats` | Aggregate interconnection queue statistics | Free |
| `get_milestone_summary` | Milestone and construction stage statistics | Free |
| `export_projects` | Bulk CSV export of projects | **Access** |

### Deals & Investment
| Tool | Description | Tier |
|------|-------------|------|
| `find_itc_deals` | ITC-eligible investment opportunities with scoring | Free |
| `get_itc_deal` | Detailed ITC deal profile | Free |
| `get_itc_summary` | Aggregate ITC deal pipeline statistics | Free |
| `get_investable_projects` | Pre-screened investable projects with grades | Free |
| `get_investable_summary` | Aggregate investability statistics | Free |
| `get_deal_sheet` | Formatted 1-page deal sheet (HTML, print to PDF) | Free |

### Tax Credits
| Tool | Description | Tier |
|------|-------------|------|
| `calculate_tax_credits` | ITC/PTC eligibility with all IRA bonus adders | Free |
| `check_domestic_content` | Domestic content ITC bonus eligibility (+10%) | Free |

### Developers
| Tool | Description | Tier |
|------|-------------|------|
| `search_developers` | Search developer profiles by name | Free |
| `get_developer` | Full developer profile with track record | Free |
| `get_developer_projects` | All projects by a specific developer | Free |
| `get_developer_stats` | Developer aggregate statistics | Free |

### Market Data
| Tool | Description | Tier |
|------|-------------|------|
| `get_lmp_monthly` | Monthly average LMP trends | Free |
| `get_lmp_zones` | List available LMP pricing zones | Free |
| `get_capacity_prices` | Capacity market auction prices | Free |
| `get_fuel_prices` | Fuel prices by state and type | Free |
| `get_technology_costs` | NREL ATB cost projections | Free |

### Grid Infrastructure
| Tool | Description | Tier |
|------|-------------|------|
| `get_grid_turbines` | US wind turbines (USWTDB) | Free |
| `get_grid_transmission` | Transmission lines (HIFLD) | Free |
| `get_grid_substations` | Electrical substations (HIFLD) | Free |
| `get_generators` | EIA generator inventory | Free |

### Distributed Generation
| Tool | Description | Tier |
|------|-------------|------|
| `search_dg_projects` | Search distributed generation installations | Free |
| `get_dg_stats` | DG aggregate statistics | Free |
| `get_investable_dg_projects` | Pre-screened investable DG projects | Free |
| `get_dg_investable_summary` | Aggregate investable DG statistics | Free |

### Utility
| Tool | Description | Tier |
|------|-------------|------|
| `get_pricing` | Plan tiers and, when self-hosting with MPP enabled, per-call amounts | Free |

## What's New in v0.4.1

- **Production API is the default base URL** — `https://api.prospectorlabs.io`. Earlier versions defaulted to the Railway hostname, so no `PROSPECTOR_API_URL` env var is needed any more.
- **Two tools delisted** — `get_lmp_daily` and `get_rto_generation` were returning empty result sets because the pipelines behind them are not populated. A tool that is listed and always empty is worse than one that is absent; they will return when the data does.
- **Tiers describe capability, not price** — the tool table now matches the plans published at `/plans`. See *Plans and payments* below.

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
| `PROSPECTOR_API_URL` | API base URL | `https://api.prospectorlabs.io` |
| `PROSPECTOR_API_KEY` | API key. **Required for `export_projects`**, which returns `401` without one. Optional for the other tools today | None |
| `MPP_RECIPIENT_ADDRESS` | Wallet address to receive payments (enables MPP — self-hosting only) | None (payments disabled) |
| `MPP_SECRET_KEY` | HMAC secret for payment challenge verification | Auto-generated |
| `MPP_REALM` | Server realm for payment challenges | `prospectorlabs.io` |

Get a key at <https://api.prospectorlabs.io/start>.

## Plans and payments

### Plans

Plans are published and enforced by the API, not by this package. Call <https://api.prospectorlabs.io/plans> for the current list — it is the only authoritative source.

| Tier | What it grants |
|------|----------------|
| **Free** | Full column width, a per-request row cap, a monthly query allowance. No bulk export |
| **Access** | The full daily queue — all projects, all columns, all markets, over both REST and MCP. Includes bulk CSV export |
| **Enterprise** | Bulk delivery, warehouse share, SLA, and redistribution of first-party sourced records |

Access and Enterprise are priced per engagement — <owen@prospectorlabs.io>.

### Agent payments (MPP)

This server can additionally charge per tool call in USDC over the [Machine Payments Protocol (MPP)](https://mpp.dev/), for operators who **run their own instance**.

MPP is opt-in and off by default: with `MPP_RECIPIENT_ADDRESS` unset, `paid_tool` returns the tool unwrapped and no payment challenge is ever issued. **The public `prospector-energy-mcp` package charges nothing per call** — access is governed by your API key's plan. Per-call amounts, when an operator enables MPP, are configured in `src/prospector_energy/payments.py`.

When enabled, the flow is:

1. Agent calls a paid tool (e.g., `search_projects`)
2. Server responds with a payment challenge (HTTP 402 equivalent)
3. Agent pays in USDC on the Tempo blockchain
4. Server verifies payment and returns data
5. Free tools (stats, summaries) always work without payment

### AgentCash

This server is also listed on [AgentCash](https://agentcash.dev/).

## Example Queries

Once connected, ask your AI agent:

- "How many solar projects are in the ERCOT queue?"
- "Calculate tax credits for a 2MW solar project in West Virginia"
- "Find investable ITC deals in New Jersey with credit rates above 50%"
- "Tell me about developer NextEra Energy's track record"
- "What were monthly average LMPs in PJM this year?"
- "Find battery storage projects over 100MW in California"

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
