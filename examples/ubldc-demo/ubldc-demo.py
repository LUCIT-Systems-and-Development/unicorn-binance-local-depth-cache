#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯

from dotenv import load_dotenv
from unicorn_binance_local_depth_cache import BinanceLocalDepthCacheManager, DepthCacheOutOfSync
import asyncio
import logging
import os

amount_test_caches: int = 5
footer: str = "By LUCIT - www.lucit.tech"
exchange: str = "binance.com-futures"
limit_count: int = 2
title: str = "UBLDC Demo"
threshold_volume: float = 200000.0
threshold_volume_limit_count: int = 3
update_interval_ms: int = 100

logging.getLogger("unicorn_binance_local_depth_cache")
logging.basicConfig(level=logging.DEBUG,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")
load_dotenv()


async def main():
    ubra = ubldc.get_ubra_manager()
    exchange_info = ubra.futures_exchange_info()
    markets = []
    for item in exchange_info['symbols']:
        if item['symbol'].endswith("USDT") and item['status'] == "TRADING":
            markets.append(item['symbol'])
    markets = markets[:amount_test_caches]

    ubldc.create_depth_cache(markets=markets)
    while ubldc.is_stop_request() is False:
        add_string = f"---------------------------------------------------------------------------------------------"
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
            ubldc.print_summary_to_png(add_string=add_string,
                                       height_per_row=13.5,
                                       print_summary_export_path="/var/www/html/",
                                       footer=footer,
                                       title=title)
            await asyncio.sleep(10)


with BinanceLocalDepthCacheManager(exchange=exchange,
                                   auto_data_cleanup_stopped_streams=True,
                                   depth_cache_update_interval=update_interval_ms,
                                   websocket_ping_interval=10,
                                   websocket_ping_timeout=15) as ubldc:
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\r\nGracefully stopping ...")

