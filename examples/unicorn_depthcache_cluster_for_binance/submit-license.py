#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯

from dotenv import load_dotenv
import asyncio
import logging
import os
from pprint import pprint
from unicorn_binance_local_depth_cache import BinanceLocalDepthCacheManager, DepthCacheClusterNotReachableError

load_dotenv()

api_secret: str = os.getenv('API_SECRET')
footer: str = "By LUCIT - www.lucit.tech"
exchange: str = "binance.com-futures"
license_token: str = os.getenv('LICENSE_TOKEN')
limit_count: int = 2
markets: list = ['1000SHIBUSDT', 'BTCUSDT', 'ETHUSDT']
title: str = "UBDCC Demo"
threshold_volume: float = 200000.0
threshold_volume_limit_count: int = 3
update_interval_ms: int = 100
ubdcc_address: str = os.getenv('UBDCC_ADDRESS')
ubdcc_port: int = int(os.getenv('UBDCC_PORT'))


logging.getLogger("unicorn_binance_local_depth_cache")
logging.basicConfig(level=logging.ERROR,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")


async def main():
    pprint(ubldc.cluster.submit_license(api_secret=api_secret, license_token=license_token, debug=True))

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
