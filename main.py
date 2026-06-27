import argparse
import json
import sys
from datetime import datetime

import pandas as pd

from client import UniswapV3Client


def fmt_usd(v: float) -> str:
    if v >= 1e9:
        return f'${v/1e9:.2f}B'
    if v >= 1e6:
        return f'${v/1e6:.2f}M'
    if v >= 1e3:
        return f'${v/1e3:.2f}K'
    return f'${v:.2f}'


def cmd_pools(client: UniswapV3Client, args):
    pools = client.get_top_pools(limit=args.limit)
    rows = []
    for p in pools:
        rows.append({
            "pool": p.id[:10] + "...",
            "pair": p.pair(),
            "fee %": f"{p.fee_pct():.4f}",
            "TVL": fmt_usd(p.total_value_locked_usd),
            "volume 24h": fmt_usd(p.volume_usd),
            "fees 24h": fmt_usd(p.fees_usd),
            "txns": p.tx_count,
        })
    df = pd.DataFrame(rows)
    print(df.to_string(index=False))

    if args.out:
        df.to_csv(args.out, index=False)
        print(f"\nSaved to {args.out}")


def cmd_swaps(client: UniswapV3Client, args):
    swaps = client.get_pool_swaps(pool_id=args.pool, limit=args.limit)
    if not swaps:
        print("No swaps found.")
        return

    rows = []
    for s in swaps:
        rows.append({
            "time": s.timestamp.strftime("%Y-%m-%d %H:%M"),
            "pair": f"{s.token0_symbol}/{s.token1_symbol}",
            "amount0": f"{s.amount0:.4f}",
            "amount1": f"{s.amount1:.4f}",
            "USD": fmt_usd(s.amount_usd),
            "sender": s.sender[:10] + "...",
        })
    df = pd.DataFrame(rows)
    print(df.to_string(index=False))

    if args.out:
        df.to_csv(args.out, index=False)
        print(f"\nSaved to {args.out}")


def cmd_tokens(client: UniswapV3Client, args):
    tokens = client.get_top_tokens(limit=args.limit)
    rows = []
    for t in tokens:
        rows.append({
            "address": t.id[:10] + "...",
            "symbol": t.symbol,
            "volume USD": fmt_usd(t.volume_usd or 0),
            "TVL USD": fmt_usd(t.total_value_locked_usd or 0),
            "fees USD": fmt_usd(t.fees_usd or 0),
            "pools": t.pool_count,
            "txns": t.tx_count,
        })
    df = pd.DataFrame(rows)
    print(df.to_string(index=False))

    if args.out:
        df.to_csv(args.out, index=False)
        print(f"\nSaved to {args.out}")


def cmd_stats(client: UniswapV3Client, args):
    stats = client.get_factory_stats()
    if not stats:
        print("No factory data returned.")
        return

    print("Uniswap V3 Factory Stats")
    print(f"  pools:       {stats.pool_count:,}")
    print(f"  total txns:  {stats.tx_count:,}")
    print(f"  volume USD:  {fmt_usd(stats.total_volume_usd)}")
    print(f"  volume ETH:  {stats.total_volume_eth:.2f} ETH")
    print(f"  fees USD:    {fmt_usd(stats.total_fees_usd)}")
    print(f"  TVL USD:     {fmt_usd(stats.total_value_locked_usd)}")
    print(f"  TVL ETH:     {stats.total_value_locked_eth:.2f} ETH")
    print(f"  owner:       {stats.owner}")

    if args.out:
        with open(args.out, "w") as f:
            json.dump(stats.__dict__, f, indent=2)
        print(f"\nSaved to {args.out}")


def cmd_ohlc(client: UniswapV3Client, args):
    data = client.get_pool_day_data(pool_id=args.pool, limit=args.limit)
    if not data:
        print("No OHLC data found.")
        return

    rows = []
    for d in data:
        rows.append({
            "date": datetime.fromtimestamp(d["date"]).strftime("%Y-%m-%d"),
            "open": float(d["open"]),
            "high": float(d["high"]),
            "low": float(d["low"]),
            "close": float(d["close"]),
            "volume USD": fmt_usd(float(d["volumeUSD"])),
            "TVL USD": fmt_usd(float(d["tvlUSD"])),
            "txns": d["txCount"],
        })
    df = pd.DataFrame(rows)
    print(df.to_string(index=False))

    if args.out:
        df.to_csv(args.out, index=False)
        print(f"\nSaved to {args.out}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="uniswap-v3-analytics",
        description="Query Uniswap V3 on-chain data via The Graph Protocol",
    )
    parser.add_argument("--url", help="Custom subgraph URL")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_pools = sub.add_parser("pools", help="Top pools by TVL")
    p_pools.add_argument("--limit", type=int, default=20)
    p_pools.add_argument("--out", help="CSV output path")

    p_swaps = sub.add_parser("swaps", help="Recent swaps for a pool")
    p_swaps.add_argument("pool", help="Pool address")
    p_swaps.add_argument("--limit", type=int, default=50)
    p_swaps.add_argument("--out", help="CSV output path")

    p_tokens = sub.add_parser("tokens", help="Top tokens by volume")
    p_tokens.add_argument("--limit", type=int, default=20)
    p_tokens.add_argument("--out", help="CSV output path")

    sub.add_parser("stats", help="Factory global stats").add_argument("--out", help="JSON output path")

    p_ohlc = sub.add_parser("ohlc", help="Pool OHLC daily candles")
    p_ohlc.add_argument("pool", help="Pool address")
    p_ohlc.add_argument("--limit", type=int, default=30)
    p_ohlc.add_argument("--out", help="CSV output path")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    client = UniswapV3Client(url=args.url) if getattr(args, "url", None) else UniswapV3Client()

    dispatch = {
        "pools": cmd_pools,
        "swaps": cmd_swaps,
        "tokens": cmd_tokens,
        "stats": cmd_stats,
        "ohlc": cmd_ohlc,
    }

    try:
        dispatch[args.cmd](client, args)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
