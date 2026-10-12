# unicorn-binance-local-depth-cache Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/) and this project adheres to 
[Semantic Versioning](http://semver.org/).

[Discussions about unicorn-binance-local-depth-cache releases!](https://github.com/oliver-zehentleitner/unicorn-binance-local-depth-cache/discussions/categories/releases)

[How to upgrade to the latest version!](https://oliver-zehentleitner.github.io/unicorn-binance-local-depth-cache/readme.html#installation-and-upgrade)

## 2.14.0.dev (development stage/unreleased/unstable)

## 2.14.1
### Fixed
- `Cluster.create_depthcache()` and `create_depthcache_async()` sent a
  `POST` to UBDCC's `/create_depthcache`, which only accepts `GET`, so
  every call came back as `405 Method Not Allowed`. Both now use `GET`.
- `websocket_ping_interval` and `websocket_ping_timeout` were passed
  swapped to UBWA (`ping_interval_default` got the timeout and vice
  versa), so with the defaults the effective ping interval was 20s
  instead of 10s and the timeout 10s instead of 20s.

### Changed
- Bumped minimum `unicorn-binance-websocket-api` dependency from
  `>=2.12.2` to `>=2.13.0` in `setup.py`, `requirements.txt`,
  `pyproject.toml`, `environment.yml` and `meta.yaml`. UBWA 2.13.0
  introduces the per-category Futures WebSocket routing
  (`/public`, `/market`, `/private`) required by Binance since
  2026-04-23 and raises `ValueError` on mixed-category streams.
  See
  [unicorn-binance-websocket-api#437](https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/issues/437).

## 2.14.0
### Changed
- **Breaking**: renamed the cluster client's credential methods to drop the
  redundant `ubdcc_` prefix and align with the rest of the API:
  `ubdcc_add_credentials()` → `add_credentials()`,
  `ubdcc_remove_credentials()` → `remove_credentials()`,
  `ubdcc_get_credentials_list()` → `get_credentials_list()` (each with its
  `_async` variant). The matching UBDCC REST endpoints were renamed too
  (`/ubdcc_*_credentials*` → `/*_credentials*`) — use UBDCC ≥ 0.7.0.
  Examples under `examples/unicorn_binance_depth_cache_cluster/` updated.
### Fixed
- `manager.py`: REST snapshot support for Binance margin exchanges. The
  exchange switch in `_get_order_book_from_rest()` had no case for
  `binance.com-margin`, `binance.com-margin-testnet`,
  `binance.com-isolated_margin` and `binance.com-isolated_margin-testnet`,
  so the snapshot returned `None` and the DepthCache never reached the
  `synchronized` state. Margin markets use the spot REST endpoint
  (`/api/v3/depth`) and the spot WebSocket diff-depth format (`U/u`),
  so they are now routed through the same code path as `binance.com`
  across all four exchange switches in `manager.py` (snapshot fetch,
  live-update gap detection, post-sync buffer replay gap detection,
  and init-phase sync-point detection).

## 2.13.0
### Added
- `manager.py`: New `set_credentials(api_key, api_secret)` method on
  `BinanceLocalDepthCacheManager` — swap the internal
  `BinanceRestApiManager` to a fresh instance bound to the given credentials
  at runtime, without recreating the depth cache manager or interrupting
  the WebSocket streams. New credentials take effect from the next REST
  call (snapshot / resync). Pass `None` / `None` to drop credentials and
  fall back to public rate limits. Enables UBDCC DCNs to react to
  credential rebalances pushed from the cluster management.

## 2.12.3
### Fixed
- `manager.py`: `binance.com-vanilla-options` depth caches never reached
  the `synchronized` state because Binance's `/eapi/v1/depth` REST
  endpoint serves a cached snapshot whose `lastUpdateId` can lag the
  live diff stream by ~25–30 seconds. With the snapshot consistently
  older than every buffered event, no event satisfied the
  `U <= lastUpdateId <= u` sync predicate, and the previous replay
  implementation dropped the init buffer on every failed attempt,
  guaranteeing an endless resync loop. The init buffer is now retained
  across resync attempts (pruned by `u < lastUpdateId` and capped at
  10 000 entries), so once Binance's REST cache rotates far enough
  forward, a previously buffered event matches the sync predicate and
  the cache synchronises. Spot and Futures are unaffected because their
  REST snapshots are live; behaviour for those exchanges is identical
  when the first replay finds the sync point on the first try (the
  common case). Post-sync events that were already in the buffer are
  now applied via the regular gap-detection path (Spot:
  `U == lastUpdateId + 1`, Futures/Options: `pu == lastUpdateId`)
  instead of being silently discarded, which also closes a pre-existing
  gap where fast initial bursts could leave the cache one or more
  events behind immediately after sync.

## 2.12.2
### Changed
- Bumped minimum `unicorn-binance-websocket-api` dependency from
  `>=2.12.0` to `>=2.12.2` in `setup.py`, `requirements.txt`,
  `pyproject.toml`, `environment.yml` and `meta.yaml`. 2.12.2 is the
  cleanup-round UBWA release.
- `setup.py`, `dev/set_version.py`, `dev/test_plain.py`: file header
  `Author: LUCIT Systems and Development` → `Oliver Zehentleitner`,
  copyright `LUCIT Systems and Development (2022-2023)` →
  `Oliver Zehentleitner (2022-2026)`.
- `dev/test_plain.py`: dropped the obsolete
  `from lucit_licensing_python.exceptions import NoValidatedLucitLicense`
  import and the corresponding `try/except NoValidatedLucitLicense`
  wrapper — the LUCIT licensing manager has been removed from UBLDC.
- `SECURITY.md`: replaced the lucit.tech contact form URL with the
  GitHub Security Advisories private-reporting URL.
- README: switched all conda references from the legacy `lucit` channel
  to `conda-forge`. Added conda-forge version / downloads / feedstock
  build badges. Removed the "There is no conda support until migration"
  placeholders. Install section is now a single
  `conda install -c conda-forge unicorn-binance-local-depth-cache`.
- README: reworded the PyPy paragraph. The old sentence ("For the PyPy
  interpreter we offer packages only from Python version 3.9 and
  higher") made sense when we still shipped wheels for pre-3.9 CPython;
  replaced with "PyPy wheels are available for all supported Python
  versions." Also dropped the stale "Anaconda packages are available
  from Python version 3.8 and higher" line and fixed the Python range
  in the Installation section to 3.9 – 3.14.
- Aligned dependency pins across `requirements.txt`, `setup.py`,
  `pyproject.toml`, `environment.yml` and `meta.yaml` using `setup.py`
  as the source of truth (`Cython>=3.0.10`, `requests>=2.32.3`;
  `orjson` was missing from `environment.yml` and has been added).
- `environment.yml`: dropped the `lucit` channel and the `defaults`
  channel; removed `lucit::` prefixes on suite deps; bumped
  `python>=3.8` to `python>=3.9` to match the rest.
- `meta.yaml`: removed the leftover `channels:` and `dependencies:`
  blocks (they are `environment.yml` keys, not valid in `meta.yaml`).
  Dropped the `lucit::` channel prefixes from suite deps. Re-embedded
  the current `README.md` into `about.description`. License is MIT.
### Removed
- `.github/workflows/build_conda.yml`: the conda-forge feedstock
  (`conda-forge/unicorn-binance-local-depth-cache-feedstock`) now
  builds and publishes the conda package; no in-repo build is needed.

## 2.12.1
### Fixed
- Options depth cache: default to `depth@500ms` when `depth_cache_update_interval` is not set (Options has no bare `@depth` stream)

## 2.12.0
### Added
- Support for Binance European Options (Vanilla Options) depth caches via `exchange="binance.com-vanilla-options"`
- New exchange strings: `binance.com-vanilla-options`, `binance.com-vanilla-options-testnet`
- Options depth cache uses the same sync algorithm as Futures (`pu`-based gap detection)
### Changed
- Minimum dependency: `unicorn-binance-rest-api>=2.10.0` (Options Market Data API)
- Minimum dependency: `unicorn-binance-websocket-api>=2.12.0` (Options exchange support)

## 2.11.2
### Fixed
- Error in GitHub Action

## 2.11.1
### Fixed
- Dependency conflict

## 2.11.0
### Added
- `Cluster` class now wraps the UBDCC 0.4.0 credential endpoints: `ubdcc_add_credentials`, `ubdcc_remove_credentials`, `ubdcc_get_credentials_list` (each with a sync + async variant). Lets you manage per-account-group Binance API key pairs on a running cluster without falling back to raw HTTP. Public responses keep keys masked and never expose `api_secret`. Two demo scripts under `examples/unicorn_depthcache_cluster_for_binance/` (`manage-credentials.py` / `-async.py`).
- `on_restart` callback parameter on `BinanceLocalDepthCacheManager` — invoked as `on_restart(market, timestamp)` every time a stream restart is detected, once per market on the affected stream. Enables reactive consumers (e.g. UBDCC) to forward restart events without polling.
- `get_last_restart_time(market)` — returns Unix timestamp of the last stream restart serving this market (or `None` if not restarted yet)
- `get_restart_count(market)` — returns the number of restarts of the stream serving this market
- Both getters expose UBLDC'''s existing per-stream restart tracking as a clean public API for on-demand queries (complement to the callback).

## 2.10.0
### Changed
- cluster.py: switched from stdlib `json` to `orjson` (suite-wide standard) — added `orjson` to dependencies
- cluster.py: `create_depthcache(s)` switched from GET to POST — markets list is now sent as JSON body to UBDCC 0.2.0, fixing URL-too-long errors when creating many DepthCaches at once
- README: updated cluster section (no longer "K8s application" — also runs locally via `pip install ubdcc`)
### Fixed
- manager.py: `get_latest_version()` crashed with `AttributeError: 'NoneType' object has no attribute 'get'` when the GitHub API request failed — now checks `isinstance(status, dict)` before calling `.get()`
- cluster.py: fixed double JSON serialization in POST requests (`json=json.dumps(params)` → `json=params`) that caused server-side 500 errors
- unittest: updated test_create_depthcache(s) to mock `requests.post` (not `requests.get`) after the GET→POST switch
- README: fixed wrong `ubdcc_port`, method names, typo "DephtCache" → "DepthCache"

## 2.9.0
### Added
- Added `get_last_update_time(market)` — returns Unix timestamp in milliseconds of the last processed depth update, or `None` if not yet synced (closes #35)
- Added support for exchange `trbinance.com` (closes #13) — note: TRBinance requires an API key even for public REST endpoints; pass `api_key`/`api_secret` to `BinanceRestApiManager`
- Added Python 3.14 support
- Added mocked unit tests for `Cluster` class (cluster.py)
### Fixed
- manager.py: detect REST API error responses in `_get_order_book_from_rest()` and log clearly instead of failing silently with a `KeyError` — includes hint for `trbinance.com` about required API key
- cluster.py: replaced `print()` with proper `logger` calls in `_request()` and `_request_async()` — `error` for network/client failures, `warning` for timeouts and cancellations
### Changed
- build_wheels.yml: Upgraded `cibuildwheel` from `v3.0.0` to `v3.4.1`
- setup.py: Fixed author from "LUCIT Systems and Development" to "Oliver Zehentleitner"
### Removed
- Dropped Python 3.8 support
- Removed `Cluster.submit_license()` and `Cluster.submit_license_async()` — LUCIT licensing is gone
- Removed `ClusterEndpoints.submit_license` endpoint definition
- Removed `examples/unicorn_depthcache_cluster_for_binance/submit-license*.py`
- `Cluster.test_connection()`: updated app name check from `lucit-ubdcc-restapi` to `ubdcc-restapi`

## 2.8.1
### Added
- build_wheels.yml:  
  CIBW_ARCHS_LINUX: "x86_64 aarch64"
  CIBW_ARCHS_MACOS: "x86_64 arm64 universal2"
  CIBW_ARCHS_WINDOWS: "AMD64"
  CIBW_MUSLLINUX_X86_64_IMAGE: "musllinux_1_1"
### Changed
- Moved from https://github.com/LUCIT-Systems-and-Development/ to https://github.com/oliver-zehentleitner
### Removed
- LUCIT Licensing Manager

## 2.8.0
### Changed
- `get_list_of_depth_caches()` is deprecated, use `get_list_of_depthcaches()` instead! From now on, only active 
  DepthCaches are returned!
- `stop_depthcache()` removes asks and bids, but the rest of the DepthCache remains.

## 2.7.0
### Changed
- Holding the thread lock is now in the more abstract functions.
### Fixed
- 'Uncontrolling growth of elements in lists of asks and bids in Depth Cache Manager' 
  [issue#45](https://github.com/oliver-zehentleitner/unicorn-binance-local-depth-cache/issues/45)
  Thanks to [@chubatrik](https://github.com/chubatrik) for finding and reporting it!
- 'error' and 'result' messages are now processed separately with corresponding log levels.
- In `_get_book_side()` only the thread lock of 'bid' was used by mistake, also for 'asks'. This has now been corrected.
- 'stop_depth_cache returns "error_msg: stream_id is missing!"'
  [issue#46](https://github.com/oliver-zehentleitner/unicorn-binance-local-depth-cache/issues/46)

## 2.6.0
### Added
- Counting restarts and logging last restart time in `ubldc.dc_streams`.

## 2.5.0
### Added
- Support of `auto_data_cleanup_stopped_streams` - Passthrough to UBWA.

## 2.4.1
### Fixed
- ValueError in `stop_depthcache()`

## 2.4.0
### Changed
- Rewrite of the init process. Now it is possible to successfully create much more DepthCaches than before!

## 2.3.0
### Added
- Async client functions for interacting with the UNICORN DepthCache Cluster for Binance.
### Fixed
- DepthCache management now correctly handles refreshes.

## 2.2.0
### Added
- ***Experimental*** Client functions for interacting with the UNICORN DepthCache Cluster for Binance 
- Support multiple streams to bypass subscription limit per stream
### Changed
- Dropping support for Python 3.7
### Renamed 
- 'ubldc.create_depth_cache()' -> 'ubldc.create_depthcache()' 
- 'ubldc.stop_depth_cache()' -> 'ubldc.stop_depthcache()'

## 2.1.1
### Fixed
- Wrong sort order in `get_asks()` - bug was released with 2.1.0.

## 2.1.0
Stability and performance optimization
### Added
- DepthCache specific infos to `print_summary()`.
### Changed
- More granular and efficient transfer of update values.
- `init_time_window` default value 10 to 5
- `websocket_ping_interval` default value 5 to 10
- `websocket_ping_timeout` default value 15 to 20
### Fixed
- Filtering and removing 0 values now works with all formats. (0.0, 0.000, 0.0000000, ...)
- Updates were erroneously applied twice in `_init_depth_cache()`.
- Handling all stream signals of UBWA clearly.
- RuntimeError in the for loop of `_sort_depth_cache()` 

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
- Ip ban when using `create_depth_cache` with many symbols [issue#30](https://github.com/oliver-zehentleitner/unicorn-binance-local-depth-cache/issues/30)
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
  https://github.com/oliver-zehentleitner/unicorn-binance-local-depth-cache/blob/master/LICENSE
- Conversion to a C++ compiled Cython package with precompiled as well as PyPy and source code wheels.
- Setup of a "Trusted Publisher" deployment chain. The source code is transparently packaged into wheels directly from
  the GitHub repository by a GitHub action for all possible platforms and published directly as a new release on GitHub
  and PyPi. A second process from Conda-Forge then uploads it to Anaconda. Thus, the entire deployment process is
  transparent and the user can be sure that the compilation of a version fully corresponds to the source code.
- `manager.stop_manager()` alias for `manager.stop_manager_with_all_caches()` 
- Support for `with`-context.

## 0.7.3
### Fixed 
- TypeError exception in `_init_depth_cache` [issue#27](https://github.com/oliver-zehentleitner/unicorn-binance-local-depth-cache/issues/27

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
