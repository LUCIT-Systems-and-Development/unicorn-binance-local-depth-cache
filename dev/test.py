#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯

from dotenv import load_dotenv
from unicorn_binance_local_depth_cache import BinanceLocalDepthCacheManager, DepthCacheOutOfSync
from unicorn_binance_rest_api import BinanceRestApiManager
import asyncio
import logging
import os

limit_count: int = 2
threshold_volume: float = 200000.0
threshold_volume_limit_count: int = 3

logging.getLogger("unicorn_binance_local_depth_cache")
logging.basicConfig(level=logging.DEBUG,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")
load_dotenv()


async def main():
    with BinanceRestApiManager(exchange="binance.com-futures") as ubra:
        exchange_info = ubra.futures_exchange_info()
    markets = []
    for item in exchange_info['symbols']:
        if item['symbol'].endswith("USDT") and item['status'] == "TRADING":
            markets.append(item['symbol'])
    markets = markets[:210]
    print(f"Start DC ...")
    ubldc.create_depth_cache(markets=markets)
    print(f"DC started!")
    while ubldc.is_stop_request() is False:
        print(f"---------------------------------------------------------------------------------------------")
        for market in markets:
            try:
                top_asks_limit = ubldc.get_asks(market=market, limit_count=limit_count)
                depth = (f"depth_cache '{market}' is in sync: {ubldc.is_depth_cache_synchronized(market=market)} "
                         f"- top {limit_count} asks: {top_asks_limit}")
            except DepthCacheOutOfSync:
                depth = (f"depth_cache '{market}' is in sync: {ubldc.is_depth_cache_synchronized(market=market)}")
            print(depth)
        await asyncio.sleep(2)


with BinanceLocalDepthCacheManager(exchange="binance.com-futures") as ubldc:
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\r\nGracefully stopping ...")
