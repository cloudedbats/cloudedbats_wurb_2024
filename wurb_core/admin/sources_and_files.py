#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org, https://github.com/cloudedbats
# Copyright (c) 2023-present Arnold Andreasson
# License: MIT License (see LICENSE or http://opensource.org/licenses/mit).

import asyncio
import logging
import pathlib

import wurb_core


class SourcesAndFiles(object):
    """ """

    def __init__(self, logger="DefaultLogger"):
        """ """
        self.logger_name = logger
        self.logger = logging.getLogger(logger)
        self.cache_by_source = {}

    # def get_rec_sources(self):
    #     """ """
    #     result = []
    #     dirs = wurb_core.config.get("field_annotations.directories")
    #     # print(str(dirs))
    #     for dir in dirs:
    #         source_dir = dir.get("source", "")
    #         cache_dir = dir.get("cache", "")
    #         if source_dir:
    #             source_dir_path = pathlib.Path(source_dir).resolve()
    #             cache_dir_path = pathlib.Path(cache_dir).resolve()
    #             result.append(str(source_dir_path))
    #             self.cache_by_source[str(source_dir_path)] = str(cache_dir_path)
    #     #
    #     return sorted(result)

    # def get_rec_cache(self, source_dir):
    #     """ """
    #     source_dir_path = pathlib.Path(source_dir).resolve()
    #     cache_dir = self.cache_by_source.get(str(source_dir_path), "")
    #     #
    #     return cache_dir

    # def get_rec_nights(self, source_dir):
    #     """ """
    #     result = []
    #     if source_dir:
    #         source_dir_path = pathlib.Path(source_dir)
    #         if source_dir_path.exists():
    #             # print("Exists: ", dir)
    #             for dir2 in source_dir_path.iterdir():
    #                 if dir2.is_dir():
    #                     result.append(str(dir2.resolve()))
    #     #
    #     return sorted(result)

    # def get_rec_files(self, night_dir):
    #     """ """
    #     result = []
    #     night_dir_path = pathlib.Path(night_dir)
    #     if night_dir_path.exists():
    #         if night_dir_path.is_dir():
    #             for file in night_dir_path.glob("*.wav"):
    #                 result.append(str(file.resolve()))
    #     #
    #     return sorted(result)
