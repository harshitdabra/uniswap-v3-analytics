# uniswap-v3-analytics

A Python CLI for pulling Uniswap V3 data (pools, swaps, tokens, TVL) straight from The Graph, so you don't need to run your own RPC node.

## What it does

It grabs the top pools by TVL, the top tokens by volume, recent swaps on a pool, daily OHLC candles, and overall factory stats. Results print to your terminal, or you can export them to CSV/JSON.

## Setup

```
git clone https://github.com/harshitdabra/uniswap-v3-analytics.git
cd uniswap-v3-analytics
pip install -r requirements.txt
cp .env.example .env
```

You'll need a free API key from The Graph Studio since the old hosted service shut down in 2023. Sign in at thegraph.com/studio, copy your key, and add it to `.env` as `GRAPH_API_KEY`.

## Usage

```
python main.py pools --limit 50 --out pools.csv
python main.py swaps 0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8 --limit 200
python main.py tokens --limit 30
python main.py stats
python main.py ohlc 0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8 --limit 90
```

You can point it at a different subgraph URL with `--url` if you need to.

The code is split into a few files. `client.py` does the HTTP calls and retry logic, `queries.py` holds the GraphQL strings, `models.py` has the dataclasses (Pool, Token, Swap, FactoryStats), and `utils.py` handles the price math like sqrtPriceX96 conversion.

You can also use it as a library instead of the CLI:

```python
from client import UniswapV3Client

client = UniswapV3Client()
pools = client.get_top_pools(limit=10)
for pool in pools:
    print(pool.pair(), pool.total_value_locked_usd)
```

MIT licensed.
