from unicorn_binance_local_depth_cache import BinanceLocalDepthCacheManager, DepthCacheOutOfSync
import time


coins = ['ethusdt', 'DYDXUSDT', "ALGOUSDT", "btcusdt"]
test_coin = "btcusdt"

with BinanceLocalDepthCacheManager(exchange="binance.com-futures",
                                   init_interval=0.5,
                                   init_time_window=1,
                                   depth_cache_update_interval=100) as ubldc:
    ubldc.create_depthcache(coins)
    print(f"DCs created: {coins}")
    time.sleep(1)
    ubldc.stop_depthcache(test_coin)
    print(f"DC {test_coin} stopped ...")
    time.sleep(1)
    print(f"list_of_depthcaches: {ubldc.get_list_of_depthcaches()}")
    print(f"Restart {test_coin}:")
    ubldc.create_depthcache(test_coin)
    time.sleep(1)
    sigterm = False
    print(f"Looking for asks:")
    while sigterm is False:
        try:
            time.sleep(0.1)
            print(f"ASKS '{test_coin}': {ubldc.get_asks(test_coin, limit_count=3)}")
        except DepthCacheOutOfSync:
            print("Please wait till the DC gets synced!")
        except KeyboardInterrupt:
            sigterm = True
print(f"finished")
