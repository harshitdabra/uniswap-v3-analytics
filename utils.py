import math
from decimal import Decimal
from typing import Tuple

Q96 = 2 ** 96
Q192 = 2 ** 192


def sqrt_price_x96_to_price(sqrt_price_x96: int, token0_decimals: int, token1_decimals: int) -> Tuple[float, float]:
    """Convert sqrtPriceX96 to token prices."""
    if sqrt_price_x96 == 0:
        return 0.0, 0.0

    price_raw = Decimal(sqrt_price_x96) ** 2 / Decimal(Q192)
    decimal_adj = Decimal(10 ** token0_decimals) / Decimal(10 ** token1_decimals)
    token0_price = float(price_raw * decimal_adj)
    token1_price = 1.0 / token0_price if token0_price else 0.0
    return token0_price, token1_price


def tick_to_price(tick: int, token0_decimals: int = 18, token1_decimals: int = 18) -> float:
    """Convert a Uniswap V3 tick to price."""
    raw = 1.0001 ** tick
    return raw * (10 ** token0_decimals) / (10 ** token1_decimals)


def fee_tier_to_pct(fee_tier: int) -> float:
    return fee_tier / 1_000_000 * 100


def token_amount(raw_amount: int, decimals: int) -> float:
    """Convert raw on-chain integer amount to human-readable float."""
    if decimals == 0:
        return float(raw_amount)
    return raw_amount / (10 ** decimals)


def compute_tvl_usd(amount0: float, amount1: float, price0_usd: float, price1_usd: float) -> float:
    return amount0 * price0_usd + amount1 * price1_usd


def liquidity_to_amounts(
    liquidity: int,
    sqrt_price_x96: int,
    tick_lower: int,
    tick_upper: int,
    token0_decimals: int = 18,
    token1_decimals: int = 18,
) -> Tuple[float, float]:
    """Approximate token amounts from liquidity position."""
    sqrt_lower = math.sqrt(1.0001 ** tick_lower) * Q96
    sqrt_upper = math.sqrt(1.0001 ** tick_upper) * Q96
    sqrt_current = sqrt_price_x96

    if sqrt_current <= sqrt_lower:
        amount0 = liquidity * (sqrt_upper - sqrt_lower) / (sqrt_lower * sqrt_upper / Q96)
        amount1 = 0.0
    elif sqrt_current >= sqrt_upper:
        amount0 = 0.0
        amount1 = liquidity * (sqrt_upper - sqrt_lower) / Q96
    else:
        amount0 = liquidity * (sqrt_upper - sqrt_current) / (sqrt_current * sqrt_upper / Q96)
        amount1 = liquidity * (sqrt_current - sqrt_lower) / Q96

    return token_amount(int(amount0), token0_decimals), token_amount(int(amount1), token1_decimals)
