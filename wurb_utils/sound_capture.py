#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Main project: https://github.com/cloudedbats
# Copyright (c) 2023-present Arnold Andreasson
# License: MIT License (see LICENSE or http://opensource.org/licenses/mit).

import asyncio
import logging
import numpy


class SoundCapture:
    """ """

    def __init__(self, audio, logger_name="DefaultLogger"):
        """ """
        self.logger = logging.getLogger(logger_name)
        self.audio = audio
        self.clear()

    def clear(self):
        self.device_index = None
        self.channels = None
        self.sampling_freq_hz = None
        self.frames = None
        self.buffer_size = None
        #
        self.out_queue_list = []
        self.main_loop = None
        self.capture_executor = None

    def get_capture_devices(self, part_of_name=None):
        """ """
        cards = []
        try:
            number_of_devices = self.audio.get_device_count()
            for index in range(number_of_devices):
                device_info = self.audio.get_device_info_by_index(index)
                device_name = device_info.get("name", "")
                input_channels = device_info.get("maxInputChannels", "")
                if int(input_channels) > 0:
                    if part_of_name in [None, ""]:
                        cards.append(device_info)
                    else:
                        if part_of_name in device_name:
                            cards.append(device_info)
        except:
            pass
        return cards

    def setup(
        self,
        device_index,
        channels,
        sampling_freq_hz,
        frames,
        buffer_size,
    ):
        """ """
        self.device_index = device_index
        self.channels = channels
        self.sampling_freq_hz = sampling_freq_hz
        self.frames = frames
        self.buffer_size = buffer_size

    def add_out_queue(self, out_queue):
        """ """
        self.out_queue_list.append(out_queue)

    async def start(self):
        """ """
        # Use executor for the IO-blocking part.
        self.main_loop = asyncio.get_event_loop()
        self.capture_executor = self.main_loop.run_in_executor(None, self.run_capture)

    async def stop(self):
        """ """
        self.capture_active = False
        if self.capture_executor:
            self.capture_executor.cancel()
            self.capture_executor = None

    def run_capture(self):
        """ """
        self.capture_active = True
        channels = 1
        if self.channels.upper() in ["STEREO", "MONO-LEFT", "MONO-RIGHT"]:
            channels = 2
        try:
            # p = pyaudio.PyAudio()
            stream = self.audio.open(
                format=self.audio.get_format_from_width(2),
                channels=channels,
                rate=self.sampling_freq_hz,
                input=True,
                output=False,
                input_device_index=self.device_index,
                frames_per_buffer=self.frames,
            )
            # Empty numpy buffer.
            in_buffer_int16 = numpy.array([], dtype=numpy.int16)
            while self.capture_active:
                # Read from capture device.
                data = stream.read(self.frames, exception_on_overflow=False)
                # Convert from string-byte array to int16 array.
                in_data_int16 = numpy.frombuffer(data, dtype=numpy.int16)

                # print("CAPTURE: Lengt int16: ", len(in_data_int16))
                # print(in_data_int16[:10])
                # print(numpy.max(in_data_int16))

                # Convert stereo to mono by using either left or right channel.
                if self.channels.upper() == "MONO-LEFT":
                    in_data_int16 = in_data_int16[0::2].copy()
                if self.channels.upper() == "MONO-RIGHT":
                    in_data_int16 = in_data_int16[1::2].copy()
                # Concatenate
                in_buffer_int16 = numpy.concatenate((in_buffer_int16, in_data_int16))
                while len(in_buffer_int16) >= self.buffer_size:
                    # Copy "buffer_size" part and save remaining part.
                    data_int16 = in_buffer_int16[0 : self.buffer_size]
                    in_buffer_int16 = in_buffer_int16[self.buffer_size :]

                    # Put data on queues in the queue list.
                    for data_queue in self.out_queue_list:
                        # Copy data.
                        data_int16_copy = data_int16.copy()
                        # Put together.
                        data_dict = {
                            "status": "data",
                            "data": data_int16_copy,
                        }
                        try:
                            if not data_queue.full():
                                self.main_loop.call_soon_threadsafe(
                                    data_queue.put_nowait, data_dict
                                )
                            else:
                                self.logger.debug("Sound capture: Queue full.")
                        #
                        except Exception as e:
                            # Logging error.
                            message = "Failed to put captured sound on queue: " + str(e)
                            self.logger.error(message)
                            if not self.main_loop.is_running():
                                # Terminate.
                                self.capture_active = False
                                break
        #
        except asyncio.CancelledError:
            pass
        except Exception as e:
            self.logger.error("EXCEPTION Sound capture: " + str(e))
        finally:
            self.capture_active = False
            stream.close()
            # p.terminate()
            self.logger.debug("Sound capture ended.")
