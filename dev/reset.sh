#!/usr/bin/bash

rm *.log
rm *.py.log
rm *.c
rm dev/*.log

rm build -r
rm dist -r
rm *.egg-info -r
rm stubs -r
rm out -r

rm unicorn_binance_local_depth_cache/*.c
rm unicorn_binance_local_depth_cache/*.cpp
rm unicorn_binance_local_depth_cache/*.html
rm unicorn_binance_local_depth_cache/*.dll
rm unicorn_binance_local_depth_cache/*.so
rm unicorn_binance_local_depth_cache/*.pyi
