[![Get a UNICORN Binance Suite License](https://raw.githubusercontent.com/LUCIT-Systems-and-Development/unicorn-binance-suite/master/images/logo/LUCIT-UBS-License-Offer.png)](https://shop.lucit.services)

[![Anaconda Release](https://img.shields.io/conda/v/lucit/unicorn-binance-local-depth-cache?color=blue)](https://anaconda.org/lucit/unicorn-binance-local-depth-cache)
[![GitHub Release](https://img.shields.io/github/release/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache.svg?label=github)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/releases)
[![PyPi Release](https://img.shields.io/pypi/v/unicorn-binance-local-depth-cache?color=blue)](https://pypi.org/project/unicorn-binance-local-depth-cache/)
[![Supported Python Version](https://img.shields.io/pypi/pyversions/unicorn_binance_local_depth_cache.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-LSOSL-blue)](https://unicorn-binance-local-depth-cache.docs.lucit.tech/license.html)
[![PyPi Downloads](https://pepy.tech/badge/unicorn-binance-local-depth-cache)](https://pepy.tech/project/unicorn-binance-local-depth-cache)
[![PyPi Downloads](https://pepy.tech/badge/unicorn-binance-local-depth-cache/month)](https://pepy.tech/project/unicorn-binance-local-depth-cache)
[![PyPi Downloads](https://pepy.tech/badge/unicorn-binance-local-depth-cache/week)](https://pepy.tech/project/unicorn-binance-local-depth-cache)
[![PyPI - Status](https://img.shields.io/pypi/status/unicorn_binance_local_depth_cache.svg)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/issues)
[![codecov](https://codecov.io/gh/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/branch/master/graph/badge.svg?token=5I03AZ3F5S)](https://codecov.io/gh/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache)
[![CodeQL](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/actions/workflows/codeql.yml/badge.svg)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/actions/workflows/codeql.yml)
[![Unit Tests](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/actions/workflows/unit-tests.yml)
[![Build and Publish GH+PyPi](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/actions/workflows/build_wheels.yml/badge.svg)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/actions/workflows/build_wheels.yml)
[![Build and Publish Anaconda](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/actions/workflows/build_conda.yml/badge.svg)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/actions/workflows/build_conda.yml)
[![Read the Docs](https://img.shields.io/badge/read-%20docs-yellow)](https://unicorn-binance-local-depth-cache.docs.lucit.tech/)
[![Read How To`s](https://img.shields.io/badge/read-%20howto-yellow)](https://medium.lucit.tech)
[![Github](https://img.shields.io/badge/source-github-cbc2c8)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache)
[![Telegram](https://img.shields.io/badge/community-telegram-41ab8c)](https://t.me/unicorndevs)
[![Gitter](https://img.shields.io/badge/community-gitter-41ab8c)](https://gitter.im/unicorn-binance-suite/unicorn-binance-local-depth-cache?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Get Free Professional Support](https://img.shields.io/badge/chat-lucit%20support-004166)](https://www.lucit.tech/get-support.html)

[![LUCIT-UBLDC-Banner](https://raw.githubusercontent.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/master/images/logo/LUCIT-UBLDC-Banner-Readme.png)](https://www.lucit.tech/unicorn-binance-local-depth-cache.html)

# UNICORN Binance Local Depth Cache 

[Description](#description) | [Installation](#installation-and-upgrade) | [How To](#howto) | [Documentation](#documentation) | 
[Examples](#examples) | [Change Log](#change-log) | [Wiki](#wiki) | [Social](#social) | 
[Notifications](#receive-notifications) | [Bugs](#how-to-report-bugs-or-suggest-improvements) | 
[Contributing](#contributing) |[Disclaimer](#disclaimer) | 
[Commercial Support](#commercial-support)

A Python SDK by [LUCIT](https://www.lucit.tech) for accessing and managing multiple local Binance 
[order books](https://academy.binance.com/en/glossary/order-book) with Python in a simple, fast, flexible, robust 
and fully functional way. 

The organization of the DepthCache takes place in the same asyncio loop as the reception of the websocket data. The 
full stack of the UBS modules (REST, WebSocket and DepthCache) can be downloaded and installed by PyPi and Anaconda 
as a Python C extension for maximum performance.

Part of '[UNICORN Binance Suite](https://www.lucit.tech/unicorn-binance-suite.html)'.

[Get help](https://www.lucit.tech/get-support.html) with the integration of the `UNICORN Binance Suite` modules!

## Get a UNICORN Binance Suite License

To run modules of the *UNICORN Binance Suite* you need a [valid license](https://medium.lucit.tech/how-to-obtain-and-use-a-unicorn-binance-suite-license-key-and-run-the-ubs-module-according-to-best-87b0088124a8#4ca4)!

## Using a DepthCache

### [Create a local depth_cache](https://unicorn-binance-local-depth-cache.docs.lucit.tech/unicorn_binance_local_depth_cache.html?highlight=create_depth_cache#unicorn_binance_local_depth_cache.manager.BinanceLocalDepthCacheManager.create_depth_cache) for Binance with just 3 lines of code
```
from unicorn_binance_local_depth_cache import BinanceLocalDepthCacheManager, DepthCacheOutOfSync

ubldc = BinanceLocalDepthCacheManager(exchange="binance.com"
                                      depth_cache_update_interval=100)
ubldc.create_depth_cache("BTCUSDT")
```

### Get the [asks](https://unicorn-binance-local-depth-cache.docs.lucit.tech/unicorn_binance_local_depth_cache.html?highlight=get_asks#unicorn_binance_local_depth_cache.manager.BinanceLocalDepthCacheManager.get_asks) and [bids](https://unicorn-binance-local-depth-cache.docs.lucit.tech/unicorn_binance_local_depth_cache.html?highlight=get_bids#unicorn_binance_local_depth_cache.manager.BinanceLocalDepthCacheManager.get_bids)
#### To obtain the complete order book
```
asks = ubldc.get_asks("BTCUSDT")
bids = ubldc.get_bids("BTCUSDT")
```

#### Get the first X elements
```
asks = ubldc.get_asks("BTCUSDT", limit_count=10)
bids = ubldc.get_bids("BTCUSDT", limit_count=10)
```

#### Retain the elements until volume X has been exceeded
```
asks = ubldc.get_asks("BTCUSDT", threshold_volume=300000)
bids = ubldc.get_bids("BTCUSDT", threshold_volume=300000)
```

### Catch an exception, if the [depth_cache is out of sync](https://unicorn-binance-local-depth-cache.docs.lucit.tech/unicorn_binance_local_depth_cache.html?highlight=is_depth_cache_synchronized#unicorn_binance_local_depth_cache.exceptions.DepthCacheOutOfSync) while accessing its data
```
try:
    asks = ubldc.get_asks(market="BTCUSDT", limit_count=5, threshold_volume=300000)
    bids = ubldc.get_bids(market="BTCUSDT", limit_count=5, threshold_volume=300000)
except DepthCacheOutOfSync:
    asks = "Out of sync!"
    bids = "Out of sync!"
```

### [Stop and delete a depth_cache](https://unicorn-binance-local-depth-cache.docs.lucit.tech/unicorn_binance_local_depth_cache.html?highlight=stop_depth_cache#unicorn_binance_local_depth_cache.manager.BinanceLocalDepthCacheManager.stop_depth_cache):
```
ubldc.stop_depth_cache("BTCUSDT")
```

## Stop `ubldc` after usage to avoid memory leaks

When you instantiate UBLDC with `with`, `ubldc.stop_manager()` is automatically executed upon exiting the `with`-block.

```
with BinanceWebSocketApiManager() as ubldc:
    ubldc.create_depth_cache("BTCUSDT")
```

Without `with`, you must explicitly execute `ubldc.stop_manager()` yourself.

```
ubldc.stop_manager()
```

[Discover more possibilities.](https://unicorn-binance-local-depth-cache.docs.lucit.tech/unicorn_binance_local_depth_cache.html)

## Description
The Python package [UNICORN Binance Local Depth Cache](https://www.lucit.tech/unicorn-binance-local-depth-cache.html) 
provides local order books for the Binance Exchanges 
[Binance](https://github.com/binance-exchange/binance-official-api-docs) ([+Testnet](https://testnet.binance.vision/)), 
[Binance Futures](https://binance-docs.github.io/apidocs/futures/en/#websocket-market-streams) 
([+Testnet](https://testnet.binancefuture.com)) and [Binance US](https://www.binance.us/).

The algorithm of the depth_cache management was designed according to these instructions:

- [Binance Spot: "How to manage a local order book correctly"](https://binance-docs.github.io/apidocs/spot/en/#how-to-manage-a-local-order-book-correctly)
- [Binance Futures: "How to manage a local order book correctly"](https://binance-docs.github.io/apidocs/futures/en/#diff-book-depth-streams)
- [Binance US: "Managing a Local Order Book"](https://docs.binance.us/#order-book-depth-diff-stream)

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

| Exchange                                                           | Exchange string               | 
|--------------------------------------------------------------------|-------------------------------| 
| [Binance](https://www.binance.com)                                 | `binance.com`                 |
| [Binance Testnet](https://testnet.binance.vision/)                 | `binance.com-testnet`         |
| [Binance USD-M Futures](https://www.binance.com)                   | `binance.com-futures`         |
| [Binance USD-M Futures Testnet](https://testnet.binancefuture.com) | `binance.com-futures-testnet` |
| [Binance US](https://www.binance.us/)                              | `binance.us`                  |

- Create multiple depth caches within a single object instance. 

- Each depth_cache is processed in a separate thread.

- Start or stop multiple caches with just one command 
[`create_depth_cache()`](https://unicorn-binance-local-depth-cache.docs.lucit.tech/unicorn_binance_local_depth_cache.html?highlight=create_depth_cache#unicorn_binance_local_depth_cache.manager.BinanceLocalDepthCacheManager.create_depth_caches)
or [`stop_depth_cache()`](https://unicorn-binance-local-depth-cache.docs.lucit.tech/unicorn_binance_local_depth_cache.html?highlight=stop_depth_cache#unicorn_binance_local_depth_cache.manager.BinanceLocalDepthCacheManager.stop_depth_cache).

- Control websocket out of sync detection with [`websocket_ping_interval`, `websocket_ping_timeout` and `websocket_close_timeout`](https://unicorn-binance-local-depth-cache.docs.lucit.tech/unicorn_binance_local_depth_cache.html#unicorn_binance_local_depth_cache.manager.BinanceLocalDepthCacheManager.create_depth_cache) 

- Powered by [UNICORN Binance REST API](https://www.lucit.tech/unicorn-binance-rest-api.html) and 
[UNICORN Binance WebSocket API](https://www.lucit.tech/unicorn-binance-websocket-api.html).

- Available as a package via `pip` and `conda` as precompiled C extension with stub files for improved Intellisense 
  functions and source code for easier debugging of the source code. [To the installation.](#installation-and-upgrade)

If you like the project, please 
[![star](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-local-depth-cache/master/images/misc/star.png)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/stargazers) it on 
[GitHub](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache)! 

## Live Demo
This live demo script runs DepthCaches from [binance.com-futues](https://www.binance.com) and runs on a *CCX13 * virtual 
machine of [HETZNER CLOUD](https://hetzner.cloud/?ref=rKgYRMq0l8fd)

[Open live monitor!](https://www.lucit.tech/unicorn-binance-local-depth-cache-live-demo.html)

[![live-demo](https://ubldc-demo.lucit.tech/ps.png)](https://www.lucit.tech/unicorn-binance-local-depth-cache-live-demo.html)

(Refresh update once a minute!)

## Installation and Upgrade
The module requires Python 3.7 and runs smoothly up to and including Python 3.12.

For the PyPy interpreter we offer packages only from Python version 3.9 and higher.

Anaconda packages are available from Python version 3.8 and higher, but only in the latest version!

The current dependencies are listed [here](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/blob/master/requirements.txt).

If you run into errors during the installation take a look [here](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-suite/wiki/Installation).

### Packages are created automatically with GitHub Actions
When a new release is to be created, we start two GitHubActions: 

- [Build and Publish Anaconda](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/actions/workflows/build_conda.yml)
- [Build and Publish GH+PyPi](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/actions/workflows/build_wheels.yml) 

Both start virtual Windows/Linux/Mac servers provided by GitHub in the cloud with preconfigured environments and 
create the respective compilations and stub files, pack them into wheels and conda packages and then publish them on 
GitHub, PYPI and Anaconda. This is a transparent method that makes it possible to trace the source code behind a 
compilation.

### A Cython binary, PyPy or source code based CPython wheel of the latest version with `pip` from [PyPI](https://pypi.org/project/unicorn-binance-rest-api/)
Our [Cython](https://cython.org/) and [PyPy](https://www.pypy.org/) Wheels are available on [PyPI](https://pypi.org/), 
these wheels offer significant advantages for Python developers:

- ***Performance Boost with Cython Wheels:*** Cython is a programming language that supplements Python with static typing and C-level performance. By compiling 
  Python code into C, Cython Wheels can significantly enhance the execution speed of Python code, especially in 
  computationally intensive tasks. This means faster runtimes and more efficient processing for users of our package. 

- ***PyPy Wheels for Enhanced Efficiency:*** PyPy is an alternative Python interpreter known for its speed and efficiency. It uses Just-In-Time (JIT) compilation, 
  which can dramatically improve the performance of Python code. Our PyPy Wheels are tailored for compatibility with 
  PyPy, allowing users to leverage this speed advantage seamlessly.

Both Cython and PyPy Wheels on PyPI make the installation process simpler and more straightforward. They ensure that 
you get the optimized version of our package with minimal setup, allowing you to focus on development rather than 
configuration.

#### Installation
`pip install unicorn-binance-local-depth-cache`

#### Update
`pip install unicorn-binance-local-depth-cache --upgrade`

### A Conda Package of the latest version with `conda` from [Anaconda](https://anaconda.org/lucit)
The `unicorn-binance-local-depth-cache` package is also available as a Cython version for the `linux-64`, `osx-64` 
and `win-64` architectures with [Conda](https://docs.conda.io/en/latest/) through the 
[`lucit` channel](https://anaconda.org/lucit). 

For optimal compatibility and performance, it is recommended to source the necessary dependencies from the 
[`conda-forge` channel](https://anaconda.org/conda-forge). 

#### Installation
```
conda config --add channels conda-forge
conda config --add channels lucit
conda install -c lucit unicorn-binance-local-depth-cache
```

#### Update
`conda update -c lucit unicorn-binance-local-depth-cache`

### From source of the latest release with PIP from [GitHub](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache)
#### Linux, macOS, ...
Run in bash:

`pip install https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/archive/$(curl -s https://api.github.com/repos/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/releases/latest | grep -oP '"tag_name": "\K(.*)(?=")').tar.gz --upgrade`

#### Windows
Use the below command with the version (such as 2.0.0) you determined 
[here](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/releases/latest):

`pip install https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/archive/2.0.0.tar.gz --upgrade`

### From the latest source (dev-stage) with PIP from [GitHub](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache)
This is not a release version and can not be considered to be stable!

`pip install https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/tarball/master --upgrade`

## Change Log
[https://lucit-systems-and-development.github.io/unicorn-binance-local-depth-cache/changelog.html](https://lucit-systems-and-development.github.io/unicorn-binance-local-depth-cache/changelog.html)

## Documentation
- [General](https://lucit-systems-and-development.github.io/unicorn-binance-local-depth-cache)
- [Modules](https://lucit-systems-and-development.github.io/unicorn-binance-local-depth-cache/modules.html)

## Examples
- [Look here!](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/tree/master/examples/)

## Howto
- [How to Obtain and Use a Unicorn Binance Suite License Key and Run the UBS Module According to Best Practice](https://medium.lucit.tech/how-to-obtain-and-use-a-unicorn-binance-suite-license-key-and-run-the-ubs-module-according-to-best-87b0088124a8)

## Project Homepage
[https://www.lucit.tech/unicorn-binance-local-depth-cache.html](https://www.lucit.tech/unicorn-binance-local-depth-cache.html)

## Wiki
[https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/wiki](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/wiki)

## Social
- [Discussions](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/discussions)
- [Gitter](https://gitter.im/unicorn-binance-suite/unicorn-binance-local-depth-cache)
- [https://t.me/unicorndevs](https://t.me/unicorndevs)
- [https://dev.binance.vision](https://dev.binance.vision)
- [https://community.binance.org](https://community.binance.org)

## Receive Notifications
To receive notifications on available updates you can 
[![watch](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-local-depth-cache/master/images/misc/watch.png)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/watchers) 
the repository on [GitHub](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache), write your 
[own script](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/blob/master/examples/ubldc_package_update_check) 
with using 
[`is_update_available()`](https://unicorn-binance-local-depth-cache.docs.lucit.tech/unicorn_binance_local_depth_cache.html?highlight=is_update_available#unicorn_binance_local_depth_cache.manager.BinanceLocalDepthCacheManager.is_update_available).

Follow us on [LinkedIn](https://www.linkedin.com/company/lucit-systems-and-development), 
[X](https://twitter.com/LUCIT_SysDev) or [Facebook](https://www.facebook.com/lucit.systems.and.development)!

To receive news (like inspection windows/maintenance) about the Binance API`s subscribe to their telegram groups: 

- [https://t.me/binance_api_announcements](https://t.me/binance_api_announcements)
- [https://t.me/binance_api_english](https://t.me/binance_api_english)
- [https://t.me/Binance_JEX_EN](https://t.me/Binance_JEX_EN)
- [https://t.me/Binance_USA](https://t.me/Binance_USA)
- [https://t.me/TRBinanceTR](https://t.me/TRBinanceTR)
- [https://t.me/BinanceExchange](https://t.me/BinanceExchange)

## How to report Bugs or suggest Improvements?
[List of planned features](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement) - click ![thumbs-up](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-local-depth-cache/master/images/misc/thumbup.png) if you need one of them or suggest a new feature!

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

## Disclaimer
This project is for informational purposes only. You should not construe this information or any other material as 
legal, tax, investment, financial or other advice. Nothing contained herein constitutes a solicitation, recommendation, 
endorsement or offer by us or any third party provider to buy or sell any securities or other financial instruments in 
this or any other jurisdiction in which such solicitation or offer would be unlawful under the securities laws of such 
jurisdiction.

### If you intend to use real money, use it at your own risk!

Under no circumstances will we be responsible or liable for any claims, damages, losses, expenses, costs or liabilities 
of any kind, including but not limited to direct or indirect damages for loss of profits.

## Commercial Support

[![Get professional and fast support](https://raw.githubusercontent.com/LUCIT-Systems-and-Development/unicorn-binance-suite/master/images/support/LUCIT-get-professional-and-fast-support.png)](https://www.lucit.tech/get-support.html)

***Do you need a developer, operator or consultant?*** [Contact us](https://www.lucit.tech/contact.html) for a non-binding initial consultation!
