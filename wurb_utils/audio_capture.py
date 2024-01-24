#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: https://cloudedbats.github.io
# Author: Arnold Andreasson, info@cloudedbats.org
# License: MIT License (see LICENSE or http://opensource.org/licenses/mit).

import asyncio
import logging
import numpy
import time


class AudioCapture:
    """ """

    def __init__(self, audio, logger_name="DefaultLogger"):
        """ """
        self.logger = logging.getLogger(logger_name)
        self.audio = audio
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
        if self.capture_is_active == True:
            info_dict = self.get_selected_capture_device()
            return [info_dict]
        devices = []
        try:
            number_of_devices = self.audio.get_device_count()
            for index in range(number_of_devices):
                device_info = self.audio.get_device_info_by_index(index)
                device_name = device_info.get("name", "")
                input_channels = device_info.get("maxInputChannels", "")
                # # Test for Windows to remove devices with wrong rate.
                # host_api = device_info.get("hostApi", "")
                # if (int(input_channels) > 0) and (host_api == 2):
                if int(input_channels) > 0:
                    info_dict = {}
                    info_dict["device_name"] = device_name
                    info_dict["input_channels"] = input_channels
                    info_dict["device_index"] = device_info.get("index", "")
                    info_dict["sampling_freq_hz"] = device_info.get(
                        "defaultSampleRate", ""
                    )
                    devices.append(info_dict)
        except Exception as e:
            self.logger.debug("AudioCapture - get_capture_devices: " + str(e))
        return devices

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
        try:
            if self.capture_is_running == True:
                self.logger.debug(
                    "AudioCapture - Start: Capture is running, waiting 2 sec... "
                )
                await asyncio.sleep(2.0)
                if self.capture_is_running == True:
                    self.logger.debug(
                        "AudioCapture - Start: Capture is still running, will be stopped... "
                    )
                    self.stop()

            # Use executor for the IO-blocking part.
            self.main_loop = asyncio.get_event_loop()
            self.capture_executor = self.main_loop.run_in_executor(
                None, self.run_capture
            )
        except Exception as e:
            message = "AlsaAudioPlayback - start. Exception: " + str(e)
            self.logger.debug(message)

    async def stop(self):
        """ """
        try:
            self.capture_is_active = False
            if self.capture_executor != None:
                self.capture_executor.cancel()
                self.capture_executor = None
        except Exception as e:
            message = "AlsaAudioPlayback - stop. Exception: " + str(e)
            self.logger.debug(message)

    def run_capture(self):
        """ """
        stream = None
        self.capture_is_active = True
        try:
            self.logger.debug("AudioCapture - Sound capture started.")
            # p = pyaudio.PyAudio()
            stream = self.audio.open(
                format=self.audio.get_format_from_width(2),
                channels=self.channels,
                rate=self.sampling_freq_hz,
                input=True,
                output=False,
                input_device_index=self.device_index,
                # Number of frames not needed here.
                # frames_per_buffer=self.frames_per_buffer,
            )
            self.capture_is_running = True
            # Time related.
            calculated_time_s = time.time()
            time_increment_s = self.buffer_size / self.sampling_freq_hz
            # Empty numpy buffer.
            in_buffer_int16 = numpy.array([], dtype=numpy.int16)
            while self.capture_is_active:
                # Read from capture device.
                data = stream.read(self.frames_per_buffer, exception_on_overflow=False)
                # Convert from string-byte array to int16 array.
                in_data_int16 = numpy.frombuffer(data, dtype=numpy.int16)

                # print("CAPTURE: Length int16: ", len(in_data_int16))
                # print(in_data_int16[:10])
                # print(numpy.max(in_data_int16))

                # Convert stereo to mono by using either left or right channel.
                if self.channels == 2:
                    if self.config_channels.upper() == "MONO-LEFT":
                        in_data_int16 = in_data_int16[0::2].copy()
                    if self.config_channels.upper() == "MONO-RIGHT":
                        in_data_int16 = in_data_int16[1::2].copy()
                # Concatenate
                in_buffer_int16 = numpy.concatenate((in_buffer_int16, in_data_int16))
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
                                self.logger.debug("AudioCapture - Queue full.")
                        #
                        except Exception as e:
                            message = (
                                "AudioCapture - Failed to put captured sound on queue: "
                                + str(e)
                            )
                            self.logger.error(message)
                            if not self.main_loop.is_running():
                                # Terminate.
                                self.capture_is_active = False
                                break
        #
        except asyncio.CancelledError:
            self.logger.debug("AudioCapture - Was cancelled.")
        except Exception as e:
            message = "AudioCapture - run_capture. Exception: " + str(e)
            self.logger.debug(message)
        finally:
            self.logger.debug("AudioCapture - Capture ended.")
            self.capture_is_active = False
            if stream:
                stream.close()
            # p.terminate()
            self.capture_is_running = False
