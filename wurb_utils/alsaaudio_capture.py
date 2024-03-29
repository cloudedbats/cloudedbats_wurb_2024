#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: https://cloudedbats.github.io
# Author: Arnold Andreasson, info@cloudedbats.org
# License: MIT License (see LICENSE or http://opensource.org/licenses/mit).

import asyncio
import logging
import numpy
import time

#
alsaaudio_installed = True
try:
    import alsaaudio
except:
    alsaaudio_installed = False


class AlsaAudioCapture:
    """ """

    def __init__(self, logger_name="DefaultLogger"):
        """ """
        self.logger = logging.getLogger(logger_name)
        self.clear()

    def clear(self):
        self.device_index = None
        self.device_name = ""
        self.channels = None
        self.config_channels = None
        self.sampling_freq_hz = None
        self.frames_per_buffer = None
        self.buffer_size = None
        #
        self.out_queue_list = []
        self.main_loop = None
        self.capture_executor = None
        self.capture_is_running = False
        self.capture_is_active = False

    def is_capture_running(self):
        """ """
        return self.capture_is_running

    def get_selected_capture_device(self):
        """ """
        info_dict = {}
        info_dict["device_index"] = self.device_index
        info_dict["device_name"] = self.device_name
        info_dict["input_channels"] = self.channels
        info_dict["config_channels"] = self.config_channels
        info_dict["sampling_freq_hz"] = self.sampling_freq_hz
        return info_dict

    def get_capture_devices(self):
        """ """
        if alsaaudio_installed == False:
            return []
        if self.capture_is_active == True:
            info_dict = self.get_selected_capture_device()
            return [info_dict]
        devices = []
        card_list = []
        try:
            # List cards and names.
            # Note: Results from card_indexes() and cards() must be mapped.
            card_ids = alsaaudio.cards()
            for id_index, card_index in enumerate(alsaaudio.card_indexes()):
                card_dict = {}
                card_dict["card_index"] = card_index
                card_dict["card_id"] = card_ids[id_index]
                card_name, long_name = alsaaudio.card_name(card_index)
                card_dict["card_name"] = card_name.strip()
                card_dict["card_long_name"] = long_name.strip()
                card_list.append(card_dict)
            # Check card devices for capture.
            for device in alsaaudio.pcms(alsaaudio.PCM_CAPTURE):
                if device.startswith("sysdefault:CARD="):
                    card_id = device.replace("sysdefault:CARD=", "").strip()
                    for card_dict in card_list:
                        if card_dict.get("card_id", "") == card_id:
                            card_dict["device"] = device
                            card_index = card_dict.get("card_index", "")
                            if card_index != "":
                                info_dict = {}
                                info_dict["device_index"] = card_index
                                info_dict["device_name"] = card_dict.get(
                                    "card_name", ""
                                )
                                #
                                more_info = self.get_more_device_info(card_index)
                                info_dict["input_channels"] = more_info["channels"]
                                info_dict["sampling_freq_hz"] = more_info["max_freq_hz"]
                                info_dict["freq_list"] = more_info["freq_list"]
                                print( info_dict["device_name"], ": ",  more_info["freq_list"])

                                devices.append(info_dict)
        except Exception as e:
            message = "AlsaAudioCapture - get_capture_devices. Exception: " + str(e)
            self.logger.debug(message)
        return devices

    def get_more_device_info(self, card_index):
        """Only for capture devices."""
        more_info = {}
        max_freq = -99
        inp = None
        try:
            try:
                inp = alsaaudio.PCM(
                    alsaaudio.PCM_CAPTURE,
                    alsaaudio.PCM_NORMAL,
                    format=alsaaudio.PCM_FORMAT_S16_LE,
                    device="sysdefault",
                    cardindex=card_index,
                )
                # Add more info.
                info = inp.info()
                more_info["channels"] = info["channels"]
                more_info["default_freq_hz"] = info["rate"]
                # Rates may be list, tuple or a single value.
                rates = inp.getrates()
                if type(rates) in [list, tuple]:
                    more_info["freq_list"] = list(inp.getrates())
                    max_freq = inp.getrates()[-1]
                    more_info["max_freq_hz"] = max_freq
                else:
                    max_freq = inp.getrates()
                    more_info["freq_list"] = [max_freq]
                    more_info["max_freq_hz"] = max_freq
            except Exception as e:
                message = "AlsaAudioCapture - get_more_device_info. Exception: " + str(e)
                self.logger.debug(message)
        finally:
            if inp:
                inp.close()
        return more_info

    def setup(
        self,
        device_index,
        device_name,
        channels,
        config_channels,
        sampling_freq_hz,
        frames_per_buffer,
        buffer_size,
    ):
        """ """
        self.device_index = device_index
        self.device_name = device_name
        self.channels = channels
        self.config_channels = config_channels
        self.sampling_freq_hz = sampling_freq_hz
        self.frames_per_buffer = frames_per_buffer
        self.buffer_size = buffer_size

    def add_out_queue(self, out_queue):
        """ """
        self.out_queue_list.append(out_queue)

    async def start(self):
        """ """
        if alsaaudio_installed == False:
            message = "AlsaAudioCapture - pyalsaaudio not installed: " + str(e)
            self.logger.debug(message)
        try:
            while self.capture_is_running == True:
                self.logger.debug(
                    "AlsaAudioCapture - Start: Capture is running, waiting 2 sec... "
                )
                await asyncio.sleep(2.0)

            # Use executor for the IO-blocking part.
            self.main_loop = asyncio.get_event_loop()
            self.capture_executor = self.main_loop.run_in_executor(
                None, self.run_capture
            )
        except Exception as e:
            message = "AlsaAudioCapture - start. Exception: " + str(e)
            self.logger.debug(message)

    async def stop(self):
        """ """
        try:
            self.capture_is_active = False
            if self.capture_executor != None:
                self.capture_executor.cancel()
                self.capture_executor = None
        except Exception as e:
            message = "AlsaAudioCapture - stop. Exception: " + str(e)
            self.logger.debug(message)

    def run_capture(self):
        """ """
        pmc_capture = None
        self.capture_is_active = True
        try:
            self.logger.debug("AlsaAudioCapture - Sound capture started.")
            pmc_capture = alsaaudio.PCM(
                alsaaudio.PCM_CAPTURE,
                alsaaudio.PCM_NORMAL,
                channels=self.channels,
                rate=self.sampling_freq_hz,
                format=alsaaudio.PCM_FORMAT_S16_LE,
                periodsize=self.frames_per_buffer,
                # periodsize=int(1024 * 4),
                device="sysdefault",
                cardindex=self.device_index,
            )
            self.capture_is_running = True
            # Time related.
            calculated_time_s = time.time()
            time_increment_s = self.buffer_size / self.sampling_freq_hz
            # Empty numpy buffer.
            in_buffer_int16 = numpy.array([], dtype=numpy.int16)
            while self.capture_is_active:
                # Read from capture device.
                length, data = pmc_capture.read()
                if length < 0:
                    self.logger.debug(
                        "AlsaAudioCapture - Capture overrun: " + str(length)
                    )
                elif len(data) > 0:
                    # Convert from string-byte array to int16 array.
                    in_data_int16 = numpy.frombuffer(data, dtype=numpy.int16)

                    # print("CAPTURE: length: ", length, "   data-len: ", len(in_data_int16))

                    # Convert stereo to mono by using either left or right channel.
                    if self.config_channels in ["MONO-LEFT", "MONO-RIGHT"]:
                        if self.config_channels.upper() == "MONO-LEFT":
                            in_data_int16 = in_data_int16[0::2].copy()
                        if self.config_channels.upper() == "MONO-RIGHT":
                            in_data_int16 = in_data_int16[1::2].copy()
                    # Concatenate
                    in_buffer_int16 = numpy.concatenate(
                        (in_buffer_int16, in_data_int16)
                    )
                    while len(in_buffer_int16) >= self.buffer_size:
                        # Copy "buffer_size" part and save remaining part.
                        data_int16 = in_buffer_int16[0 : self.buffer_size]
                        in_buffer_int16 = in_buffer_int16[self.buffer_size :]

                        # Put data on queues in the queue list.
                        for data_queue in self.out_queue_list:
                            # Time rounded to half sec.
                            calculated_time_s += time_increment_s
                            device_time = int((calculated_time_s) * 2) / 2
                            # Used to detect time drift.
                            detector_time = time.time()
                            # Copy data.
                            data_int16_copy = data_int16.copy()
                            # Put together.
                            data_dict = {
                                "status": "data",
                                "adc_time": device_time,
                                "detector_time": detector_time,
                                "data": data_int16_copy,
                            }
                            try:
                                if not data_queue.full():
                                    self.main_loop.call_soon_threadsafe(
                                        data_queue.put_nowait, data_dict
                                    )
                                else:
                                    self.logger.debug("AlsaAudioCapture - Queue full.")
                            #
                            except Exception as e:
                                message = (
                                    "AlsaAudioCapture - Failed to put on queue: "
                                    + str(e)
                                )
                                self.logger.debug(message)
                                if not self.main_loop.is_running():
                                    # Terminate.
                                    self.capture_is_active = False
                                    break
        #
        except asyncio.CancelledError:
            self.logger.debug("AlsaAudioCapture - Was cancelled.")
        except Exception as e:
            message = "AlsaAudioCapture - run_capture. Exception: " + str(e)
            self.logger.debug(message)
        finally:
            self.logger.debug("AlsaAudioCapture - Capture ended.")
            self.capture_is_active = False
            if pmc_capture:
                pmc_capture.close()
            self.capture_is_running = False
