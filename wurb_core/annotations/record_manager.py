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


class RecordManager(object):
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
        # Needs only be loaded once.
        if not self.sources_by_id:
            self.sources_by_id = {}
            sources = wurb_core.config.get("annotations.sources")
            for source in sources:
                id = source.get("id", "")
                if id:
                    self.sources_by_id[id] = source

    def get_source_dir(self, source_id):
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
        source_dir = self.get_source_dir(source_id)
        if source_dir:
            source_dir_path = pathlib.Path(source_dir).resolve()
            if source_dir_path.exists():
                for dir2 in sorted(source_dir_path.iterdir()):
                    if dir2.is_dir():
                        night = {}
                        night["id"] = dir2.name
                        result.append(night)
        #
        return result

    def get_rec_files(self, source_id, night_id, record_id):
        """ """
        result = []
        source_dir = pathlib.Path(self.get_source_dir(source_id)).resolve()
        night_dir = pathlib.Path(source_dir, night_id).resolve()
        if night_dir.exists():
            for record_file in sorted(night_dir.glob("*.wav")):
                result.append(record_file)
        #
        return result

    def get_rec_file(self, source_id, night_id, record_id):
        """ """
        result = ""
        source_dir = pathlib.Path(self.get_source_dir(source_id)).resolve()
        night_dir = pathlib.Path(source_dir, night_id).resolve()
        if night_dir.exists():
            recorded_files = sorted(night_dir.glob(record_id + "*.wav"))
            # if len(recorded_files) == 1:
            if len(recorded_files) > 0:
                result = recorded_files[0]
            else:
                print("ERROR...")
        #
        return result

    def get_rec_info(self, source_id, night_id, record_id):
        """ """
        rec_file = self.get_rec_file(source_id, night_id, record_id)
        rec_files = self.get_rec_files(source_id, night_id, record_id)
        prefix, utc_datetime, local_date, local_time = wurb_core.metadata.get_rec_keys(rec_file)
        metadata = wurb_core.metadata.get_metadata(rec_file)
        annotations = metadata.get("annotations", [])
        annotation = annotations[0]


        rec_ids = []
        for rec in sorted(rec_files):
            rec_ids.append(wurb_core.metadata.get_rec_id(rec))

        if not record_id in ["", None]:
            if not record_id in rec_ids:
                print("ERROR: record_id is missing in the nights list.")

        first_record_id = ""
        previous_record_id = ""
        next_record_id = ""
        last_record_id = ""
        last_record_id = ""
        record_index = 0

        if len(rec_files) > 0:
            for index, rec_id in enumerate(rec_ids):
                if record_id in ["", None]:
                    record_id = rec_id
                last_record_id = rec_id
                if first_record_id == "":
                    first_record_id = rec_id
                if record_id == rec_id:
                            record_index = index + 1
                if next_record_id == "":
                    if rec_id > record_id:
                        next_record_id = rec_id
                if rec_id < record_id:
                    previous_record_id = rec_id
        
        record_data = {
            "sourceId": source_id,
            "nightId": night_id,
            "recordId": record_id,
            "firstRecordId": first_record_id,
            "previousRecordId": previous_record_id,
            "nextRecordId": next_record_id,
            "lastRecordId": last_record_id,
            "index": str(record_index),
            "maxIndex": str(len(rec_files)),
            "recordFile": rec_file.name,
            "prefix": prefix,
            "localDate": str(local_date),
            "localTime": str(local_time),
            "dateTimeUtc": str(utc_datetime),
            "quality": annotation.get("quality", ""),
            "tags": str(annotation.get("tags", [])),
            "comments": annotation.get("comments", ""),
        }
        return record_data
