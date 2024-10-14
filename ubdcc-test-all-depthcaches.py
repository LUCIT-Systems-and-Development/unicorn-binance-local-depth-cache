#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯

from unicorn_binance_local_depth_cache import BinanceLocalDepthCacheManager, DepthCacheClusterNotReachableError
import asyncio
import logging
import os

exchange: str = "binance.com-futures"
limit_count: int = 2
threshold_volume: float = 200000.0
ubdcc_address = ""

logging.getLogger("unicorn_binance_local_depth_cache")
logging.basicConfig(level=logging.INFO,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")


async def main():
    dc = ubldc.cluster.get_depthcache_list()
    errors = {}
    non_working_caches = []
    working_caches = []
    for dcl_exchange in dc['depthcache_list']:
        print(f"Testing {len(dc['depthcache_list'][dcl_exchange])} DepthCaches for exchange '{dcl_exchange}' on UBDCC "
              f"'{ubdcc_address}'!")
        loop = 1
        for market in dc['depthcache_list'][dcl_exchange]:
            asks = ubldc.cluster.get_asks(exchange=dcl_exchange, market=market,
                                          limit_count=limit_count, threshold_volume=threshold_volume)
            if asks.get('error_id') is not None:
                print(f"Asks from DepthCache #{loop} '{market}' failed: {asks.get('error_id')} - {asks.get('message')}\r\n"
                      f"{asks.get('requests')}")
                errors[asks.get('error_id')] = 1 if errors.get(asks.get('error_id')) is None else errors.get(asks.get('error_id')) + 1
                non_working_caches.append(market)
            else:
                print(f"Asks from DepthCache #{loop} '{market}': {asks}")
                working_caches.append(market)
            loop += 1

    print(f"Successful working caches: {len(working_caches)}")
    for error in errors:
        print(f"ERROR: {error}: {errors[error]}")

    print(f"exclude={non_working_caches}")
    await asyncio.sleep(1)

try:
    with BinanceLocalDepthCacheManager(exchange=exchange, ubdcc_address=ubdcc_address) as ubldc:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("\r\nGracefully stopping ...")
except DepthCacheClusterNotReachableError as error_msg:
    print(f"ERROR: {error_msg}")
