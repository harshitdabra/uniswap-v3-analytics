TOP_POOLS_QUERY = """
{
  pools(
    first: $limit
    orderBy: totalValueLockedUSD
    orderDirection: desc
    where: { totalValueLockedUSD_gt: "1000000" }
  ) {
    id
    token0 { id symbol name decimals }
    token1 { id symbol name decimals }
    feeTier
    liquidity
    sqrtPrice
    tick
    token0Price
    token1Price
    volumeToken0
    volumeToken1
    volumeUSD
    feesUSD
    txCount
    totalValueLockedToken0
    totalValueLockedToken1
    totalValueLockedUSD
    createdAtTimestamp
    createdAtBlockNumber
  }
}
"""

POOL_SWAPS_QUERY = """
{
  swaps(
    first: $limit
    orderBy: timestamp
    orderDirection: desc
    where: { pool: "$pool_id" }
  ) {
    id
    timestamp
    pool { id }
    token0 { symbol }
    token1 { symbol }
    sender
    recipient
    origin
    amount0
    amount1
    amountUSD
    sqrtPriceX96
    tick
    logIndex
  }
}
"""

TOP_TOKENS_QUERY = """
{
  tokens(
    first: $limit
    orderBy: volumeUSD
    orderDirection: desc
    where: { volumeUSD_gt: "1000000" }
  ) {
    id
    symbol
    name
    decimals
    totalSupply
    volume
    volumeUSD
    feesUSD
    txCount
    poolCount
    totalValueLocked
    totalValueLockedUSD
    derivedETH
  }
}
"""

FACTORY_STATS_QUERY = """
{
  factories(first: 1) {
    id
    poolCount
    txCount
    totalVolumeUSD
    totalVolumeETH
    totalFeesUSD
    totalFeesETH
    untrackedVolumeUSD
    totalValueLockedUSD
    totalValueLockedETH
    owner
  }
}
"""

POOL_DAY_DATA_QUERY = """
{
  poolDayDatas(
    first: $limit
    orderBy: date
    orderDirection: desc
    where: { pool: "$pool_id" }
  ) {
    date
    pool { id }
    liquidity
    sqrtPrice
    token0Price
    token1Price
    tick
    tvlUSD
    volumeToken0
    volumeToken1
    volumeUSD
    feesUSD
    txCount
    open
    high
    low
    close
  }
}
"""

TOKEN_HOUR_DATA_QUERY = """
{
  tokenHourDatas(
    first: $limit
    orderBy: periodStartUnix
    orderDirection: desc
    where: { token: "$token_id" }
  ) {
    periodStartUnix
    token { id symbol }
    volume
    volumeUSD
    totalValueLocked
    totalValueLockedUSD
    priceUSD
    feesUSD
    open
    high
    low
    close
  }
}
"""
