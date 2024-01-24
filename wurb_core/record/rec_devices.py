#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: https://cloudedbats.github.io
# Author: Arnold Andreasson, info@cloudedbats.org
# License: MIT License (see LICENSE or http://opensource.org/licenses/mit).

import logging
import wurb_core


class RecDevices(object):
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
        self.config_capture_devices = []
        self.config_playback_devices = []
        self.configure()

    def clear(self):
        """ """
        # Capture.
        self.capture_device = None
        # Playback.
        self.playback_device = None

    def configure(self):
        """ """
        # Capture.
        self.config_capture_devices = wurb_core.config.get("audio_capture")
        # Playback.
        self.config_playback_devices = wurb_core.config.get("audio_playback")

    def get_capture_device_info(self):
        """ """
        if self.capture_device == None:
            self.check_capture_devices()
        #
        if self.capture_device in [None, {}]:
            return {}
        return self.capture_device

    def get_playback_device_info(self):
        """ """
        if "device_index" not in self.playback_device_info:
            self.check_playback_devices()
        #
        if self.playback_device_info in [None, {}]:
            return {}
        return self.playback_device_info

    def is_mic_available(self):
        """ """
        if self.capture_device in [None, {}]:
            return False
        else:
            return True

    def is_speaker_available(self):
        """ """
        if self.playback_device in [None, {}]:
            return False
        else:
            return True

    def check_capture_devices(self):
        """ """
        self.capture_device = None
        try:
            #
            available_devices = wurb_core.audio_capture.get_capture_devices()
            #
            for config_device_dict in self.config_capture_devices:
                try:
                    config_name_part = config_device_dict["device_name"]
                    config_sampling_freq_hz = config_device_dict["sampling_freq_hz"]
                    for device_dict in available_devices:
                        device_full_name = device_dict["device_name"]
                        if config_name_part in device_full_name:
                            sampling_freq_hz = device_dict["sampling_freq_hz"]

                            if int(config_sampling_freq_hz) == int(sampling_freq_hz):
                                self.capture_device = device_dict
                                # Adjust to config.
                                if "channels" in config_device_dict:
                                    self.capture_device[
                                        "config_channels"
                                    ] = config_device_dict.get("channels", "")
                                # Done.
                                return
                except Exception as e:
                    message = "RecDevices - check_capture_devices-1. Exception: " + str(
                        e
                    )
                    self.logger.debug(message)
            # # Check if Pettersson M500.
            # if not device_name:
            #     if self.pettersson_m500.is_m500_available():
            #         device_name = self.pettersson_m500.get_device_name()
            #         sampling_freq_hz = self.pettersson_m500.get_sampling_freq_hz()
            # # Check if another ALSA mic. is specified in advanced settings.

            # Not found.
            self.capture_device_info = {}

        except Exception as e:
            message = "RecDevices - check_capture_devices-2. Exception: " + str(e)
            self.logger.debug(message)

    def check_playback_devices(self):
        """ """
        self.playback_device = None
        try:
            #
            available_devices = wurb_core.audio_playback.get_playback_devices()
            #
            for config_device_dict in self.config_playback_devices:
                try:
                    config_name_part = config_device_dict["device_name"]
                    for device_dict in available_devices:
                        device_full_name = device_dict["device_name"]
                        if config_name_part in device_full_name:
                            self.playback_device = device_dict
                            # Adjust to config.
                            if "sampling_freq_hz" in config_device_dict:
                                self.playback_device[
                                    "sampling_freq_hz"
                                ] = config_device_dict.get("sampling_freq_hz", "")
                            if "period_size" in config_device_dict:
                                self.playback_device[
                                    "period_size"
                                ] = config_device_dict.get("period_size", "")
                            if "buffer_size" in config_device_dict:
                                self.playback_device[
                                    "buffer_size"
                                ] = config_device_dict.get("buffer_size", "")
                            if "buffer_max_size" in config_device_dict:
                                self.playback_device[
                                    "buffer_max_size"
                                ] = config_device_dict.get("buffer_max_size", "")
                            if "in_queue_length" in config_device_dict:
                                self.playback_device[
                                    "in_queue_length"
                                ] = config_device_dict.get(
                                    "chin_queue_lengthannels", ""
                                )
                            # Done.
                            return
                except Exception as e:
                    message = (
                        "RecDevices - check_playback_devices-1. Exception: " + str(e)
                    )
                    self.logger.debug(message)
        except Exception as e:
            message = "RecDevices - check_playback_devices-2. Exception: " + str(e)
            self.logger.debug(message)
