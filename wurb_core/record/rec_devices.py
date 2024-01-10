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
        self.configure()

    def clear(self):
        """ """
        # Capture.
        self.capture_device_info = {}
        # info["device_name"] = self.capture_device_name
        # info["sampling_freq_hz"] = self.capture_sampling_freq_hz
        # info["device_index"] = self.capture_device_index
        # info["input_channels"] = self.capture_channels

        # Playback.
        self.playback_device_info = {}
        # info["device_name"] = self.capture_device_name
        # info["sampling_freq_hz"] = self.capture_sampling_freq_hz
        # info["device_index"] = self.capture_device_index
        # info["input_channels"] = self.capture_channels

    def configure(self):
        """ """
        # # Capture.
        # self.capture_name_part_list = ["Pettersson", "UltraMic"]
        # # Playback.
        # self.playback_name_part_list = ["headphones", "MacBook"]

        # Capture.
        self.capture_name_part_list = []
        # self.capture_devices = []
        audio_devices = wurb_core.config.get("audio_capture")
        for audio_device in audio_devices:
            name = audio_device.get("device_name", "")
            if name:
                self.capture_name_part_list.append(name)
                # device_dict = {}
                # device_dict["name"] = name
                # device_dict["sampling_freq_hz"] = audio_device.get("sampling_freq_hz", "")
                # self.capture_devices.append(device_dict)
        # Playback.
        self.playback_name_part_list = []
        # self.playback_devices = []
        audio_devices = wurb_core.config.get("audio_playback")
        for audio_device in audio_devices:
            name = audio_device.get("device_name", "")
            if name:
                self.playback_name_part_list.append(name)
                # device_dict = {}
                # device_dict["name"] = name
                # device_dict["sampling_freq_hz"] = audio_device.get("sampling_freq_hz", "")
                # self.playback_devices.append(device_dict)

    def get_capture_device_info(self):
        """ """
        if "device_index" not in self.capture_device_info:
            self.check_capture_devices()
        #
        return self.capture_device_info

    def get_playback_device_info(self):
        """ """
        if "device_index" not in self.playback_device_info:
            self.check_playback_devices()
        #
        return self.playback_device_info

    def is_mic_available(self):
        """ """
        device_index = self.capture_device_info.get("device_index", None)
        if device_index == None:
            return False
        else:
            return True

    def is_speaker_available(self):
        """ """
        device_index = self.playback_device_info.get("device_index", None)
        if device_index == None:
            return False
        else:
            return True

    def check_capture_devices(self):
        """For asyncio events."""
        try:
            devices = wurb_core.audio_capture.get_capture_devices()
            devices_by_name = {}
            for device in devices:
                name = device.get("device_name", "")
                devices_by_name[name] = device
            #
            for device_name_part in self.capture_name_part_list:
                try:
                    for device_by_name in devices_by_name.keys():
                        if device_name_part in device_by_name:
                            device_info = devices_by_name[device_by_name]
                            self.capture_device_info = device_info
                            # Done.
                            return
                except:
                    pass

            # # Check if Pettersson M500.
            # if not device_name:
            #     if self.pettersson_m500.is_m500_available():
            #         device_name = self.pettersson_m500.get_device_name()
            #         sampling_freq_hz = self.pettersson_m500.get_sampling_freq_hz()
            # # Check if another ALSA mic. is specified in advanced settings.

            # Not found.
            self.capture_device_info = {}

        except Exception as e:
            message = "RecDevices - check_capture_devices. Exception: " + str(e)
            self.logger.debug(message)

    def check_playback_devices(self):
        """For asyncio events."""
        try:
            devices = wurb_core.audio_playback.get_playback_devices()
            devices_by_name = {}
            for device in devices:
                name = device.get("device_name", "")
                devices_by_name[name] = device
            #
            for device_name_part in self.playback_name_part_list:
                try:
                    for device_by_name in devices_by_name.keys():
                        if device_name_part in device_by_name:
                            device_info = devices_by_name[device_by_name]
                            self.playback_device_info = device_info
                            # Done.
                            return
                except:
                    pass
            # Not found.
            self.playback_device_info = {}

        except Exception as e:
            message = "RecDevices - check_playback_devices. Exception: " + str(e)
            self.logger.debug(message)
