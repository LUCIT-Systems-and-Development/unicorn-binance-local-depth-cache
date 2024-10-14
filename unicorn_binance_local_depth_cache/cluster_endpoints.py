#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯
#
# File: unicorn_binance_local_depth_cache/cluster_endpoints.py
#
# Part of ‘UNICORN Binance Local Depth Cache’
# Project website: https://www.lucit.tech/unicorn-binance-local-depth-cache.html
# Github: https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache
# Documentation: https://unicorn-binance-local-depth-cache.docs.lucit.tech
# PyPI: https://pypi.org/project/unicorn-binance-local-depth-cache
# LUCIT Online Shop: https://shop.lucit.services/software
#
# License: LSOSL - LUCIT Synergetic Open Source License
# https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/blob/master/LICENSE
#
# Author: LUCIT Systems and Development
#
# Copyright (c) 2022-2024, LUCIT Systems and Development - https://www.lucit.tech
# All rights reserved.

class ClusterEndpoints:
    create_depthcache: str = "create_depthcache"
    create_depthcaches: str = "create_depthcaches"
    get_asks: str = "get_asks"
    get_bids: str = "get_bids"
    get_cluster_info: str = "get_cluster_info"
    get_depthcache_list: str = "get_depthcache_list"
    get_depthcache_info: str = "get_depthcache_info"
    stop_depthcache: str = "stop_depthcache"
    submit_license: str = "submit_license"
    test: str = "test"
