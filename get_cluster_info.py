#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯

import asyncio
import logging
import os
from pprint import pprint
from unicorn_binance_local_depth_cache import BinanceLocalDepthCacheManager, DepthCacheClusterNotReachableError

footer: str = "By LUCIT - www.lucit.tech"
exchange: str = "binance.com-futures"
limit_count: int = 2
markets: list = ['1000SHIBUSDT', 'BTCUSDT', 'ETHUSDT']
title: str = "UBLDC Demo"
threshold_volume: float = 200000.0
threshold_volume_limit_count: int = 3
update_interval_ms: int = 100

ubdcc_address = ""

logging.getLogger("unicorn_binance_local_depth_cache")
logging.basicConfig(level=logging.INFO,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")


async def main():
    pprint(ubldc.cluster.get_cluster_info(), depth=4)
    await asyncio.sleep(1)

try:
    with BinanceLocalDepthCacheManager(exchange=exchange, ubdcc_address=ubdcc_address) as ubldc:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("\r\nGracefully stopping ...")
except DepthCacheClusterNotReachableError as error_msg:
    print(f"ERROR: {error_msg}")
