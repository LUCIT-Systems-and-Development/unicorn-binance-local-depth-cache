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

exchange: str = "binance.com-futures"
ubdcc_address: str = os.getenv('UBDCC_ADDRESS')
ubdcc_port: int = int(os.getenv('UBDCC_PORT'))

logging.getLogger("unicorn_binance_local_depth_cache")
logging.basicConfig(level=logging.ERROR,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")


async def main():
    dc = await ubldc.cluster.get_depthcache_list_async()
    for dcl_exchange in dc['depthcache_list']:
        print(f"Stopping {len(dc['depthcache_list'][dcl_exchange])} DepthCaches for exchange '{dcl_exchange}' on UBDCC "
              f"'{ubdcc_address}'!")
        loop = 1
        for market in dc['depthcache_list'][dcl_exchange]:
            print(f"Stopping DepthCache #{loop}: {market}")
            pprint(ubldc.cluster.stop_depthcache(exchange=dcl_exchange, market=market, debug=True))
            loop += 1
    await asyncio.sleep(1)

try:
    with BinanceLocalDepthCacheManager(exchange=exchange, ubdcc_address=ubdcc_address, ubdcc_port=ubdcc_port) as ubldc:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("\r\nGracefully stopping ...")
except DepthCacheClusterNotReachableError as error_msg:
    print(f"ERROR: {error_msg}")
