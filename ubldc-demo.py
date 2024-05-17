#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯

from unicorn_binance_local_depth_cache import BinanceLocalDepthCacheManager, DepthCacheOutOfSync
from unicorn_binance_rest_api import BinanceRestApiManager
from typing import Optional
import asyncio
import logging
import os
import time

footer: str = "By LUCIT - www.lucit.tech"
exchange: str = "binance.com-futures"
limit_count: int = 2
markets: list = ['BTCUSDT', 'ETHUSDT']
title: str = "UBLDC Demo"
threshold_volume: float = 200000
threshold_volume_limit_count: int = 3
update_interval_ms: Optional[int] = None


logging.getLogger("unicorn_binance_local_depth_cache")
logging.basicConfig(level=logging.DEBUG,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")


async def main():
    ubldc.create_depth_cache(markets=markets)
    while ubldc.is_stop_request() is False:
        add_string = (f"binance_api_status={ubra.get_used_weight(cached=True)}\r\n "
                      f"---------------------------------------------------------------------------------------------")
        for market in markets:
            try:
                top_asks_limit = ubldc.get_asks(market=market, limit_count=limit_count)
                top_bids_limit = ubldc.get_bids(market=market, limit_count=limit_count)
                top_asks_threshold = ubldc.get_asks(market=market,
                                                    limit_count=threshold_volume_limit_count,
                                                    threshold_volume=threshold_volume)
                top_bids_threshold = ubldc.get_bids(market=market,
                                                    limit_count=threshold_volume_limit_count,
                                                    threshold_volume=threshold_volume)
            except DepthCacheOutOfSync:
                top_asks_limit = "Out of sync!"
                top_bids_limit = "Out of sync!"
                top_asks_threshold = "Out of sync!"
                top_bids_threshold = "Out of sync!"
            depth = (f"depth_cache '{market}' is in sync: {ubldc.is_depth_cache_synchronized(market=market)}\r\n " 
                     f"- top {limit_count} asks: {top_asks_limit}\r\n "
                     f"- top {limit_count} bids: {top_bids_limit}\r\n "
                     f"- top {threshold_volume_limit_count} asks vol. > {threshold_volume}: {top_asks_threshold}\r\n "
                     f"- top {threshold_volume_limit_count} bids vol. > {threshold_volume}: {top_bids_threshold}")
            add_string = f"{add_string}\r\n {depth}"

        if os.getenv('EXPORT_TO_PNG') is None:
            ubldc.print_summary(add_string=add_string, footer=footer, title=title)
            await asyncio.sleep(1)
        else:
            ubldc.ubwa.print_summary_to_png(add_string=add_string,
                                            height_per_row=13.5,
                                            print_summary_export_path="/var/www/html/",
                                            footer=footer,
                                            title=title)
            await asyncio.sleep(10)


ubra = BinanceRestApiManager(exchange=exchange)
with BinanceLocalDepthCacheManager(exchange=exchange,
                                   init_time_window=5,
                                   ubra_manager=ubra,
                                   websocket_ping_interval=10,
                                   websocket_ping_timeout=15,
                                   depth_cache_update_interval=update_interval_ms) as ubldc:
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\r\nGracefully stopping ...")
    except Exception as e:
        print(f"\r\nERROR: {e}")
        print("Gracefully stopping ...")
