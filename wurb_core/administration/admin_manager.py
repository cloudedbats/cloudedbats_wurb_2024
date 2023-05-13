#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org, https://github.com/cloudedbats
# Copyright (c) 2023-present Arnold Andreasson
# License: MIT License (see LICENSE or http://opensource.org/licenses/mit).

import asyncio
import logging
import pathlib

import wurb_core


class AdminManager(object):
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

    async def get_admin_info(self, source_id, night_id):
        """ """
        monitoring_night = ""
        directory_path = ""
        number_of_sound_files = 0
        number_of_q0 = 0
        number_of_not_assigned = 0

        if night_id not in ["", "select"]:
            monitoring_night = night_id
            if (source_id) and (night_id):
                dir_path = pathlib.Path(
                    wurb_core.record_manager.get_source_dir(source_id)
                ).resolve()
                directory_path = str(dir_path)
                rec_files = wurb_core.record_manager.get_rec_files(source_id, night_id)
                number_of_sound_files = len(rec_files)
                for rec_file in rec_files:
                    metadata = wurb_core.metadata.get_metadata(rec_file)
                    flat_metadata = wurb_core.metadata.flatten_metadata(metadata)
                    quality = flat_metadata.get("annotations.wurb-user.quality", "")
                    if quality == "Q0":
                        number_of_q0 += 1
                    if quality == "Not assigned":
                        number_of_not_assigned += 1
                    await asyncio.sleep(0)

        admin_info = {
            "monitoringNight": monitoring_night,
            "dirPath": directory_path,
            "numberOfSoundFiles": number_of_sound_files,
            "numberOfQ0": number_of_q0,
            "numberOfNoAssigned": number_of_not_assigned,
        }
        return admin_info
