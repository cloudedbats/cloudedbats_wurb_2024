#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: https://cloudedbats.github.io, https://github.com/cloudedbats
# Copyright (c) 2023-present Arnold Andreasson
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import asyncio
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
        # self.rec_event = asyncio.Event()

    def clear(self):
        """ """
        # Ultrasound microphones supported by default:
        # - Pettersson: u256, u384, M500-384 and M500.
        # - Dodotronic: UltraMic 192K, 200K, 250K, 384K.
        self.default_name_part_list = ["Pettersson", "UltraMic", "EasyMic", "Pettersson u384 USB Ultrasound Microphone"]
        self.device_name = ""
        self.device_index = None
        self.sampling_freq_hz = 0
        self.check_interval_s = 5.0
        self.notification_event = None
#         self.pettersson_m500 = wurb_utils.PetterssonM500()
# ####        self.alsa_cards = wurb_core.AlsaSoundCards()
#         self.alsa_capture = None

    def check_devices(self):
        """For asyncio events."""
        try:
            capture_devices = wurb_core.audio_capture.get_capture_devices()
            devices_by_name = {}
            for capture_device in capture_devices:
                name = capture_device.get("name", "")
                devices_by_name[name] = capture_device
            #
            self.set_connected_device("", None, 0)
            device_name = ""
            device_index = None
            sampling_freq_hz = 0
            for device_name_part in self.default_name_part_list:
                try:
                    if device_name_part in devices_by_name:
                        device = devices_by_name[device_name_part]
                        device_index = device.get("index", "")
                        device_name = device.get("name", "")
                        sampling_freq_hz = device.get("defaultSampleRate", "")
                        break
                except:
                    pass

            # Check if Pettersson M500.
            if not device_name:
                if self.pettersson_m500.is_m500_available():
                    device_name = self.pettersson_m500.get_device_name()
                    sampling_freq_hz = self.pettersson_m500.get_sampling_freq_hz()
            # Check if another ALSA mic. is specified in advanced settings.

            # Done.
            self.set_connected_device(device_name, device_index, sampling_freq_hz)

        except Exception as e:
            # Logging error.
            message = "Rec. check_devices: " + str(e)
            wurb_core.wurb_logger.error(message)

    def reset_devices(self):
        """For asyncio events."""
        try:
            self.set_connected_device("", None, 0)

        except Exception as e:
            # Logging error.
            message = "Recorder: reset_devices: " + str(e)
            wurb_core.wurb_logger.error(message)

    def get_notification_event(self):
        """ """
        try:
            if self.notification_event == None:
                self.notification_event = asyncio.Event()
            return self.notification_event
        except Exception as e:
            # Logging error.
            message = "Recorder: get_notification_event: " + str(e)
            wurb_core.wurb_logger.error(message)

    def get_connected_device(self):
        """ """
        try:
            return self.device_index, self.device_name, self.sampling_freq_hz
        except Exception as e:
            # Logging error.
            message = "Recorder: get_connected_device: " + str(e)
            wurb_core.wurb_logger.error(message)

    def set_connected_device(self, device_name, device_index, sampling_freq_hz):
        """ """
        try:
            self.device_name = device_name
            self.device_index = device_index
            self.sampling_freq_hz = sampling_freq_hz
            # Create a new event and release all from the old event.
            old_notification_event = self.notification_event
            self.notification_event = asyncio.Event()
            if old_notification_event:
                old_notification_event.set()
        except Exception as e:
            # Logging error.
            message = "Recorder: set_connected_device: " + str(e)
            wurb_core.wurb_logger.error(message)
