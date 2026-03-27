"""Prospector Energy MCP Server.

Exposes the Prospector Labs Energy Data API (61 endpoints) as MCP tools
that Claude, GPT, and other AI agents can discover and call natively.

Usage:
    python -m prospector_energy          # stdio transport (default)
    python -m prospector_energy --sse    # SSE transport for web clients

Environment:
    PROSPECTOR_API_URL  — API base URL (default: Railway production)
    PROSPECTOR_API_KEY  — Optional API key for authenticated access
"""

import json
import sys
from typing import Any

from mcp.server.fastmcp import FastMCP

from .client import ProspectorClient

mcp = FastMCP(
    "prospector-energy",
    instructions=(
        "Energy infrastructure data for the US power grid. "
        "47,000+ interconnection queue projects, 4.8M distributed generation installations, "
        "6,593 developer profiles, tax credit calculations, ITC deal sourcing, "
        "market data, and grid infrastructure. Use these tools to answer questions "
        "about US energy projects, renewable energy development, tax credits, "
        "and energy market data."
    ),
)

_client: ProspectorClient | None = None


def _get_client() -> ProspectorClient:
    global _client
    if _client is None:
        _client = ProspectorClient()
    return _client


def _fmt(data: Any) -> str:
    """Format API response as readable text."""
    if isinstance(data, dict):
        return json.dumps(data, indent=2, default=str)
    return str(data)


# =============================================================================
# Primary Tools
# =============================================================================


@mcp.tool()
async def search_projects(
    state: str | None = None,
    region: str | None = None,
    type: str | None = None,
    status: str | None = None,
    developer: str | None = None,
    min_mw: float | None = None,
    max_mw: float | None = None,
    page: int = 1,
    per_page: int = 20,
) -> str:
    """Search the US interconnection queue database (47,000+ utility-scale energy projects).

    Covers all major ISOs: PJM, MISO, ERCOT, CAISO, NYISO, SPP, ISO-NE, plus
    West and Southeast non-ISO regions.

    Projects include solar, wind, battery storage, natural gas, nuclear, and hybrid.
    Each project has enrichment data: tax credit eligibility, developer track record,
    energy community status, investability score, and interconnection status.

    Use this to answer questions like:
    - "How many solar projects are in the ERCOT queue?"
    - "What projects is NextEra developing in PJM?"
    - "Find battery storage projects over 100 MW in California"

    Args:
        state: US state abbreviation (e.g. "TX", "CA", "NJ")
        region: ISO/RTO region (PJM, MISO, ERCOT, CAISO, NYISO, SPP, ISO-NE, West, Southeast)
        type: Technology type (Solar, Wind, Battery Storage, Natural Gas, Nuclear, Hybrid, etc.)
        status: Project status (Active, Withdrawn, Operational, Suspended)
        developer: Developer name (partial match)
        min_mw: Minimum capacity in MW
        max_mw: Maximum capacity in MW
        page: Page number (default 1)
        per_page: Results per page (default 20, max 200)
    """
    client = _get_client()
    data = await client.get("/projects", {
        "state": state, "region": region, "type": type, "status": status,
        "developer": developer, "min_mw": min_mw, "max_mw": max_mw,
        "page": page, "per_page": per_page,
    })
    return _fmt(data)


@mcp.tool()
async def get_project(queue_id: str) -> str:
    """Get full details for a specific interconnection queue project.

    Returns all enrichment fields: tax credits, energy community eligibility,
    low-income eligibility, developer info, investability score, construction stage,
    interconnection costs, FERC financials, and more.

    Args:
        queue_id: The project's queue ID (e.g. "AB2-037", "J0123", "GI-2024-001")
    """
    client = _get_client()
    data = await client.get(f"/projects/{queue_id}")
    return _fmt(data)


@mcp.tool()
async def calculate_tax_credits(
    technology: str,
    capacity_mw: float,
    state: str,
    county: str | None = None,
    cod_year: int | None = None,
) -> str:
    """Calculate ITC/PTC tax credit eligibility for an energy project.

    Applies all IRA (Inflation Reduction Act) bonus adders:
    - Base credit (ITC 30% or PTC $28.35/MWh)
    - Energy community bonus (+10%)
    - Low-income community bonus (+10-20%)
    - Domestic content bonus (+10%)

    Use this to answer questions like:
    - "What tax credits does a 2MW solar project in West Virginia qualify for?"
    - "Calculate the ITC for a 50MW wind farm in a coal closure community"

    Args:
        technology: Project type (Solar, Wind, Battery Storage, etc.)
        capacity_mw: Project capacity in megawatts
        state: US state abbreviation
        county: County name (needed for energy community and low-income checks)
        cod_year: Expected commercial operation date year (affects credit phase-down)
    """
    client = _get_client()
    data = await client.get("/tax-credits/calculate", {
        "technology": technology, "capacity_mw": capacity_mw,
        "state": state, "county": county, "cod_year": cod_year,
    })
    return _fmt(data)


@mcp.tool()
async def find_itc_deals(
    state: str | None = None,
    region: str | None = None,
    type: str | None = None,
    min_credit_rate: float | None = None,
    max_capacity_mw: float | None = None,
    page: int = 1,
    per_page: int = 20,
) -> str:
    """Find ITC-eligible investment opportunities with scoring.

    Searches for projects that qualify for Investment Tax Credits, scored by
    credit value, developer track record, and project viability. Designed
    for investors seeking ITC deal flow.

    Use this to answer questions like:
    - "Find high-value ITC deals in New Jersey"
    - "What solar projects have 50%+ effective credit rates?"
    - "Show me small-scale deals under 20MW in energy communities"

    Args:
        state: US state abbreviation
        region: ISO/RTO region
        type: Technology type
        min_credit_rate: Minimum effective credit rate (0.0-1.0, e.g. 0.5 for 50%)
        max_capacity_mw: Maximum capacity (smaller projects often have higher credit rates)
        page: Page number
        per_page: Results per page
    """
    client = _get_client()
    data = await client.get("/deals/itc", {
        "state": state, "region": region, "type": type,
        "min_credit_rate": min_credit_rate, "max_capacity_mw": max_capacity_mw,
        "page": page, "per_page": per_page,
    })
    return _fmt(data)


@mcp.tool()
async def get_itc_deal(queue_id: str) -> str:
    """Get detailed ITC deal profile for a specific project.

    Returns full tax credit breakdown, developer info, investability scoring,
    and deal-relevant enrichment data.

    Args:
        queue_id: The project's queue ID
    """
    client = _get_client()
    data = await client.get(f"/deals/itc/{queue_id}")
    return _fmt(data)


@mcp.tool()
async def search_developers(q: str) -> str:
    """Search energy project developers by name.

    Searches across 6,593 developer profiles and 6,332 name aliases.
    Returns developer summary with tier classification, track record,
    and portfolio metrics.

    Developer tiers: major_utility, major_ipp, mid_platform, pe_fund, independent

    Args:
        q: Search query (developer name, partial match supported)
    """
    client = _get_client()
    data = await client.get("/developers/search", {"q": q})
    return _fmt(data)


@mcp.tool()
async def get_developer(developer_id: int) -> str:
    """Get full developer profile with track record.

    Returns: tier classification, project counts, capacity totals,
    completion rate, regional breakdown, technology mix, aliases,
    corporate relationships, and capital needs assessment.

    Args:
        developer_id: Developer ID (get from search_developers)
    """
    client = _get_client()
    data = await client.get(f"/developers/{developer_id}")
    return _fmt(data)


@mcp.tool()
async def get_developer_projects(
    developer_id: int,
    page: int = 1,
    per_page: int = 20,
    sort: str = "capacity_mw",
    order: str = "desc",
) -> str:
    """Get all projects by a specific developer.

    Lists all interconnection queue projects associated with the developer,
    including all name aliases.

    Args:
        developer_id: Developer ID (get from search_developers)
        page: Page number
        per_page: Results per page
        sort: Sort by field (capacity_mw, queue_date_std, status_std)
        order: Sort order (asc, desc)
    """
    client = _get_client()
    data = await client.get(f"/developers/{developer_id}/projects", {
        "page": page, "per_page": per_page, "sort": sort, "order": order,
    })
    return _fmt(data)


@mcp.tool()
async def get_investable_projects(
    min_score: int | None = None,
    state: str | None = None,
    region: str | None = None,
    type: str | None = None,
    page: int = 1,
    per_page: int = 20,
) -> str:
    """Find pre-screened investable energy projects.

    Projects are scored on: ITC eligibility, developer independence (needs capital),
    construction stage progression, energy community bonus, and project viability.

    Investability grades: A (70+), B (50-69), C (30-49), D (<30)

    Use this to answer questions like:
    - "Show me the highest-scored investable projects"
    - "Find investable solar deals in Texas"
    - "What Grade A projects are available in PJM?"

    Args:
        min_score: Minimum investability score (0-100)
        state: US state abbreviation
        region: ISO/RTO region
        type: Technology type
        page: Page number
        per_page: Results per page
    """
    client = _get_client()
    data = await client.get("/investable", {
        "min_score": min_score, "state": state, "region": region,
        "type": type, "page": page, "per_page": per_page,
    })
    return _fmt(data)


@mcp.tool()
async def get_investable_summary() -> str:
    """Get aggregate investability statistics.

    Returns: total investable projects, breakdown by grade/tier/region/type,
    total investable capacity, and deal pipeline summary.
    """
    client = _get_client()
    data = await client.get("/investable/summary")
    return _fmt(data)


@mcp.tool()
async def get_market_stats() -> str:
    """Get aggregate statistics for the interconnection queue database.

    Returns: total projects, capacity by region/type/status, technology mix,
    historical trends, and data freshness.
    """
    client = _get_client()
    data = await client.get("/stats")
    return _fmt(data)


@mcp.tool()
async def search_dg_projects(
    state: str | None = None,
    type: str | None = None,
    status: str | None = None,
    min_kw: float | None = None,
    max_kw: float | None = None,
    page: int = 1,
    per_page: int = 20,
) -> str:
    """Search distributed generation installations (4.8M+ projects).

    Covers rooftop solar, community solar, and other sub-1MW installations
    from 16 state programs across 27+ states.

    Sources include: LBNL Tracking the Sun, NY-SUN, NJ Clean Energy,
    CA DG Stats, IL Shines, MA SMART, NY DPS SIR, and more.

    Args:
        state: US state abbreviation
        type: Technology type (Solar, Battery Storage, etc.)
        status: Status filter (Active, Operational, Withdrawn)
        min_kw: Minimum capacity in kW
        max_kw: Maximum capacity in kW
        page: Page number
        per_page: Results per page
    """
    client = _get_client()
    data = await client.get("/dg/projects", {
        "state": state, "type": type, "status": status,
        "min_kw": min_kw, "max_kw": max_kw,
        "page": page, "per_page": per_page,
    })
    return _fmt(data)


# =============================================================================
# Secondary Tools
# =============================================================================


@mcp.tool()
async def get_lmp_daily(
    iso: str | None = None,
    zone: str | None = None,
    days: int = 7,
) -> str:
    """Get daily locational marginal prices (LMP) for energy markets.

    LMP data from CAISO, ERCOT, ISO-NE, MISO, NYISO, and PJM.

    Args:
        iso: ISO/RTO name (CAISO, ERCOT, ISONE, MISO, NYISO, PJM)
        zone: Pricing zone name
        days: Number of days of history (default 7)
    """
    client = _get_client()
    data = await client.get("/lmp/daily", {"iso": iso, "zone": zone, "days": days})
    return _fmt(data)


@mcp.tool()
async def get_capacity_prices(
    iso: str | None = None,
    year: int | None = None,
) -> str:
    """Get capacity market auction prices.

    Args:
        iso: ISO/RTO name
        year: Delivery year
    """
    client = _get_client()
    data = await client.get("/capacity/prices", {"iso": iso, "year": year})
    return _fmt(data)


@mcp.tool()
async def get_generators(
    state: str | None = None,
    fuel_type: str | None = None,
    min_mw: float | None = None,
    page: int = 1,
    per_page: int = 20,
) -> str:
    """Search EIA generator inventory (26,000+ generators).

    Args:
        state: US state abbreviation
        fuel_type: Fuel type (Solar, Wind, Natural Gas, Nuclear, etc.)
        min_mw: Minimum nameplate capacity in MW
        page: Page number
        per_page: Results per page
    """
    client = _get_client()
    data = await client.get("/generators", {
        "state": state, "fuel_type": fuel_type, "min_mw": min_mw,
        "page": page, "per_page": per_page,
    })
    return _fmt(data)


@mcp.tool()
async def get_technology_costs(
    technology: str | None = None,
    year: int | None = None,
) -> str:
    """Get NREL Annual Technology Baseline (ATB) cost projections.

    Levelized cost of energy, capital costs, and capacity factors for
    solar, wind, battery storage, natural gas, nuclear, and other technologies.

    Args:
        technology: Technology name
        year: Projection year
    """
    client = _get_client()
    data = await client.get("/technology-costs", {
        "technology": technology, "year": year,
    })
    return _fmt(data)


@mcp.tool()
async def check_domestic_content(queue_id: str) -> str:
    """Check domestic content eligibility for a project's ITC bonus (+10%).

    Analyzes whether a project can qualify for the domestic content bonus
    under IRA Section 45X, based on technology type and known supply chain data.

    Args:
        queue_id: The project's queue ID
    """
    client = _get_client()
    data = await client.get(f"/domestic-content/{queue_id}")
    return _fmt(data)


@mcp.tool()
async def get_grid_turbines(
    state: str | None = None,
    manufacturer: str | None = None,
    min_kw: float | None = None,
    page: int = 1,
    per_page: int = 20,
) -> str:
    """Search the US Wind Turbine Database (75,000+ turbines).

    Source: USGS/LBNL/AWEA Wind Turbine Database (USWTDB).

    Args:
        state: US state abbreviation
        manufacturer: Turbine manufacturer name
        min_kw: Minimum turbine capacity in kW
        page: Page number
        per_page: Results per page
    """
    client = _get_client()
    data = await client.get("/grid/turbines", {
        "state": state, "manufacturer": manufacturer, "min_kw": min_kw,
        "page": page, "per_page": per_page,
    })
    return _fmt(data)


@mcp.tool()
async def get_developer_stats() -> str:
    """Get aggregate developer statistics.

    Returns: total developers, breakdown by tier, average completion rates,
    developers needing capital, top headquarter states.
    """
    client = _get_client()
    data = await client.get("/developers/stats")
    return _fmt(data)


@mcp.tool()
async def get_dg_stats() -> str:
    """Get distributed generation aggregate statistics.

    Returns: project counts and capacity by state, type, and status.
    """
    client = _get_client()
    data = await client.get("/dg/stats")
    return _fmt(data)


def main():
    transport = "sse" if "--sse" in sys.argv else "stdio"
    mcp.run(transport=transport)


if __name__ == "__main__":
    main()
