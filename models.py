from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class Token:
    id: str
    symbol: str
    name: str
    decimals: int
    total_supply: Optional[str] = None
    volume: Optional[float] = None
    volume_usd: Optional[float] = None
    fees_usd: Optional[float] = None
    tx_count: Optional[int] = None
    pool_count: Optional[int] = None
    total_value_locked: Optional[float] = None
    total_value_locked_usd: Optional[float] = None
    derived_eth: Optional[float] = None

    @classmethod
    def from_dict(cls, d: dict) -> "Token":
        return cls(
            id=d["id"],
            symbol=d["symbol"],
            name=d["name"],
            decimals=int(d["decimals"]),
            total_supply=d.get("totalSupply"),
            volume=float(d["volume"]) if d.get("volume") else None,
            volume_usd=float(d["volumeUSD"]) if d.get("volumeUSD") else None,
            fees_usd=float(d["feesUSD"]) if d.get("feesUSD") else None,
            tx_count=int(d["txCount"]) if d.get("txCount") else None,
            pool_count=int(d["poolCount"]) if d.get("poolCount") else None,
            total_value_locked=float(d["totalValueLocked"]) if d.get("totalValueLocked") else None,
            total_value_locked_usd=float(d["totalValueLockedUSD"]) if d.get("totalValueLockedUSD") else None,
            derived_eth=float(d["derivedETH"]) if d.get("derivedETH") else None,
        )


@dataclass
class Pool:
    id: str
    token0: Token
    token1: Token
    fee_tier: int
    liquidity: int
    sqrt_price: int
    tick: Optional[int]
    token0_price: float
    token1_price: float
    volume_token0: float
    volume_token1: float
    volume_usd: float
    fees_usd: float
    tx_count: int
    total_value_locked_token0: float
    total_value_locked_token1: float
    total_value_locked_usd: float
    created_at: Optional[datetime] = None
    created_at_block: Optional[int] = None

    @classmethod
    def from_dict(cls, d: dict) -> "Pool":
        return cls(
            id=d["id"],
            token0=Token.from_dict(d["token0"]),
            token1=Token.from_dict(d["token1"]),
            fee_tier=int(d["feeTier"]),
            liquidity=int(d["liquidity"]),
            sqrt_price=int(d["sqrtPrice"]),
            tick=int(d["tick"]) if d.get("tick") is not None else None,
            token0_price=float(d["token0Price"]),
            token1_price=float(d["token1Price"]),
            volume_token0=float(d["volumeToken0"]),
            volume_token1=float(d["volumeToken1"]),
            volume_usd=float(d["volumeUSD"]),
            fees_usd=float(d["feesUSD"]),
            tx_count=int(d["txCount"]),
            total_value_locked_token0=float(d["totalValueLockedToken0"]),
            total_value_locked_token1=float(d["totalValueLockedToken1"]),
            total_value_locked_usd=float(d["totalValueLockedUSD"]),
            created_at=datetime.fromtimestamp(int(d["createdAtTimestamp"])) if d.get("createdAtTimestamp") else None,
            created_at_block=int(d["createdAtBlockNumber"]) if d.get("createdAtBlockNumber") else None,
        )

    def pair(self) -> str:
        return f"{self.token0.symbol}/{self.token1.symbol}"

    def fee_pct(self) -> float:
        return self.fee_tier / 1_000_000 * 100


@dataclass
class Swap:
    id: str
    timestamp: datetime
    pool_id: str
    token0_symbol: str
    token1_symbol: str
    sender: str
    recipient: str
    origin: str
    amount0: float
    amount1: float
    amount_usd: float
    sqrt_price_x96: int
    tick: int
    log_index: int

    @classmethod
    def from_dict(cls, d: dict) -> "Swap":
        return cls(
            id=d["id"],
            timestamp=datetime.fromtimestamp(int(d["timestamp"])),
            pool_id=d["pool"]["id"],
            token0_symbol=d["token0"]["symbol"],
            token1_symbol=d["token1"]["symbol"],
            sender=d["sender"],
            recipient=d["recipient"],
            origin=d["origin"],
            amount0=float(d["amount0"]),
            amount1=float(d["amount1"]),
            amount_usd=float(d["amountUSD"]),
            sqrt_price_x96=int(d["sqrtPriceX96"]),
            tick=int(d["tick"]),
            log_index=int(d["logIndex"]),
        )


@dataclass
class FactoryStats:
    id: str
    pool_count: int
    tx_count: int
    total_volume_usd: float
    total_volume_eth: float
    total_fees_usd: float
    total_fees_eth: float
    untracked_volume_usd: float
    total_value_locked_usd: float
    total_value_locked_eth: float
    owner: str

    @classmethod
    def from_dict(cls, d: dict) -> "FactoryStats":
        return cls(
            id=d["id"],
            pool_count=int(d["poolCount"]),
            tx_count=int(d["txCount"]),
            total_volume_usd=float(d["totalVolumeUSD"]),
            total_volume_eth=float(d["totalVolumeETH"]),
            total_fees_usd=float(d["totalFeesUSD"]),
            total_fees_eth=float(d["totalFeesETH"]),
            untracked_volume_usd=float(d["untrackedVolumeUSD"]),
            total_value_locked_usd=float(d["totalValueLockedUSD"]),
            total_value_locked_eth=float(d["totalValueLockedETH"]),
            owner=d["owner"],
        )
