#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯

from unicorn_binance_local_depth_cache import BinanceLocalDepthCacheManager
from typing import Optional
import asyncio
import logging
import os


amount_test_caches: int = 40
exchange: str = "binance.com"
update_interval_ms: int | None = None

logging.getLogger("unicorn_binance_local_depth_cache")
logging.basicConfig(level=logging.DEBUG,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")


async def main():
    ubra = ubldc.get_ubra_manager()
    exchange_info = ubra.get_exchange_info()
    markets = []
    for item in exchange_info['symbols']:
        if item['symbol'].endswith("USDT") and item['status'] == "TRADING":
            markets.append(item['symbol'])
    markets = markets[:amount_test_caches]

    print(f"Starting {exchange} DepthCaches for {len(markets)} markets: {markets}")
    ubldc.create_depthcache(markets=markets)

    while ubldc.is_stop_request() is False:
        markets_synced: list = []
        markets_not_synced: list = []
        for market in markets:
            if ubldc.is_depth_cache_synchronized(market=market) is True:
                markets_synced.append(market)
            else:
                markets_not_synced.append(market)
        add_string = (f"---------------------------------------------------------------------------------------------"
                      f"\r\n NOT SYNCED: {markets_not_synced}\r\n SYNCED: {markets_synced}")
        ubldc.print_summary(add_string=add_string)
        await asyncio.sleep(1)


with BinanceLocalDepthCacheManager(exchange=exchange,
                                   init_time_window=5,
                                   websocket_ping_interval=10,
                                   websocket_ping_timeout=20,
                                   depth_cache_update_interval=update_interval_ms) as ubldc:
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\r\nGracefully stopping ...")
    except Exception as e:
        print(f"\r\nERROR: {e}")
        print("Gracefully stopping ...")
