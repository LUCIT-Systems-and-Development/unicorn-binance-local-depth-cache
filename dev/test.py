#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯
import time

from dotenv import load_dotenv
from unicorn_binance_local_depth_cache import (BinanceLocalDepthCacheManager, DepthCacheOutOfSync,
                                               DepthCacheAlreadyStopped)
from unicorn_binance_rest_api import BinanceRestApiManager
import asyncio
import logging
import os

amount_test_caches: int = 40

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
    markets = markets[:amount_test_caches]
    ubldc.create_depthcache(markets=markets)
    while ubldc.is_stop_request() is False:
        working = []
        non_working = []
        for market in markets:
            try:
                ubldc.get_asks(market=market, limit_count=1)
                working.append(market)
            except DepthCacheOutOfSync:
                non_working.append(market)
            except DepthCacheAlreadyStopped:
                non_working.append(market)
        ubldc.print_summary(add_string=f"Working: {len(working)}, Non-Working: {len(non_working)}")
        await asyncio.sleep(60)


with BinanceLocalDepthCacheManager(exchange="binance.com-futures") as ubldc:
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\r\nGracefully stopping ...")
