#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯

from dotenv import load_dotenv
from unicorn_binance_local_depth_cache import (BinanceLocalDepthCacheManager, DepthCacheOutOfSync,
                                               DepthCacheClusterNotReachableError)
import asyncio
import logging
import os

load_dotenv()

footer: str = "By LUCIT - www.lucit.tech"
exchange: str = "binance.com-futures"
limit_count: int = 2
markets: list = ['1000SHIBUSDT', 'BTCUSDT', 'ETHUSDT']
title: str = "UBDCC Demo"
threshold_volume: float = 200000.0
threshold_volume_limit_count: int = 3
ubdcc_address: str = os.getenv('UBDCC_ADDRESS')
ubdcc_port: int = int(os.getenv('UBDCC_PORT'))
update_interval_ms: int = 100


logging.getLogger("unicorn_binance_local_depth_cache")
logging.basicConfig(level=logging.ERROR,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")


async def main():
    ubldc.cluster.create_depthcache(markets=markets)
    while ubldc.is_stop_request() is False:
        dividing_line = f"---------------------------------------------------------------------------------------------"
        add_string = dividing_line
        for market in markets:
            try:
                top_asks_limit = ubldc.cluster.get_asks(market=market, limit_count=limit_count)
                top_bids_limit = ubldc.cluster.get_bids(market=market, limit_count=limit_count)
                top_asks_threshold = ubldc.cluster.get_asks(market=market,
                                                            limit_count=threshold_volume_limit_count,
                                                            threshold_volume=threshold_volume)
                top_bids_threshold = ubldc.cluster.get_bids(market=market,
                                                            limit_count=threshold_volume_limit_count,
                                                            threshold_volume=threshold_volume)
            except DepthCacheOutOfSync:
                top_asks_limit = "Out of sync!"
                top_bids_limit = "Out of sync!"
                top_asks_threshold = "Out of sync!"
                top_bids_threshold = "Out of sync!"
            depth = (f"depth_cache '{market}' is in sync: \r\n " 
                     f"- top {limit_count} asks: {top_asks_limit}\r\n "
                     f"- top {limit_count} bids: {top_bids_limit}\r\n "
                     f"- top {threshold_volume_limit_count} asks vol. > {threshold_volume}: {top_asks_threshold}\r\n "
                     f"- top {threshold_volume_limit_count} bids vol. > {threshold_volume}: {top_bids_threshold}")
            add_string = f"{add_string}\r\n {depth}"
        add_string = f"{add_string}\r\n {dividing_line}"
        add_string = f"{add_string}\r\n UBDCC status: {ubldc.cluster.get_cluster_info()['result']}"
        ubldc.print_summary(add_string=add_string, footer=footer, title=title)
        await asyncio.sleep(1)

try:
    with BinanceLocalDepthCacheManager(exchange=exchange, ubdcc_address=ubdcc_address, ubdcc_port=ubdcc_port) as ubldc:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("\r\nGracefully stopping ...")
except DepthCacheClusterNotReachableError as error_msg:
    print(f"ERROR: {error_msg}")
