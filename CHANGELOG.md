# unicorn-binance-local-depth-cache Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/) and this project adheres to 
[Semantic Versioning](http://semver.org/).

[Discussions about unicorn-binance-local-depth-cache releases!](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/discussions/categories/releases)

[How to upgrade to the latest version!](https://unicorn-binance-local-depth-cache.docs.lucit.tech/readme.html#installation-and-upgrade)

## 2.0.0.dev (development stage/unreleased/unstable)

## 2.0.0
Scaling. The core functions have been rewritten in this update. Instead of one stream per depth_cache, we now use one 
stream up to the max subscription limit of the endpoint and use the new UBWA `asyncio_queue` interface.
`get_stream_data_from_asyncio_queue()`. And we avoid bans by complying with Binance weight costs on init.
### Added
- Support for "binance.us"
- Since UBLDC is delivered as a compiled C extension, IDEs such as Pycharm and Visual Code cannot use information about 
  available methods, parameters and their types for autocomplete and other intellisense functions. As a solution, from 
  now on stub files (PYI) will be created in the build process and attached to the packages. The IDEs can automatically 
  obtain the required information from these.
- `ubldc.get_ubwa_manager()` returns the UBWA instance of UBLDC
- `ubldc.get_ubra_manager()` returns the UBRA instance of UBLDC
- New exceptions: `DepthCacheAlreadyStopped` and `DepthCacheNotFound`
### Changed
- The parameter `ubwa_manager` was removed from `BinanceLocalDepthCacheManager()`, because UBLDC has to claim the 
  callback function of the `stream_signals` for itself and has to initialize the instance itself. It is possible to 
  request the active `BinanceWebSocketApiManager()` instance with the new method `ubldc.get_ubwa_manager()`. 
  `ubwa.create_stream()` can be used normally, only the `stream_signals` are only accessible for UBLDC.
- Updated description text in all files.
### Fixed
- Ip ban when using `create_depth_cache` with many symbols [issue#30](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/issues/30)
- Import in `licensing_manager.py`.
- Type of global `logger` variable.
### Security
Set higher minimum version `2.4.0` for `unicorn-binance-rest-api` are affected by vulnerabilities in used dependencies!

- Dependency `certifi`:
  - CVE-2023-37920, Score: 9.8 (High)
    - Certifi is a curated collection of Root Certificates for validating the trustworthiness of SSL certificates while 
      verifying the identity of TLS hosts. Certifi 1.0.1 through 2023.5.7 recognizes "e-Tugra" root certificates. 
      e-Tugra's root certificates were subject to an investigation prompted by reporting of security issues in their 
      systems. Certifi 2023.07.22 removes root certificates from "e-Tugra" from the root store.
    - https://devhub.checkmarx.com/cve-details/CVE-2023-37920/
- Dependency `cryptography`:
  - CVE-2023-38325, Score: 7.5 (High)
    - The cryptography package versions prior to 41.0.2 for Python mishandles SSH certificates that have critical 
      options.
    - https://devhub.checkmarx.com/cve-details/CVE-2023-38325/
  - CVE-2023-49083, Score: 7.5 (High)
    - Cryptography is a package designed to expose cryptographic primitives and recipes to Python developers. Calling 
      `load_pem_pkcs7_certificates` or `load_der_pkcs7_certificates` could lead to a NULL-pointer dereference and 
      segfault. Exploitation of this vulnerability poses a serious risk of Denial of Service (DoS) for any application 
      attempting to deserialize a PKCS7 blob/certificate. The consequences extend to potential disruptions in system 
      availability and stability. This issue affects versions 3.1 through 41.0.5.
    - https://devhub.checkmarx.com/cve-details/CVE-2023-49083/
  - CVE-2023-50782, Score: 7.5 (High)
    - A flaw was found in the python cryptography package versions prior to 42.0.0. This issue may allow a remote 
      attacker to decrypt captured messages in TLS servers that use RSA key exchanges, which may lead to exposure of 
      confidential or sensitive data. This issue is an incomplete fix of CVE-2020-25659.
    - https://devhub.checkmarx.com/cve-details/CVE-2023-50782/
  - CVE-2024-26130, Score: 7.5 (High)
    - cryptography is a package designed to expose cryptographic primitives and recipes to Python developers. Starting 
      in version 38.0.0 and prior to version 42.0.4, if `pkcs12.serialize_key_and_certificates` is called with both a 
      certificate whose public key did not match the provided private key and an `encryption_algorithm` with `hmac_hash` 
      set (via `PrivateFormat.PKCS12.encryption_builder().hmac_hash(...)`, then a NULL pointer dereference would occur, 
      crashing the Python process. This has been resolved in version 42.0.4, the first version in which a `ValueError` 
      is properly raised.
    - https://devhub.checkmarx.com/cve-details/CVE-2024-26130/
- Dependency  `requests`:
  - CVE-2023-32681, Score: 6.1 (Medium)
    - Requests is a HTTP library. Requests has been leaking Proxy-Authorization headers to destination servers when 
      redirected to an HTTPS endpoint. This is a product of how we use `rebuild_proxies` to reattach the 
      `Proxy-Authorization` header to requests. For HTTP connections sent through the tunnel, the proxy will identify 
      the header in the request itself and remove it prior to forwarding to the destination server. However when sent 
      over HTTPS, the `Proxy-Authorization` header must be sent in the CONNECT request as the proxy has no visibility 
      into the tunneled request. This results in Requests forwarding proxy credentials to the destination server 
      unintentionally, allowing a malicious actor to potentially exfiltrate sensitive information. This issue affects 
      versions 2.3.0 through 2.30.0.
    - https://devhub.checkmarx.com/cve-details/CVE-2023-32681/

## 1.0.0
### Added
- Support for Python 3.11 and 3.12
- Integration of the `lucit-licensing-python` library for verifying the UNICORN Binance Suite license. A license can be 
  purchased in the LUCIT Online Shop: https://shop.lucit.services/software/unicorn-binance-suite
- License change from MIT to LSOSL - LUCIT Synergetic Open Source License:
  https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/blob/master/LICENSE
- Conversion to a C++ compiled Cython package with precompiled as well as PyPy and source code wheels.
- Setup of a "Trusted Publisher" deployment chain. The source code is transparently packaged into wheels directly from
  the GitHub repository by a GitHub action for all possible platforms and published directly as a new release on GitHub
  and PyPi. A second process from Conda-Forge then uploads it to Anaconda. Thus, the entire deployment process is
  transparent and the user can be sure that the compilation of a version fully corresponds to the source code.
- `manager.stop_manager()` alias for `manager.stop_manager_with_all_caches()` 
- Support for `with`-context.

## 0.7.3
### Fixed 
- TypeError exception in `_init_depth_cache` [issue#27](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/issues/27

## 0.7.2
Codebase equal to 0.7.0, testing azure pipe

## 0.7.1
Codebase equal to 0.7.0, just preparing conda-forge packaging

## 0.7.0
### Added 
- Active `high_performance` of UBWA.
- Exception handling for REST calls
- Improved logging
### Changed
- Websocket reconnect intervals
- Reduced calls of `market.lower()`
### Removed
- Obsolete variable `self.timeout`

## 0.6.0
### Added
- `default_websocket_close_timeout`, `default_websocket_ping_interval`, `default_websocket_ping_timeout` and 
`websocket_close_timeout`, `websocket_close_timeout`, `websocket_ping_interval`
### Changed
- `default_websocket_close_timeout`, `default_websocket_ping_interval`, `default_websocket_ping_timeout` default values is 1,
so websockets disconnect very fast, and we recognize "out of sync" very fast.

## 0.5.3
### Changed
- Balanced log levels 
### Fixed
- KeyError in `stop_depth_cache()`

## 0.5.2
### Changed
- close_timeout=5 in `create_stream()`
### Fixed
- `_init_depth_cache()` returns False if `order_book` is False

## 0.5.1
### Fixed
- Wrong proof of `is_stop_request()`

## 0.5.0
### Added
- `_reset_depth_cache()`
- `_get_order_book_from_depth_cache()`
- `is_stop_request()`
### Changed
- Clear stream_buffer on disconnect 
- Better error handling in `_init_depth_cache()`
### Fixed
- `stop_depth_cache()` did not stop its dependent stream and did not clear the stream_buffer
- A few error handling's

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
