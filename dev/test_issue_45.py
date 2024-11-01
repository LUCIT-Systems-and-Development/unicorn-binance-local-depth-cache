from unicorn_binance_local_depth_cache import BinanceLocalDepthCacheManager, DepthCacheOutOfSync
from pprint import pprint
import time
import logging

logging.basicConfig(level=logging.DEBUG, filename='dc.log')

coin = "BTCUSDT"

ubldc = BinanceLocalDepthCacheManager(exchange="binance.com-futures", depth_cache_update_interval=100)
ubldc.create_depthcache(coin)
time.sleep(4)
while True:
    try:
        try:
            asks = ubldc.get_asks(coin)
            bids = ubldc.get_bids(coin)
        except DepthCacheOutOfSync:
            asks = "Out of sync!"
            bids = "Out of sync!"
        print(f"Bids: {len(bids)}, asks: {len(asks)}")
        #pprint(asks)
        time.sleep(1)
    except (KeyboardInterrupt) as k:
        print(k)
        ubldc.stop_manager()
        print(f"finished")
        exit()
