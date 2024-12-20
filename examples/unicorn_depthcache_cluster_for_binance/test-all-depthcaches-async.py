#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯

from dotenv import load_dotenv
from pprint import pprint
from unicorn_binance_local_depth_cache import BinanceLocalDepthCacheManager, DepthCacheClusterNotReachableError
import asyncio
import logging
import os

load_dotenv()

exchange: str = "binance.com"
limit_count: int = 2
threshold_volume: float = 20000.0
ubdcc_address: str = os.getenv('UBDCC_ADDRESS')
ubdcc_port: int = int(os.getenv('UBDCC_PORT'))

logging.getLogger("unicorn_binance_local_depth_cache")
logging.basicConfig(level=logging.ERROR,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")


async def main():
    dc = await ubldc.cluster.get_depthcache_list_async(debug=False)
    errors = {}
    non_working_caches = []
    working_caches = []
    for dcl_exchange in dc['depthcache_list']:
        print(f"Testing {len(dc['depthcache_list'][dcl_exchange])} DepthCaches for exchange '{dcl_exchange}' on UBDCC "
              f"'{ubdcc_address}'!")
        loop = 1
        for market in dc['depthcache_list'][dcl_exchange]:
            asks = await ubldc.cluster.get_asks_async(exchange=dcl_exchange, market=market, limit_count=limit_count,
                                                      threshold_volume=threshold_volume, debug=True)
            if asks.get('error_id') is not None:
                print(f"Asks from DepthCache #{loop} '{market}' failed: {asks.get('error_id')} - {asks.get('message')}")
                pprint(asks)
                errors[asks.get('error_id')] = 1 if errors.get(asks.get('error_id')) is None else errors.get(asks.get('error_id')) + 1
                non_working_caches.append(market)
            else:
                print(f"Asks from DepthCache #{loop} '{market}':")
                pprint(asks)
                working_caches.append(market)
            loop += 1

    print(f"Successful working caches: {len(working_caches)}")
    if len(errors) > 0:
        print(f"ERRORS:")
        pprint(errors)
    await asyncio.sleep(1)

try:
    with BinanceLocalDepthCacheManager(exchange=exchange, ubdcc_address=ubdcc_address, ubdcc_port=ubdcc_port) as ubldc:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("\r\nGracefully stopping ...")
        except Exception as error_msg:
            print(f"ERROR: {error_msg}")
except DepthCacheClusterNotReachableError as error_msg:
    print(f"ERROR: {error_msg}")
