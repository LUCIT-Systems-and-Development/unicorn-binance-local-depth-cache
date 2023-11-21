#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: dev/set_version.sh
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
# Copyright (c) 2022-2023, LUCIT Systems and Development (https://www.lucit.tech)
# All rights reserved.

import sys


def replace_string_in_files(replace_string,
                            config_file_path="./dev/set_version_config.txt",
                            log_file_path="./dev/set_version.log"):
    with open(config_file_path, 'r', encoding='utf-8') as config_file:
        lines = config_file.readlines()
        search_string = lines[0].strip()
        file_list = lines[1].strip().split(',')

    for file_path in file_list:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            content = content.replace(search_string, replace_string)

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Replaced in {file_path}")
        except FileNotFoundError:
            print(f"FileNotFoundError: {file_path}")
        except Exception as e:
            print(f"Error during editing {file_path}: {e}")

    with open(log_file_path, 'a', encoding='utf-8') as log_file:
        log_file.write(f"Replaced: {search_string} with {replace_string}\n")

    with open(config_file_path, 'w', encoding='utf-8') as config_file:
        config_file.write(replace_string + '\n' + ','.join(file_list) + '\n')


if __name__ == "__main__":
    input_replace_string = sys.argv[1]
    replace_string_in_files(input_replace_string)
