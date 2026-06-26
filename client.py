import os
import time
import requests
from typing import Optional
from dotenv import load_dotenv

from models import Pool, Token, Swap, FactoryStats
from queries import (
    TOP_POOLS_QUERY,
    POOL_SWAPS_QUERY,
    TOP_TOKENS_QUERY,
    FACTORY_STATS_QUERY,
    POOL_DAY_DATA_QUERY,
    TOKEN_HOUR_DATA_QUERY,
)

load_dotenv()

SUBGRAPH_URL = os.getenv(
    "SUBGRAPH_URL",
    "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3",
)

RETRY_ATTEMPTS = 3
RETRY_DELAY = 2


class UniswapV3Client:
    def __init__(self, url: str = SUBGRAPH_URL, timeout: int = 30):
        self.url = url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def _query(self, gql: str) -> dict:
        payload = {"query": gql}
        for attempt in range(RETRY_ATTEMPTS):
            try:
                resp = self.session.post(self.url, json=payload, timeout=self.timeout)
                resp.raise_for_status()
                data = resp.json()
                if "errors" in data:
                    raise ValueError(f"GraphQL errors: {data['errors']}")
                return data["data"]
            except (requests.RequestException, ValueError) as e:
                if attempt == RETRY_ATTEMPTS - 1:
                    raise
                time.sleep(RETRY_DELAY * (attempt + 1))
        return {}

    def get_top_pools(self, limit: int = 20) -> list[Pool]:
        gql = TOP_POOLS_QUERY.replace("$limit", str(limit))
        data = self._query(gql)
        return [Pool.from_dict(p) for p in data.get("pools", [])]

    def get_pool_swaps(self, pool_id: str, limit: int = 100) -> list[Swap]:
        gql = POOL_SWAPS_QUERY.replace("$limit", str(limit)).replace("$pool_id", pool_id.lower())
        data = self._query(gql)
        return [Swap.from_dict(s) for s in data.get("swaps", [])]

    def get_top_tokens(self, limit: int = 20) -> list[Token]:
        gql = TOP_TOKENS_QUERY.replace("$limit", str(limit))
        data = self._query(gql)
        return [Token.from_dict(t) for t in data.get("tokens", [])]

    def get_factory_stats(self) -> Optional[FactoryStats]:
        data = self._query(FACTORY_STATS_QUERY)
        factories = data.get("factories", [])
        return FactoryStats.from_dict(factories[0]) if factories else None

    def get_pool_day_data(self, pool_id: str, limit: int = 30) -> list[dict]:
        gql = POOL_DAY_DATA_QUERY.replace("$limit", str(limit)).replace("$pool_id", pool_id.lower())
        data = self._query(gql)
        return data.get("poolDayDatas", [])

    def get_token_hour_data(self, token_id: str, limit: int = 48) -> list[dict]:
        gql = TOKEN_HOUR_DATA_QUERY.replace("$limit", str(limit)).replace("$token_id", token_id.lower())
        data = self._query(gql)
        return data.get("tokenHourDatas", [])
