from unicorn_binance_local_depth_cache import BinanceLocalDepthCacheManager
import time

ubldc = BinanceLocalDepthCacheManager(exchange="binance.com-futures", depth_cache_update_interval=100)
coins = ['ethusdt', 'DYDXUSDT', "ALGOUSDT", "btcusdt"]
ubldc.create_depthcache(coins)
print(f"DCs created ...")
time.sleep(4)
ubldc.stop_depthcache("btcusdt")
print(f"DC stopped ...")
time.sleep(4)
ubldc.stop_manager()
print(f"finished")
