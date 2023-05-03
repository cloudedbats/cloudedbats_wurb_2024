#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org, https://github.com/cloudedbats
# Copyright (c) 2023-present Arnold Andreasson
# License: MIT License (see LICENSE or http://opensource.org/licenses/mit).

import asyncio
import logging
import pathlib

import wurb_core


class AdminCleanup(object):
    """ """

    def __init__(self, config=None, logger=None, logger_name="DefaultLogger"):
        """ """
        self.config = config
        self.logger = logger
        if self.config == None:
            self.config = {}
        if self.logger == None:
            self.logger = logging.getLogger(logger_name)
        #
        self.clear()
        self.configure()

    def clear(self):
        """ """

    def configure(self):
        """ """

    async def remove_q0(self, source_id, night_id):
        """ """
        quality_by_file = self.extract_quality(source_id, night_id)
        for file, quality in quality_by_file.items():
            if quality == "Q0":
                rec_file_path = pathlib.Path(file)
                if rec_file_path.exists():
                    rec_file_path.unlink()
                    print("WAV-FILE DELETED (Q0): ", str(rec_file_path))
                wurb_core.metadata.delete_metadata(rec_file_path)

        return {}

    async def remove_not_assigned(self, source_id, night_id):
        """ """
        quality_by_file = self.extract_quality(source_id, night_id)
        for file, quality in quality_by_file.items():
            if quality == "Not assigned":
                rec_file_path = pathlib.Path(file)
                if rec_file_path.exists():
                    rec_file_path.unlink()
                    print("WAV-FILE DELETED (NA): ", str(rec_file_path))
                wurb_core.metadata.delete_metadata(rec_file_path)

        return {}

    async def delete_monitoring_night(self, source_id, night_id):
        """ """
        print("TEST: delete_monitoring_night")
        return {}

    def extract_quality(self, source_id, night_id):
        """ """
        quality_by_file = {}
        # Get files for night.
        for rec_file in wurb_core.record_manager.get_rec_files(source_id, night_id):
            print("FILE: ", str(rec_file))
            # Get metadata for recording.
            metadata = wurb_core.metadata.get_metadata(rec_file)
            flat_metadata = self.flatten_metadata(metadata)
            quality = flat_metadata.get("annotations.wurb-user.quality", "")
            quality_by_file[str(rec_file)] = quality
        return quality_by_file

    def flatten_metadata(self, metadata):
        """ """
        flat_metadata = {}
        # Recording.
        recording_dict = metadata.get("recording", {})
        for key, value in recording_dict.items():
            flat_metadata["recording." + key] = value
        # Annotations.
        annotations = metadata.get("annotations", {})
        for annotation in annotations:
            user = annotation.get("user", "no-user")
            for key, value in annotation.items():
                flat_metadata["annotations." + user + "." + key] = value
        #
        return flat_metadata
