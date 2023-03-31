#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: https://cloudedbats.github.io, https://github.com/cloudedbats
# Copyright (c) 2023-present Arnold Andreasson
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import logging
import pathlib
import wave
import datetime
import time

import wurb_core


class RecFileWriter(object):
    """ """

    def __init__(self):
        """ """
        self.clear()

    def clear(self):
        """ """
        self.device_name = None
        self.wave_file = None
        self.rec_target_dir_path = None
        self.rec_file_prefix = None
        self.rec_type = None
        self.sampling_freq_hz = None
        self.rec_datetime_str = None
        self.latitude_dd = None
        self.longitude_dd = None
        self.rec_latlongstring = None
        self.rec_type_str = None
        self.peak_info_str = None
        self.rec_filename_path = None
        self.max_peak_freq_hz = None
        self.max_peak_dbfs = None

    def prepare(
        self, device_name, sampling_freq_hz, start_time, max_peak_freq_hz, max_peak_dbfs
    ):
        """ """
        self.clear()
        self.device_name = device_name
        self.prepare_rec_target_dir()
        self.rec_file_prefix = wurb_core.wurb_settings.get_setting("filenamePrefix")
        self.rec_type = wurb_core.wurb_settings.get_setting("recType")
        self.sampling_freq_hz = int(sampling_freq_hz)
        if self.rec_type == "TE":
            self.sampling_freq_hz = int(self.sampling_freq_hz / 10.0)
        self.prepare_datetime(start_time)
        self.prepare_location()
        self.prepare_rec_type_str(self.sampling_freq_hz, self.rec_type)
        self.prepare_peak_info(max_peak_freq_hz, max_peak_dbfs)
        self.max_peak_freq_hz = max_peak_freq_hz
        self.max_peak_dbfs = max_peak_dbfs

    def prepare_rec_target_dir(self):
        """ """
        target_directory = wurb_core.config.get(
            "record.target.rec_dir", default="../wurb_recordings"
        )
        file_directory = wurb_core.wurb_settings.get_setting("fileDirectory")
        # Add date to file directory.
        # date_option = wurb_core.config.get(
        #     "file_directory_date_option", default="date-post-after"
        # )
        date_option = wurb_core.wurb_settings.get_setting("fileDirectoryDateOption")

        used_date_str = ""
        if date_option in ["date-pre-true", "date-post-true"]:
            used_date = datetime.datetime.now()
            used_date_str = used_date.strftime("%Y-%m-%d")
        if date_option in ["date-pre-after", "date-post-after"]:
            used_date = datetime.datetime.now() + datetime.timedelta(hours=12)
            used_date_str = used_date.strftime("%Y-%m-%d")
        if date_option in ["date-pre-before", "date-post-before"]:
            used_date = datetime.datetime.now() - datetime.timedelta(hours=12)
            used_date_str = used_date.strftime("%Y-%m-%d")
        if date_option in ["date-pre-true", "date-pre-after", "date-pre-before"]:
            rec_target_dir = used_date_str + "_" + file_directory
        elif date_option in ["date-post-true", "date-post-after", "date-post-before"]:
            rec_target_dir = file_directory + "_" + used_date_str
        else:
            rec_target_dir = file_directory
        #
        self.rec_target_dir_path = pathlib.Path(target_directory, rec_target_dir)
        if not self.rec_target_dir_path.exists():
            self.rec_target_dir_path.mkdir(parents=True)

    def prepare_datetime(self, start_time):
        """ """
        rec_datetime_str = time.strftime("%Y%m%dT%H%M%S%z", time.localtime(start_time))
        self.rec_datetime_str = rec_datetime_str

    def prepare_location(self):
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
        #
        self.latitude_dd = latitude_dd
        self.longitude_dd = longitude_dd
        self.rec_latlongstring = latlongstring

    def prepare_rec_type_str(self, sampling_freq_hz, rec_type):
        """ """
        try:
            sampling_freq_khz = sampling_freq_hz / 1000.0
            sampling_freq_khz = int(round(sampling_freq_khz, 0))
        except:
            sampling_freq_khz = "FS000"

        self.rec_type_str = rec_type + str(sampling_freq_khz)

    def prepare_peak_info(self, max_peak_freq_hz, max_peak_dbfs):
        """ """
        peak_info_str = ""
        if max_peak_freq_hz and max_peak_dbfs:
            peak_info_str += "_"  # "_Peak"
            peak_info_str += str(int(round(max_peak_freq_hz / 1000.0, 0)))
            peak_info_str += "kHz"
            peak_info_str += str(int(round(max_peak_dbfs, 0)))
            peak_info_str += "dB"
        self.peak_info_str = peak_info_str

    def open(self):
        """ """
        if self.rec_target_dir_path is None:
            self.wave_file = None
            return

        # Filename example: "WURB1_20180420T205942+0200_N00.00E00.00_TE384.wav"
        filename = self.rec_file_prefix
        filename += "_"
        filename += self.rec_datetime_str
        filename += "_"
        filename += self.rec_latlongstring
        filename += "_"
        filename += self.rec_type_str
        filename += self.peak_info_str
        filename += ".wav"

        # Create directories.
        if not self.rec_target_dir_path.exists():
            self.rec_target_dir_path.mkdir(parents=True)

        # Open wave file for writing.
        self.rec_filename_path = pathlib.Path(self.rec_target_dir_path, filename)
        self.wave_file = wave.open(str(self.rec_filename_path), "wb")
        self.wave_file.setnchannels(1)  # 1=Mono.
        self.wave_file.setsampwidth(2)  # 2=16 bits.
        self.wave_file.setframerate(self.sampling_freq_hz)
        # Logging.
        target_path_str = str(self.rec_target_dir_path)
        target_path_str = target_path_str.replace("/media/pi/", "USB:")
        target_path_str = target_path_str.replace("/home/pi/", "SD-card:/home/pi/")
        message_rec_type = ""
        if self.rec_type == "TE":
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

    def close(self):
        """ """
        if self.wave_file is not None:
            self.wave_file.close()
            self.wave_file = None
            #
            self.copy_settings()
            self.create_metadata()

    def copy_settings(self):
        """Copy settings to target directory."""
        # try:
        #     if self.rec_target_dir_path is not None:
        #         from_dir = wurb_core.wurb_settings.settings_dir_path
        #         log_file_name = wurb_core.wurb_settings.settings_file_name
        #         from_file_path = pathlib.Path(from_dir, log_file_name)
        #         to_file_path = pathlib.Path(self.rec_target_dir_path, log_file_name)
        #         to_file_path.write_text(from_file_path.read_text())
        #         # Logging debug.
        #         wurb_core.wurb_logger.debug(message="File closed.")
        # except Exception as e:
        #     # Logging error.
        #     message = "Recorder: Copy settings to wave file directory: " + str(e)
        #     wurb_core.wurb_logger.error(message)

    def create_metadata(self):
        """ """
        geoSource = wurb_core.wurb_settings.get_location_dict().get("geoSource", "")
        detectionLimitKhz = wurb_core.wurb_settings.get_setting("detectionLimitKhz")
        detectionSensitivityDbfs = wurb_core.wurb_settings.get_setting(
            "detectionSensitivityDbfs"
        )
        detectionAlgorithm = wurb_core.wurb_settings.get_setting("detectionAlgorithm")
        schedulerStartEvent = wurb_core.wurb_settings.get_setting("schedulerStartEvent")
        schedulerStartAdjust = wurb_core.wurb_settings.get_setting(
            "schedulerStartAdjust"
        )
        schedulerStopEvent = wurb_core.wurb_settings.get_setting("schedulerStopEvent")
        schedulerStopAdjust = wurb_core.wurb_settings.get_setting("schedulerStopAdjust")

        metadata = wurb_core.metadata.read_metadata(self.rec_filename_path)
        recording = metadata.get("recording", {})
        recording["deviceName"] = self.device_name
        recording["geoSource"] = geoSource
        recording["detectionLimitKhz"] = detectionLimitKhz
        recording["detectionSensitivityDbfs"] = detectionSensitivityDbfs
        recording["detectionAlgorithm"] = detectionAlgorithm
        recording["schedulerStartEvent"] = schedulerStartEvent
        recording["schedulerStartAdjust"] = schedulerStartAdjust
        recording["schedulerStopEvent"] = schedulerStopEvent
        recording["schedulerStopAdjust"] = schedulerStopAdjust
        if self.max_peak_freq_hz:
            recording["maxPeakFreqHz"] = str(round(self.max_peak_freq_hz))
        if self.max_peak_dbfs:
            recording["maxPeakDbfs"] = str(round(self.max_peak_dbfs, 1))

        latitude, longitude = wurb_core.wurb_settings.get_valid_location()
        if (latitude == 0.0) or (longitude == 0.0):
            pass
        else:
            sun_moon_dict = wurb_core.sun_moon.get_sun_moon_info(latitude, longitude)
            recording["sunsetLocal"] = str(sun_moon_dict.get("sunset_local", ""))
            recording["sunriseLocal"] = str(sun_moon_dict.get("sunrise_local", ""))
            recording["moonPhase"] = sun_moon_dict.get("moon_phase", "")
        #
        wurb_core.metadata.write_metadata(self.rec_filename_path, metadata)
