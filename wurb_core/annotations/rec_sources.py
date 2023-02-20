#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org, https://github.com/cloudedbats
# Copyright (c) 2023-present Arnold Andreasson
# License: MIT License (see LICENSE or http://opensource.org/licenses/mit).

import asyncio
import logging
import pathlib
import datetime
import dateutil.parser
import yaml

import wurb_core


class RecSources(object):
    """ """

    def __init__(self, logger="DefaultLogger"):
        """ """
        self.logger_name = logger
        self.logger = logging.getLogger(logger)
        self.clear()

    def clear(self):
        """ """
        self.sources_by_id = {}

    def load_sources(self):
        """ """
        if not self.sources_by_id:
            self.sources_by_id = {}
            sources = wurb_core.config.get("annotations.sources")
            for source in sources:
                id = source.get("id", "")
                if id:
                    self.sources_by_id[id] = source

    def get_rec_dir(self, source_id):
        """ """
        self.load_sources()
        result = ""
        source = self.sources_by_id.get(source_id, "")
        if source:
            result = source.get("rec_dir", "")
        return result
    
    def get_cache_dir(self, source_id):
        """ """
        self.load_sources()
        result = ""
        source = self.sources_by_id.get(source_id, "")
        if source:
            result = source.get("cache_dir", "")
        return result

    def get_rec_sources(self):
        """ """
        result = []
        sources = wurb_core.config.get("annotations.sources")
        for source in sources:
            new_dict = {}
            new_dict["id"] = source.get("id", "")
            new_dict["name"] = source.get("name", "")
            result.append(new_dict)
        return result

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

    def get_rec_nights(self, source_id):
        """ """
        result = []
        rec_dir = self.get_rec_dir(source_id)
        if rec_dir:
            rec_dir_path = pathlib.Path(rec_dir).resolve()
            if rec_dir_path.exists():
                for dir2 in sorted(rec_dir_path.iterdir()):
                    if dir2.is_dir():
                        night = {}
                        night["recId"] = dir2.name
                        night["recFilePath"] = str(dir2.resolve())
                        result.append(night)
        #
        return result

    def get_rec_info(self, source_id, night_id, record_id):
        """ """
        json_data = {
            "fileIndex": 1,
            "maxIndex": 70,
            "eventPath": "wurb_recordings",
            "waveFileName": "w53.......",
            "spectrogramPath": "wurb_recordings",
            "spectrogramName": "Taberg_2022-12-30_PEAKS.png",
            "overviewPath": "wurb_recordings",
            "overviewName": "Taberg_2022-12-30_PEAKS.png",
            "quality": "Q2",
            "tags": ["FM-QCF", "Social"],
            "comments": "Comment...",
        }
        return json_data
