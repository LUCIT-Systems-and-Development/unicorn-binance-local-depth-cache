#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯

from dotenv import load_dotenv
from pprint import pprint
from unicorn_binance_local_depth_cache import BinanceLocalDepthCacheManager, DepthCacheClusterNotReachableError
from unicorn_binance_rest_api import BinanceRestApiManager
import asyncio
import logging
import os

load_dotenv()

exchange: str = "binance.com"
ubdcc_address: str = os.getenv('UBDCC_ADDRESS')
ubdcc_port: int = int(os.getenv('UBDCC_PORT'))

logging.getLogger("unicorn_binance_local_depth_cache")
logging.basicConfig(level=logging.ERROR,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")


async def main():
    with BinanceRestApiManager(exchange=exchange) as ubra:
        if exchange == "binance.com" or exchange == "binance.us":
            exchange_info = ubra.get_exchange_info()
        elif exchange == "binance.com-futures":
            exchange_info = ubra.futures_exchange_info()
        else:
            raise ValueError(f"Unknown exchange: {exchange}")
        markets = []
        for item in exchange_info['symbols']:
            if item['status'] == "TRADING":
                markets.append(item['symbol'])
    result = await ubldc.cluster.create_depthcaches_async(exchange=exchange, markets=markets[1200:], desired_quantity=1)
    print(f"Adding {len(markets)} DepthCaches for exchange '{exchange}' on UBDCC '{ubdcc_address}':")
    pprint(result)

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
