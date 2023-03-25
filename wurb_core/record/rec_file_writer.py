#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: https://cloudedbats.github.io, https://github.com/cloudedbats
# Copyright (c) 2023-present Arnold Andreasson
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import asyncio
import logging
import pathlib
import wave
import time

import wurb_core


class RecFileWriter(object):
    """ """

    def __init__(self, config=None, logger=None, logger_name="DefaultLogger"):
        """ """
        if config == None:
            self.config = {}
        else:
            self.config = config
        if logger == None:
            self.logger = logging.getLogger(logger_name)
        else:
            self.logger = logger
        #
        self.clear()

    def clear(self):
        """ """
        self.rec_target_dir_path = None
        self.wave_file = None
        # self.size_counter = 0

    def create(self, start_time, max_peak_freq_hz, max_peak_dbfs):
        """ """
        rec_file_prefix = wurb_core.wurb_settings.get_setting("filenamePrefix")
        rec_type = wurb_core.wurb_settings.get_setting("recType")
        sampling_freq_hz = 384000 ############### self.wurb_recorder.sampling_freq_hz
        if rec_type == "TE":
            sampling_freq_hz = int(sampling_freq_hz / 10.0)


        try:
            # self.rec_target_dir_path = wurb_core.wurb_rpi.get_wavefile_target_dir_path()
            rec_target_dir = wurb_core.config.get("record.target.rec_dir", default="../wurb_recordings")
            self.rec_target_dir_path = pathlib.Path(rec_target_dir)
            if not self.rec_target_dir_path.exists():
                self.rec_target_dir_path.mkdir(parents=True)
        except:
            pass

        if self.rec_target_dir_path is None:
            self.wave_file = None
            return

        rec_datetime = self.get_datetime(start_time)
        rec_location = self.get_location()
        rec_type_str = self.create_rec_type_str(
            384000, rec_type
            ########### self.wurb_recorder.sampling_freq_hz, rec_type
        )

        # Peak info to filename.
        peak_info_str = ""
        if max_peak_freq_hz and max_peak_dbfs:
            peak_info_str += "_"  # "_Peak"
            peak_info_str += str(int(round(max_peak_freq_hz / 1000.0, 0)))
            peak_info_str += "kHz"
            peak_info_str += str(int(round(max_peak_dbfs, 0)))
            peak_info_str += "dB"

        # Filename example: "WURB1_20180420T205942+0200_N00.00E00.00_TE384.wav"
        filename = rec_file_prefix
        filename += "_"
        filename += rec_datetime
        filename += "_"
        filename += rec_location
        filename += "_"
        filename += rec_type_str
        filename += peak_info_str
        filename += ".wav"

        # Create directories.
        if not self.rec_target_dir_path.exists():
            self.rec_target_dir_path.mkdir(parents=True)
        # Open wave file for writing.
        filenamepath = pathlib.Path(self.rec_target_dir_path, filename)
        self.wave_file = wave.open(str(filenamepath), "wb")
        self.wave_file.setnchannels(1)  # 1=Mono.
        self.wave_file.setsampwidth(2)  # 2=16 bits.
        self.wave_file.setframerate(sampling_freq_hz)
        # Logging.
        target_path_str = str(self.rec_target_dir_path)
        target_path_str = target_path_str.replace("/media/pi/", "USB:")
        target_path_str = target_path_str.replace("/home/pi/", "SD-card:/home/pi/")
        message_rec_type = ""
        if rec_type == "TE":
            message_rec_type = "(TE) "
        message = "Sound file " + message_rec_type + "to: " + target_path_str
        wurb_core.wurb_logger.info(message)
        # Logging debug.
        message = "Filename: " + filename
        wurb_core.wurb_logger.debug(message=message)

    def write(self, buffer):
        """ """
        if self.wave_file is not None:
            self.wave_file.writeframes(buffer)
            # self.size_counter += len(buffer) / 2  # Count frames.

    def close(self):
        """ """
        if self.wave_file is not None:
            self.wave_file.close()
            self.wave_file = None

        # Copy settings to target directory.
        try:
            if self.rec_target_dir_path is not None:
                from_dir = wurb_core.wurb_settings.settings_dir_path
                log_file_name = wurb_core.wurb_settings.settings_file_name
                from_file_path = pathlib.Path(from_dir, log_file_name)
                to_file_path = pathlib.Path(self.rec_target_dir_path, log_file_name)
                to_file_path.write_text(from_file_path.read_text())
                # Logging debug.
                wurb_core.wurb_logger.debug(message="File closed.")
        except Exception as e:
            # Logging error.
            message = "Recorder: Copy settings to wave file directory: " + str(e)
            wurb_core.wurb_logger.error(message)

    def get_datetime(self, start_time):
        """ """
        datetime_str = time.strftime("%Y%m%dT%H%M%S%z", time.localtime(start_time))
        return datetime_str

    def get_location(self):
        """ """
        latlongstring = ""
        try:
            latitude_dd, longitude_dd = wurb_core.wurb_settings.get_valid_location()

            if latitude_dd >= 0.0:
                latlongstring += "N"
            else:
                latlongstring += "S"
            latlongstring += str(abs(latitude_dd))
            #
            if longitude_dd >= 0.0:
                latlongstring += "E"
            else:
                latlongstring += "W"
            latlongstring += str(abs(longitude_dd))
        except:
            latlongstring = "N00.00E00.00"

        return latlongstring

    def create_rec_type_str(self, sampling_freq_hz, rec_type):
        """ """
        try:
            sampling_freq_khz = sampling_freq_hz / 1000.0
            sampling_freq_khz = int(round(sampling_freq_khz, 0))
        except:
            sampling_freq_khz = "FS000"

        return rec_type + str(sampling_freq_khz)
