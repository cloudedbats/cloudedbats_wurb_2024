#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: https://cloudedbats.github.io, https://github.com/cloudedbats
# Copyright (c) 2023-present Arnold Andreasson
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import logging
import wurb_core


class RecDevices(object):
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
        # Capture.
        self.capture_name_part_list = ["Pettersson", "UltraMic"]
        self.capture_device_name = ""
        self.capture_device_index = None
        self.capture_sampling_freq_hz = 0
        self.capture_channels = 0
        # Playback.
        self.playback_name_part_list = ["headphones", "MacBook"]
        self.playback_device_name = ""
        self.playback_device_index = None
        self.playback_sampling_freq_hz = 0
        self.playback_channels = 0

    def get_capture_device_info(self):
        """ """
        self.check_capture_devices()
        info = {}
        info["device_name"] = self.capture_device_name
        info["sampling_freq_hz"] = self.capture_sampling_freq_hz
        info["device_index"] = self.capture_device_index
        info["input_channels"] = self.capture_channels
        return info

    def get_playback_device_info(self):
        """ """
        self.check_playback_devices()
        info = {}
        info["device_name"] = self.playback_device_name
        info["sampling_freq_hz"] = self.playback_sampling_freq_hz
        info["device_index"] = self.playback_device_index
        info["output_channels"] = self.playback_channels
        return info

    def is_mic_available(self):
        """ """
        device_info = wurb_core.rec_devices.get_capture_device_info()
        device_index = device_info.get("device_index", None)
        if device_index == None:
            return False
        else:
            return True

    def is_speaker_available(self):
        """ """
        device_info = wurb_core.rec_devices.get_playback_device_info()
        device_index = device_info.get("device_index", None)
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
            device_name = ""
            device_index = None
            sampling_freq_hz = 0
            for device_name_part in self.capture_name_part_list:
                try:
                    for device_by_name in devices_by_name.keys():
                        if device_name_part in device_by_name:
                            device = devices_by_name[device_by_name]
                            device_index = device.get("device_index", "")
                            device_name = device.get("device_name", "")
                            input_channels = device.get("input_channels", "")
                            sampling_freq_hz = device.get("sampling_freq_hz", "")
                            # Done.
                            self.set_capture_device(
                                device_name,
                                device_index,
                                sampling_freq_hz,
                                input_channels,
                            )
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
            self.set_capture_device("", None, 0, 0)

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
            device_name = ""
            device_index = None
            sampling_freq_hz = 0
            for device_name_part in self.playback_name_part_list:
                try:
                    for device_name in devices_by_name.keys():
                        if device_name_part in device_name:
                            device = devices_by_name[device_name]
                            device_index = device.get("device_index", "")
                            device_name = device.get("device_name", "")
                            output_channels = device.get("output_channels", "")
                            sampling_freq_hz = device.get("sampling_freq_hz", "")
                            # Done.
                            self.set_playback_device(
                                device_name,
                                device_index,
                                sampling_freq_hz,
                                output_channels,
                            )
                            return
                except:
                    pass

            # Not found.
            self.set_playback_device("", None, 0, 0)

        except Exception as e:
            message = "RecDevices - check_playback_devices. Exception: " + str(e)
            self.logger.debug(message)

    def set_capture_device(
        self, device_name, device_index, sampling_freq_hz, input_channels
    ):
        """ """
        try:
            self.capture_device_name = device_name
            self.capture_device_index = device_index
            self.capture_sampling_freq_hz = sampling_freq_hz
            self.capture_channels = input_channels
        except Exception as e:
            message = "RecDevices - set_capture_device. Exception: " + str(e)
            self.logger.debug(message)

    def set_playback_device(
        self, device_name, device_index, sampling_freq_hz, output_channels
    ):
        """ """
        try:
            self.playback_device_name = device_name
            self.playback_device_index = device_index
            self.playback_sampling_freq_hz = sampling_freq_hz
            self.playback_channels = output_channels
        except Exception as e:
            message = "RecDevices - set_playback_device. Exception: " + str(e)
            self.logger.debug(message)
