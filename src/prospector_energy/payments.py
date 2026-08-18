"""MPP (Machine Payments Protocol) integration for paid tool access.

Enables AI agents to pay per-tool-call via stablecoins (USDC on Tempo)
using the x402/MPP protocol. Payment is opt-in: if MPP_RECIPIENT_ADDRESS
is not set, all tools work as before (free, with API key rate limits).

Environment:
    MPP_RECIPIENT_ADDRESS — Your wallet address to receive payments (required to enable)
    MPP_SECRET_KEY        — HMAC secret for challenge verification (auto-generated if not set)
    MPP_CURRENCY          — Token contract address (default: pathUSD on Tempo)
    MPP_CHAIN_ID          — Chain ID (default: 42431 for Tempo mainnet)
    MPP_RPC_URL           — RPC URL (default: Tempo mainnet)
    MPP_REALM             — Server realm for challenges (default: prospectorlabs.io)
"""

import os
import secrets
from functools import wraps
from typing import Any, Callable

# Pricing tiers (amounts in smallest unit — 6 decimals for USDC, so 1000 = $0.001)
# These are per-tool-call prices in pathUSD (USDC equivalent)
PRICING = {
    # Free tools (no payment required) — discovery and aggregate stats
    "free": [
        "get_queue_stats",
        "get_developer_stats",
        "get_dg_stats",
        "get_investable_summary",
        "get_dg_investable_summary",
        "get_itc_summary",
        "get_milestone_summary",
        "get_lmp_zones",
    ],
    # Standard tier — $0.01 per call (10000 = 0.01 USDC with 6 decimals)
    "standard": {
        "amount": "10000",
        "tools": [
            "search_projects",
            "search_dg_projects",
            "search_developers",
            "get_generators",
            "get_grid_turbines",
            "get_grid_transmission",
            "get_grid_substations",
            "get_lmp_daily",
            "get_lmp_monthly",
            "get_capacity_prices",
            "get_fuel_prices",
            "get_rto_generation",
            "get_technology_costs",
            "get_developer_projects",
        ],
    },
    # Premium tier — $0.05 per call
    "premium": {
        "amount": "50000",
        "tools": [
            "get_project",
            "get_developer",
            "get_project_score",
            "calculate_tax_credits",
            "check_domestic_content",
            "find_itc_deals",
            "get_itc_deal",
            "get_investable_projects",
            "get_investable_dg_projects",
        ],
    },
    # Pro tier — $0.10 per call
    "pro": {
        "amount": "100000",
        "tools": [
            "get_deal_sheet",
            "export_projects",
        ],
    },
}

# Default Tempo mainnet pathUSD token address
DEFAULT_CURRENCY = "0x20c0000000000000000000000000000000000000"
DEFAULT_CHAIN_ID = 42431
DEFAULT_RPC_URL = "https://rpc.tempo.xyz/"
DEFAULT_REALM = "prospectorlabs.io"


def _get_config() -> dict[str, Any] | None:
    """Get MPP configuration from environment. Returns None if not configured."""
    recipient = os.environ.get("MPP_RECIPIENT_ADDRESS")
    if not recipient:
        return None

    return {
        "recipient": recipient,
        "secret_key": os.environ.get("MPP_SECRET_KEY", secrets.token_hex(32)),
        "currency": os.environ.get("MPP_CURRENCY", DEFAULT_CURRENCY),
        "chain_id": int(os.environ.get("MPP_CHAIN_ID", DEFAULT_CHAIN_ID)),
        "rpc_url": os.environ.get("MPP_RPC_URL", DEFAULT_RPC_URL),
        "realm": os.environ.get("MPP_REALM", DEFAULT_REALM),
    }


def _get_price(tool_name: str) -> str | None:
    """Get the price for a tool. Returns None if free."""
    if tool_name in PRICING["free"]:
        return None
    for tier in ["standard", "premium", "pro"]:
        if tool_name in PRICING[tier]["tools"]:
            return PRICING[tier]["amount"]
    # Unknown tools default to standard pricing
    return PRICING["standard"]["amount"]


def _get_tier_name(tool_name: str) -> str:
    """Get human-readable tier name for a tool."""
    if tool_name in PRICING["free"]:
        return "free"
    for tier in ["standard", "premium", "pro"]:
        if tool_name in PRICING[tier]["tools"]:
            return tier
    return "standard"


# Try to import MPP — graceful fallback if not installed
_mpp_available = False
_pay_decorator = None
_ChargeIntent = None
_payment_capabilities = None

try:
    from mpp.extensions.mcp import pay, payment_capabilities
    from mpp.methods.tempo import ChargeIntent

    _mpp_available = True
    _pay_decorator = pay
    _ChargeIntent = ChargeIntent
    _payment_capabilities = payment_capabilities
except ImportError:
    pass


def get_payment_capabilities() -> dict[str, Any] | None:
    """Get MCP payment capabilities dict, or None if MPP not available."""
    config = _get_config()
    if not config or not _mpp_available or not _payment_capabilities:
        return None
    return _payment_capabilities(["tempo"], ["charge"])


def paid_tool(tool_name: str) -> Callable:
    """Decorator that adds MPP payment to a tool if configured.

    If MPP is not installed or not configured, returns the tool unchanged.
    Free-tier tools are never wrapped.
    """
    def decorator(func: Callable) -> Callable:
        config = _get_config()
        price = _get_price(tool_name)

        # No payment needed: free tool, MPP not installed, or not configured
        if price is None or not _mpp_available or config is None:
            return func

        # Build the payment request
        payment_request = {
            "amount": price,
            "currency": config["currency"],
            "recipient": config["recipient"],
            "methodDetails": {
                "chainId": config["chain_id"],
                "feePayer": True,
            },
        }

        tier = _get_tier_name(tool_name)
        description = f"Prospector Labs energy data — {tool_name} ({tier} tier)"

        # Apply MPP @pay decorator
        return _pay_decorator(
            intent=_ChargeIntent(rpc_url=config["rpc_url"]),
            request=payment_request,
            realm=config["realm"],
            secret_key=config["secret_key"],
            description=description,
        )(func)

    return decorator


def is_payments_enabled() -> bool:
    """Check if MPP payments are configured and available."""
    return _mpp_available and _get_config() is not None


def get_pricing_info() -> dict[str, Any]:
    """Get pricing info for all tools (useful for documentation)."""
    enabled = is_payments_enabled()
    info = {
        "enabled": enabled,
        "currency": "USDC (pathUSD)",
        "plans_url": "https://api.prospectorlabs.io/plans",
        "note": (
            "Per-call MPP amounts below are ACTIVE on this instance."
            if enabled
            else "This instance charges nothing per call — MPP is not configured, so the "
            "amounts below are inert. Access is governed by your API key's plan; "
            "see plans_url."
        ),
        "tiers": {},
    }
    for tier_name in ["free", "standard", "premium", "pro"]:
        tier_data = PRICING[tier_name]
        if tier_name == "free":
            info["tiers"][tier_name] = {
                "price": "$0.00",
                "tools": tier_data,
            }
        else:
            amount = int(tier_data["amount"])
            price_usd = amount / 1_000_000
            info["tiers"][tier_name] = {
                "price": f"${price_usd:.2f}",
                "amount_raw": tier_data["amount"],
                "tools": tier_data["tools"],
            }
    return info
