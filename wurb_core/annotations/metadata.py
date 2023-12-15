#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: https://cloudedbats.github.io
# Author: Arnold Andreasson, info@cloudedbats.org
# License: MIT License (see LICENSE or http://opensource.org/licenses/mit).

import asyncio
import logging
import pathlib
import datetime
import dateutil.parser
import yaml

import wurb_core


class Metadata(object):
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
        self.metadata_header_rows = [
            "# Metadata for CloudedBats WURB-2024.",
            "#" "---",
        ]

    def get_data_dir(self, rec_file_path):
        """ """
        file_path = pathlib.Path(rec_file_path)
        parent_dir = file_path.parent
        data_dir_path = pathlib.Path(parent_dir, "data", "rec_metadata").resolve()
        if not data_dir_path.exists():
            data_dir_path.mkdir(parents=True)
        #
        return data_dir_path

    def get_metadata_file_path(self, rec_file_path):
        """ """
        data_dir = self.get_data_dir(rec_file_path)
        prefix, utc_datetime, local_date, local_time = self.get_rec_keys(rec_file_path)
        datetime_str = (
            str(local_date).replace("-", "") + "T" + str(local_time).replace(":", "")
        )
        metadata_file_path = pathlib.Path(
            data_dir, prefix + "_" + datetime_str + "_metadata.yaml"
        ).resolve()
        #
        return metadata_file_path

    def get_rec_id(self, rec_file_path):
        """ """
        data_dir = self.get_data_dir(rec_file_path)
        prefix, utc_datetime, local_date, local_time = self.get_rec_keys(rec_file_path)
        datetime_str = (
            str(local_date).replace("-", "") + "T" + str(local_time).replace(":", "")
        )
        rec_id = prefix + "_" + datetime_str
        #
        return rec_id

    def get_rec_keys(self, rec_file_path):
        """ """
        file_name = pathlib.Path(rec_file_path).name
        parts = file_name.split("_")
        prefix = parts[0]
        utc_datetime_str = parts[1]
        utc_datetime = dateutil.parser.isoparse(utc_datetime_str)
        local_date = utc_datetime.date()
        local_time = utc_datetime.time()
        #
        return prefix, utc_datetime, local_date, local_time

    def add_basic_metadata(self, rec_file_path):
        """ """
        rec_file_path = pathlib.Path(rec_file_path)
        metadata_file_path = self.get_metadata_file_path(rec_file_path)
        prefix, utc_datetime, local_date, local_time = self.get_rec_keys(rec_file_path)
        metadata = {}
        recording = {}
        metadata["recording"] = recording
        recording["recFileName"] = rec_file_path.name
        # recording["rec_file_path"] = str(rec_file_path.resolve())
        # recording["metadata_file_name"] = metadata_file_path.name
        # recording["metadata_file_path"] = str(metadata_file_path.resolve())

        # recording["cache_file_name"] = rec_file_path.name.replace(
        #     ".wav", "_SPECTROGRAM.jpg"
        # )
        # recording["cache_file_path"] = (
        #     str(rec_file_path.resolve())
        #     .replace("wurb_recordings", "wurb_cache/spectrograms")
        #     .replace(".wav", "_SPECTROGRAM.jpg")
        # )

        recording["prefix"] = prefix
        recording["dateTimeUtc"] = str(utc_datetime)
        recording["dateLocal"] = str(local_date)
        recording["timeLocal"] = str(local_time)
        metadata["annotations"] = [
            {
                "user": "wurb-user",
                "quality": "Not assigned",
                "tags": "",
                "comments": "",
            },
        ]
        #
        self.write_metadata(rec_file_path, metadata)

    def read_metadata(self, rec_file_path):
        """ """
        metadata = {}
        rec_file_path = pathlib.Path(rec_file_path)
        metadata_file_path = self.get_metadata_file_path(rec_file_path)
        if not metadata_file_path.exists():
            self.add_basic_metadata(rec_file_path)
        #
        with open(metadata_file_path, "r") as file:
            # metadata = yaml.load(file, Loader=yaml.Loader)
            metadata = yaml.safe_load(file)
        #
        return metadata

    def write_metadata(self, rec_file_path, metadata):
        """ """
        rec_file_path = pathlib.Path(rec_file_path)
        metadata_file_path = self.get_metadata_file_path(rec_file_path)
        #
        with open(metadata_file_path, "w") as file:
            file.writelines("\n".join(self.metadata_header_rows) + "\n")
            yaml.dump(metadata, file, default_flow_style=False)

    def get_metadata(self, rec_file_path):
        """ """
        metadata = {}
        rec_file_path = pathlib.Path(rec_file_path).resolve()
        # Read metadata from file.
        metadata = self.read_metadata(rec_file_path)
        #
        return metadata

    def delete_metadata(self, rec_file_path):
        """ """
        rec_file_path = pathlib.Path(rec_file_path)
        metadata_file_path = self.get_metadata_file_path(rec_file_path)
        if metadata_file_path.exists():
            metadata_file_path.unlink()
            print("METADATA DELETED: ", str(metadata_file_path))

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
