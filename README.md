# uniswap-v3-analytics

Python CLI for querying Uniswap V3 on-chain data via [The Graph Protocol](https://thegraph.com). No RPC node needed - just HTTP.

## What it does

- Fetches top pools by TVL, top tokens by volume, recent swaps, OHLC candles, and factory global stats
- Outputs tables to stdout or exports to CSV/JSON
- Typed dataclasses for all entities (Pool, Token, Swap, FactoryStats)
- Auto-retry on network errors, configurable subgraph URL

## Files

```
uniswap-v3-analytics/
|-- client.py        # UniswapV3Client - HTTP queries with retry logic
|-- queries.py       # GraphQL query strings (pools, swaps, tokens, OHLC)
|-- models.py        # Dataclasses: Pool, Token, Swap, FactoryStats
|-- utils.py         # Price math: sqrtPriceX96, tick conversion, liquidity amounts
|-- main.py          # CLI entry point (argparse)
|-- requirements.txt
+-- .env.example
```

## Setup

```bash
git clone https://github.com/harshitdabra/uniswap-v3-analytics.git
cd uniswap-v3-analytics
pip install -r requirements.txt
cp .env.example .env
```

### API Key (required)

The Graph hosted service was shut down in 2023. You need a free API key from The Graph Studio:

1. Go to [thegraph.com/studio](https://thegraph.com/studio/)
2. Sign in with your wallet or email
3. Copy your API key from the dashboard
4. Add it to `.env`:

```
GRAPH_API_KEY=your_api_key_here
```

The subgraph being queried is the official [Uniswap V3 subgraph](https://thegraph.com/explorer/subgraphs/5zvR82QoaXYFyDEKLZ9t6v9adgnptxYpKpSbxtgVENFV) on the decentralized network.

## Usage

**Top 20 pools by TVL:**
```bash
python main.py pools
python main.py pools --limit 50 --out pools.csv
```

**Recent swaps on USDC/ETH pool:**
```bash
python main.py swaps 0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8
python main.py swaps 0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8 --limit 200 --out swaps.csv
```

**Top tokens by volume:**
```bash
python main.py tokens --limit 30
```

**Factory global stats:**
```bash
python main.py stats
python main.py stats --out stats.json
```

**OHLC daily candles for a pool:**
```bash
python main.py ohlc 0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8 --limit 90
```

**Custom subgraph URL:**
```bash
python main.py --url https://gateway.thegraph.com/api/<KEY>/subgraphs/id/<ID> pools
```

## Sample Output

```
$ python main.py pools --limit 5
       pool        pair    fee %         TVL  volume 24h  fees 24h    txns
 0x8ad599...  USDC/WETH   0.3000  $1.23B  $312.45M  $937.35K  124532
 0x4e68ca...  WBTC/WETH   0.3000  $892.10M  $89.23M  $267.69K   45231
 0x11b815...  WETH/USDT   0.3000  $543.20M  $67.12M  $201.36K   32198
 0x99ac8c...  WBTC/USDC   0.3000  $234.50M  $23.45M   $70.35K   15432
 0xcbcdf9...  WBTC/WETH   0.0500  $189.30M  $18.93M   $94.65K   12345
```

## Using as a library

```python
from client import UniswapV3Client
from utils import tick_to_price, sqrt_price_x96_to_price

client = UniswapV3Client()  # reads GRAPH_API_KEY from .env

pools = client.get_top_pools(limit=10)
for pool in pools:
    print(pool.pair(), pool.total_value_locked_usd)

stats = client.get_factory_stats()
print(stats.pool_count, stats.total_value_locked_usd)

swaps = client.get_pool_swaps("0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8", limit=50)
for s in swaps:
    print(s.timestamp, s.amount_usd)
```

## License

MIT - built by [Harshit Dabra](https://github.com/harshitdabra)
