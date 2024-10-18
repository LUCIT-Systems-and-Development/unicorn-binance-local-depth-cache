#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯

from unicorn_binance_local_depth_cache import BinanceLocalDepthCacheManager, DepthCacheOutOfSync
from typing import Optional
import asyncio
import logging
import os

amount_test_caches: int = 40
exchange: str = "binance.com"
update_interval_ms: Optional[int] = None
threshold_volume: float = 200000.0

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
        add_string = (f"binance_api_status={ubra.get_used_weight(cached=True)}\r\n "
                      f"---------------------------------------------------------------------------------------------")
        for market in markets:
            try:
                top_asks = ubldc.get_asks(market=market, threshold_volume=threshold_volume)
                top_bids = ubldc.get_bids(market=market, threshold_volume=threshold_volume)
            except DepthCacheOutOfSync:
                top_asks = "Out of sync!"
                top_bids = "Out of sync!"
            depth = (f"depth_cache '{market}' is in sync: {ubldc.is_depth_cache_synchronized(market=market)}\r\n " 
                     f" - top asks volume > {threshold_volume}: {top_asks}\r\n "
                     f" - top bids volume > {threshold_volume}: {top_bids}")
            add_string = f"{add_string}\r\n {depth}"

        ubldc.print_summary(add_string=add_string)
        await asyncio.sleep(1)


with BinanceLocalDepthCacheManager(exchange=exchange,
                                   init_time_window=5,
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
