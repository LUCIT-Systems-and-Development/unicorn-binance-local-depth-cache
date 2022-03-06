# unicorn-binance-local-depth-cache Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/) and this project adheres to 
[Semantic Versioning](http://semver.org/).

[Discussions about unicorn-binance-websocket-api releases!](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/discussions/categories/releases)

## 0.4.1.dev (development stage/unreleased/unstable)
### Added
- `_reset_depth_cache()`
### Changed
- Clear stream_buffer on disconnect 
- Better error handling in `_init_depth_cache()`

## 0.4.1
### Added
- Resetting asks and bits on stream_signal DISCONNECT
### Fixing
- `requests.exceptions.ConnectionError` exception while fetching the order_book

## 0.4.0
### Added
- `default_update_interval`
### Changes
- a few small :)

## 0.3.0
### Added
- threading.Lock(): `self.threading_lock_ask` and `self.threading_lock_bid`

### Added
- `set_refresh_request()`

## 0.2.0
### Added
- Binance Futures support (exchange="binance.com-futures")
### Changed
- `create_depth_cache()` renamed parameter `market` to `markets`. `markets` can be a str or a list of one or more market symbols
- `stop_depth_cache()` renamed parameter `market` to `markets`. `markets` can be a str or a list of one or more market symbols
-  Renamed `stop_manager()` to `stop_manager_with_all_caches()`
### Removed
- `create_depth_caches()` 
- `stop_depth_caches()` 

## 0.1.0
Initial Release!
