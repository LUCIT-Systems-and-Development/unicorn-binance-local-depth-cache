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

exchange: str = "binance.com-futures"
update_interval_ms: Optional[int] = None
limit_count: int = 4

logging.getLogger("unicorn_binance_local_depth_cache")
logging.basicConfig(level=logging.DEBUG,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")


async def main():
    exclude_markets: list = ['BCCUSDT', 'VENUSDT', 'TRXUSDT', 'NULSUSDT', 'TUSDUSDT', 'PAXUSDT', 'BCHABCUSDT',
                             'BCHSVUSDT', 'BTTUSDT', 'USDSUSDT', 'USDCUSDT', 'TFUELUSDT', 'MITHUSDT', 'NANOUSDT',
                             'DASHUSDT', 'NEOUSDT', 'ICXUSDT']
    all_markets: list = [item['symbol'] for item in ubra.get_all_tickers() if item['symbol'].endswith("USDT")]
    markets: list = []

    for market in all_markets[:2]:
        if market not in exclude_markets:
            markets.append(market)

    print(f"Starting DepthCaches for markets: {markets}")
    ubldc.create_depth_cache(markets=markets)

    while ubldc.is_stop_request() is False:
        add_string = (f"binance_api_status={ubra.get_used_weight(cached=True)}\r\n "
                      f"---------------------------------------------------------------------------------------------")
        for market in markets:
            try:
                top_asks = ubldc.get_asks(market=market, limit_count=limit_count)
                top_bids = ubldc.get_bids(market=market, limit_count=limit_count)
            except DepthCacheOutOfSync:
                top_asks = "Out of sync!"
                top_bids = "Out of sync!"
            depth = (f"depth_cache '{market}' is in sync: {ubldc.is_depth_cache_synchronized(market=market)}\r\n " 
                     f" - top {limit_count} asks: {top_asks}\r\n "
                     f" - top {limit_count} bids: {top_bids}")
            add_string = f"{add_string}\r\n {depth}"

        ubldc.print_summary(add_string=add_string)
        time.sleep(0.2)


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