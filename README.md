[![GitHub release](https://img.shields.io/github/release/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache.svg)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/releases)
[![GitHub](https://img.shields.io/github/license/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache.svg?color=blue)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/blob/master/LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/unicorn-binance-local-depth-cache.svg)](https://www.python.org/downloads/)
[![Downloads](https://pepy.tech/badge/unicorn-binance-local-depth-cache)](https://pepy.tech/project/unicorn-binance-local-depth-cache)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/unicorn-binance-local-depth-cache.svg?label=PyPI%20wheel)](https://pypi.org/project/unicorn-binance-local-depth-cache/)
[![PyPI - Status](https://img.shields.io/pypi/status/unicorn-binance-local-depth-cache.svg)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/issues) 
[![Unit Tests](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/actions/workflows/unit-tests.yml)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/context:python)
[![codecov](https://codecov.io/gh/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/branch/master/graph/badge.svg?token=Z6SEARA4W4)](https://codecov.io/gh/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache)
[![Read the Docs](https://img.shields.io/badge/read-%20docs-yellow)](https://unicorn-binance-local-depth-cache.docs.lucit.tech/)
[![Github](https://img.shields.io/badge/source-github-yellow)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache)
[![Telegram](https://img.shields.io/badge/chat-telegram-yellow.svg)](https://t.me/unicorndevs)

# UNICORN Binance Local Depth Cache 

[Description](#description) | [Installation](#installation-and-upgrade) | [Documentation](#documentation) | [Examples](#examples) | [Change Log](#change-log) | [Wiki](#wiki) | [Social](#social) | [Notifications](#receive-notifications) | [Bugs](#how-to-report-bugs-or-suggest-improvements) | [Contributing](#contributing)|
[Commercial Support](#commercial-support)

A local Binance DepthCache Manager for Python that supports multiple depth caches in one instance in a easy, fast, flexible, 
robust and fully-featured way.

Part of ['UNICORN Binance Suite'](https://www.lucit.tech/unicorn-binance-suite.html).

### [Create a local depth_cache](https://unicorn-binance-local-depth-cache.docs.lucit.tech/unicorn_binance_local_depth_cache.html?highlight=create_depth_cache#unicorn_binance_local_depth_cache.manager.BinanceLocalDepthCacheManager.create_depth_cache) for Binance with just 3 lines of code:
```
import unicorn_binance_local_depth_cache

ubldc = unicorn_binance_local_depth_cache.BinanceLocalDepthCacheManager(exchange="binance.com")
ubldc.create_depth_cache("LUNABTC")
```

### Get the [asks](https://unicorn-binance-local-depth-cache.docs.lucit.tech/unicorn_binance_local_depth_cache.html?highlight=get_asks#unicorn_binance_local_depth_cache.manager.BinanceLocalDepthCacheManager.get_asks) and [bids](https://unicorn-binance-local-depth-cache.docs.lucit.tech/unicorn_binance_local_depth_cache.html?highlight=get_bids#unicorn_binance_local_depth_cache.manager.BinanceLocalDepthCacheManager.get_bids) depth with:
```
asks = ubldc.get_asks("LUNABTC")
bids = ubldc.get_bids("LUNABTC")
```

### Catch an exception, if the [depth_cache is out of sync](https://unicorn-binance-local-depth-cache.docs.lucit.tech/unicorn_binance_local_depth_cache.html?highlight=is_depth_cache_synchronized#unicorn_binance_local_depth_cache.exceptions.DepthCacheOutOfSync) while accessing its data:
```
try:
    print(f"Top 10 asks: {ubldc.get_asks(market=market)[:10]}")
    print(f"Top 10 bids: {ubldc.get_bids(market=market)[:10]}")
except DepthCacheOutOfSync as error_msg:
    print(f"ERROR: {error_msg}")
```

### [Stop and delete a depth_cache](https://unicorn-binance-local-depth-cache.docs.lucit.tech/unicorn_binance_local_depth_cache.html?highlight=stop_depth_cache#unicorn_binance_local_depth_cache.manager.BinanceLocalDepthCacheManager.stop_depth_cache):
```
ubldc.stop_depth_cache("LUNABTC")
```

### [Stop the full instance](https://unicorn-binance-local-depth-cache.docs.lucit.tech/unicorn_binance_local_depth_cache.html?highlight=stop_manager_with_all_depth_caches#unicorn_binance_local_depth_cache.manager.BinanceLocalDepthCacheManager.stop_manager_with_all_depth_caches):
```
ubldc.stop_manager_with_all_depth_caches()
```

### Get the right logger:
```
logging.getLogger("unicorn_binance_local_depth_cache")
```

[Discover more possibilities.](https://unicorn-binance-local-depth-cache.docs.lucit.tech/unicorn_binance_local_depth_cache.html)

## Description
The Python package [UNICORN Binance Local Depth Cache](https://www.lucit.tech/unicorn-binance-local-depth-cache.html) 
provides a local depth_cache for the Binance Exchanges [Binance](https://github.com/binance-exchange/binance-official-api-docs) 
([+Testnet](https://testnet.binance.vision/)), 
[Binance Futures](https://binance-docs.github.io/apidocs/futures/en/#websocket-market-streams) 
([+Testnet](https://testnet.binancefuture.com)) - more are coming soon.

The algorithm of the depth_cache management was designed according to these instructions:

- [Binance Spot: "How to manage a local order book correctly"](https://developers.binance.com/docs/binance-api/spot-detail/web-socket-streams#how-to-manage-a-local-order-book-correctly)
- [Binance Futures: "How to manage a local order book correctly"](https://binance-docs.github.io/apidocs/futures/en/#diff-book-depth-streams)

By [`create_depth_cache()`](https://unicorn-binance-local-depth-cache.docs.lucit.tech/unicorn_binance_local_depth_cache.html?highlight=create_depth_cache#unicorn_binance_local_depth_cache.manager.BinanceLocalDepthCacheManager.create_depth_caches) 
the depth_cache is started and initialized, that means for each depth_cache you want to create a separate 
thread is started. As soon as at least one depth update is received via websocket, a REST snapshot is downloaded and 
the depth updates are applied to it, keeping it in sync in real-time. Once this is done, the state of the cache is set 
to "synchronous".

Data in the depth_cache can be accessed with ['get_asks()'](https://unicorn-binance-local-depth-cache.docs.lucit.tech/unicorn_binance_local_depth_cache.html?highlight=get_asks#unicorn_binance_local_depth_cache.manager.BinanceLocalDepthCacheManager.get_asks) 
and ['get_bids()'](https://unicorn-binance-local-depth-cache.docs.lucit.tech/unicorn_binance_local_depth_cache.html?highlight=get_bids#unicorn_binance_local_depth_cache.manager.BinanceLocalDepthCacheManager.get_bids). 
If the state of the depth_cache is not synchronous during access, the exception 
['DepthCacheOutOfSync'](https://unicorn-binance-local-depth-cache.docs.lucit.tech/unicorn_binance_local_depth_cache.html?highlight=is_depth_cache_synchronized#unicorn_binance_local_depth_cache.exceptions.DepthCacheOutOfSync) 
is thrown.

The depth_cache will immediately start an automatic re-initialization if a gap in the UpdateID`s is detected (missing 
update event) or if the websocket connection is interrupted. As soon as this happens the state of the depth_cache is set 
to "out of sync" and when accessing the cache the exception ['DepthCacheOutOfSync'](https://unicorn-binance-local-depth-cache.docs.lucit.tech/unicorn_binance_local_depth_cache.html?highlight=is_depth_cache_synchronized#unicorn_binance_local_depth_cache.exceptions.DepthCacheOutOfSync) is thrown.

### Why a local depth_cache?
A local depth_cache is the fastest way to access the current order book depth at any time while transferring as little data as necessary. A REST snapshot takes a lot of time and the amount of data that is transferred is relatively large. Continuous full transmission of the order book via websocket is faster, but the amount of data is huge. A local depth_cache is initialized once with a REST snapshot and then handles Diff. Depth updates applied by the websocket connection. By transferring a small amount of data (only the changes), a local depth_cache is kept in sync in real time and also allows extremely fast (local) access to the data without exceeding the [Binance request weight limits](https://www.binance.com/en/support/faq/360004492232).

### What are the benefits of the UNICORN Binance Local Depth Cache?
- Always know if the cache is in sync! If the depth_cache is out of sync, the exception ['DepthCacheOutOfSync'](https://unicorn-binance-local-depth-cache.docs.lucit.tech/unicorn_binance_local_depth_cache.html?highlight=is_depth_cache_synchronized#unicorn_binance_local_depth_cache.exceptions.DepthCacheOutOfSync) 
is thrown or ask with [`is_depth_cache_synchronized()`](https://unicorn-binance-local-depth-cache.docs.lucit.tech/unicorn_binance_local_depth_cache.html?highlight=is_depth_cache_synchronized#unicorn_binance_local_depth_cache.manager.BinanceLocalDepthCacheManager.is_depth_cache_synchronized). 
- If a depth cache is out of sync it gets refreshed automatically within a few seconds.
- 100% Websocket auto-reconnect!
- Supported Exchanges

| Exchange | Exchange string | 
| -------- | --------------- | 
| [Binance](https://www.binance.com) | `BinanceLocalDepthCacheManager(exchange="binance.com")` |
| [Binance Testnet](https://testnet.binance.vision/) | `BinanceLocalDepthCacheManager(exchange="binance.com-testnet")` |
| [Binance USD-M Futures](https://www.binance.com) | `BinanceLocalDepthCacheManager(exchange="binance.com-futures")` |
| [Binance USD-M Futures Testnet](https://testnet.binancefuture.com) | `BinanceLocalDepthCacheManager(exchange="binance.com-futures-testnet")` |
| More are coming soon | - |

- Create multiple depth caches within a single object instance. 
- Each depth_cache is processed in a separate thread.
- Start or stop multiple caches with just one command 
[`create_depth_cache()`](https://unicorn-binance-local-depth-cache.docs.lucit.tech/unicorn_binance_local_depth_cache.html?highlight=create_depth_cache#unicorn_binance_local_depth_cache.manager.BinanceLocalDepthCacheManager.create_depth_caches)
or [`stop_depth_cache()`](https://unicorn-binance-local-depth-cache.docs.lucit.tech/unicorn_binance_local_depth_cache.html?highlight=stop_depth_cache#unicorn_binance_local_depth_cache.manager.BinanceLocalDepthCacheManager.stop_depth_cache).
- Control websocket out of sync detection with [`websocket_ping_interval`, `websocket_ping_timeout` and `websocket_close_timeout`](https://unicorn-binance-local-depth-cache.docs.lucit.tech/unicorn_binance_local_depth_cache.html#unicorn_binance_local_depth_cache.manager.BinanceLocalDepthCacheManager.create_depth_cache) 
- Powered by [UNICORN Binance REST API](https://www.lucit.tech/unicorn-binance-rest-api.html) and 
[UNICORN Binance WebSocket API](https://www.lucit.tech/unicorn-binance-websocket-api.html).

## Installation and Upgrade
The module requires Python 3.7 or above.

The current dependencies are listed 
[here](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/blob/master/requirements.txt).

If you run into errors during the installation take a look [here](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/wiki/Installation).

### A wheel of the latest release with PIP from [PyPI](https://pypi.org/project/unicorn-binance-local-depth-cache/)
`pip install unicorn-binance-local-depth-cache --upgrade`
### From source of the latest release with PIP from [Github](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache)
#### Linux, macOS, ...
Run in bash:

`pip install https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/archive/$(curl -s https://api.github.com/repos/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/releases/latest | grep -oP '"tag_name": "\K(.*)(?=")').tar.gz --upgrade`
#### Windows
Use the below command with the version (such as 0.5.0) you determined 
[here](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/releases/latest):

`pip install https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/archive/0.5.0.tar.gz --upgrade`
### From the latest source (dev-stage) with PIP from [Github](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache)
This is not a release version and can not be considered to be stable!

`pip install https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/tarball/master --upgrade`

### [Conda environment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html), [Virtualenv](https://virtualenv.pypa.io/en/latest/) or plain [Python](https://docs.python.org/2/install/)
Download the [latest release](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/releases/latest) 
or the [current master branch](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/archive/master.zip)
 and use:
 
- ./environment.yml
- ./requirements.txt
- ./setup.py

## Change Log
[https://lucit-systems-and-development.github.io/unicorn-binance-local-depth-cache/CHANGELOG.html](https://lucit-systems-and-development.github.io/unicorn-binance-local-depth-cache/CHANGELOG.html)

## Documentation
- [General](https://lucit-systems-and-development.github.io/unicorn-binance-local-depth-cache)
- [Modules](https://lucit-systems-and-development.github.io/unicorn-binance-local-depth-cache/unicorn_binance_local_depth_cache.html)

## Examples
- [example_depth_cache.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/blob/master/example_depth_cache.py)
- [example_log_to_console.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/blob/master/example_log_to_console.py)
- [example_refresh_interval.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/blob/master/example_refresh_interval.py)
- [example_shared_ubwa_instance.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/blob/master/example_shared_ubwa_instance.py)
- [example_update_interval.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/blob/master/example_update_interval.py)
- [example_version_of_this_package.py](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/blob/master/example_version_of_this_package.py)

## Project Homepage
[https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache)

## Wiki
[https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/wiki](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/wiki)

## Social
- [Discussions](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/discussions)
- [https://t.me/unicorndevs](https://t.me/unicorndevs)
- [https://dev.binance.vision](https://dev.binance.vision)
- [https://community.binance.org](https://community.binance.org)

## Receive Notifications
To receive notifications on available updates you can 
[![watch](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-local-depth-cache/master/images/misc/watch.png)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/watchers) 
the repository on [GitHub](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache), write your 
[own script](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/blob/master/example_version_of_this_package.py) 
with using 
[`is_update_available()`](https://unicorn-binance-local-depth-cache.docs.lucit.tech/unicorn_binance_local_depth_cache.html?highlight=is_update_available#unicorn_binance_local_depth_cache.manager.BinanceLocalDepthCacheManager.is_update_available).

Follow us on [Twitter](https://twitter.com/LUCIT_SysDev) or on [Facebook](https://www.facebook.com/lucit.systems.and.development) for general news about the [unicorn-binance-suite](https://www.lucit.tech/unicorn-binance-suite.html)!

To receive news (like inspection windows/maintenance) about the Binance API`s subscribe to their telegram groups: 

- [https://t.me/binance_api_announcements](https://t.me/binance_api_announcements)
- [https://t.me/binance_api_english](https://t.me/binance_api_english)
- [https://t.me/Binance_JEX_EN](https://t.me/Binance_JEX_EN)
- [https://t.me/Binance_USA](https://t.me/Binance_USA)
- [https://t.me/TRBinanceTR](https://t.me/TRBinanceTR)
- [https://t.me/BinanceDEXchange](https://t.me/BinanceDEXchange)
- [https://t.me/BinanceExchange](https://t.me/BinanceExchange)

## How to report Bugs or suggest Improvements?
[List of planned features](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement) - 
click ![thumbs-up](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-local-depth-cache/master/images/misc/thumbup.png) if you need one of them or suggest a new feature!

Before you report a bug, [try the latest release](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache#installation-and-upgrade). If the issue still exists, provide the error trace, OS 
and Python version and explain how to reproduce the error. A demo script is appreciated.

If you dont find an issue related to your topic, please open a new [issue](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/issues)!

[Report a security bug!](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/security/policy)

## Contributing
[UNICORN Binance Local Depth Cache](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache) is an open 
source project which welcomes contributions which can be anything from simple documentation fixes and reporting dead links to new features. To 
contribute follow 
[this guide](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/blob/master/CONTRIBUTING.md).
 
### Contributors
[![Contributors](https://contributors-img.web.app/image?repo=LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/graphs/contributors)

We ![love](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-local-depth-cache/master/images/misc/heart.png) open source!

## Commercial Support
[![LUCIT](https://www.lucit.tech/files/images/logos/LUCIT-LOGO.png)](https://www.lucit.tech)

***Do you need a developer, operator or consultant?***

Contact [me](https://about.me/oliver-zehentleitner) for a non-binding initial consultation via my company 
[LUCIT](https://www.lucit.tech) from Vienna (Austria) or via [Telegram](https://t.me/LUCIT_OZ).

