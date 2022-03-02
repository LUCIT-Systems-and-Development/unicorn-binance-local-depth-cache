[![GitHub release](https://img.shields.io/github/release/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache.svg)](https://pypi.org/project/unicorn-binance-local-depth-cache/)
[![GitHub](https://img.shields.io/github/license/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache.svg?color=blue)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/blob/master/LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/unicorn-binance-local-depth-cache.svg)](https://www.python.org/downloads/)
[![Downloads](https://pepy.tech/badge/unicorn-binance-local-depth-cache)](https://pepy.tech/project/unicorn-binance-local-depth-cache)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/unicorn-binance-local-depth-cache.svg?label=PyPI%20wheel)](https://pypi.org/project/unicorn-binance-local-depth-cache/)
[![PyPI - Status](https://img.shields.io/pypi/status/unicorn-binance-local-depth-cache.svg)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/issues) 
[![Python application](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/actions/workflows/python-app.yml/badge.svg)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/actions/workflows/python-app.yml)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/context:python)
[![codecov](https://codecov.io/gh/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/branch/master/graph/badge.svg?token=Z6SEARA4W4)](https://codecov.io/gh/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache)
[![Read the Docs](https://img.shields.io/badge/read-%20docs-yellow)](https://unicorn-binance-local-depth-cache.docs.lucit.tech/)
[![Github](https://img.shields.io/badge/source-github-yellow)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache)
[![Telegram](https://img.shields.io/badge/chat-telegram-yellow.svg)](https://t.me/unicorndevs)

# UNICORN Binance Local Depth Cache 

[Description](#description) | [Installation](#installation-and-upgrade) | [How To](#howto) |
[Documentation](#documentation) | [Examples](#examples) | [Change Log](#change-log) | [Wiki](#wiki) | [Social](#social) |
[Notifications](#receive-notifications) | [Bugs](#how-to-report-bugs-or-suggest-improvements) | 
[Contributing](#contributing) | [Commercial Support](#commercial-support)

*** ALPHA ***

A local DepthCache written in Python for the Binance order books (com+testnet, com-margin+testnet, 
com-isolated_margin+testnet, com-futures+testnet, com-coin_futures, us, tr, jex, dex/chain+testnet).

Part of ['UNICORN Binance Suite'](https://www.lucit.tech/unicorn-binance-suite.html).

```
import unicorn_binance_local_depth_cache

--example-code--
```

## Description

--long-description--

### What are the benefits of the UNICORN Binance Local Depth Cache?
- 

## Installation and Upgrade
The module requires Python 3.7 or above, as it depends on Pythons latest asyncio features for asynchronous/concurrent 
processing. 

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
Use the below command with the version (such as 1.35.0) you determined 
[here](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/releases/latest):

`pip install https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/archive/1.35.0.tar.gz --upgrade`
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
[`is_update_availabe()`](https://lucit-systems-and-development.github.io/unicorn-binance-local-depth-cache/unicorn_binance_local_depth_cache.html#unicorn_binance_local_depth_cache.unicorn_binance_local_depth_cache_manager.BinanceTrailingStopLossEngineManager.is_update_availabe).

Follow us on [Twitter](https://twitter.com/LUCIT_SysDev) or on [Facebook](https://www.facebook.com/lucit.systems.and.development) for general news about the [unicorn-binance-suite](https://www.lucit.tech/unicorn-binance-suite.html)!

To receive news (like inspection windows/maintenance) about the Binance API`s subscribe to their telegram groups: 
- [https://t.me/binance_api_announcements](https://t.me/binance_api_announcements)
- [https://t.me/binance_api_english](https://t.me/binance_api_english)
- [https://t.me/BinanceExchange](https://t.me/BinanceExchange)
- [https://t.me/Binance_USA](https://t.me/Binance_USA)
- [https://t.me/Binance_JEX_EN](https://t.me/Binance_JEX_EN)
- [https://t.me/BinanceDEXchange](https://t.me/BinanceDEXchange)

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
[![Contributors](https://contributors-img.web.app/image?repo=oliver-zehentleitner/unicorn-binance-local-depth-cache)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/graphs/contributors)

We ![love](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-local-depth-cache/master/images/misc/heart.png) open source!

## Commercial Support
[![LUCIT](https://www.lucit.tech/files/images/logos/LUCIT-LOGO.png)](https://www.lucit.tech)

***Do you need a developer, operator or consultant?***

Contact [me](https://about.me/oliver-zehentleitner) for a non-binding initial consultation via my company 
[LUCIT](https://www.lucit.tech) from Vienna (Austria) or via [Telegram](https://t.me/LUCIT_OZ).

