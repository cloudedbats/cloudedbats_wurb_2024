#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org, https://github.com/cloudedbats
# Copyright (c) 2023-present Arnold Andreasson
# License: MIT License (see LICENSE or http://opensource.org/licenses/mit).

import asyncio
import logging
import numpy
try:
    import alsaaudio
except: pass


class SoundCapture:
    """ """

    def __init__(self, logger="DefaultLogger"):
        """ """
        self.config = None
        self.out_queue_list = []
        self.card_index = None
        self.sampling_freq_hz = None
        self.channels = None
        self.buffer_size = None
        self.period_size = None
        self.main_loop = None
        self.capture_executor = None
        self.logger = logging.getLogger(logger)

    def setup(self, card_index, config):
        """ """
        self.config = config
        self.card_index = int(card_index)
        # List of out data queues.
        self.out_queue_list = []
        # Setup for sound capture.
        self.sampling_freq_hz = int(self.config["sampling_freq_hz"])
        self.channels = self.config["channels"]
        self.buffer_size = int(self.config["buffer_size"])
        self.period_size = int(self.config["period_size"])

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
        pmc_capture = None
        self.capture_active = True
        channels = 1
        if self.channels.upper() == "STEREO":
            channels = 2
        try:
            pmc_capture = alsaaudio.PCM(
                alsaaudio.PCM_CAPTURE,
                alsaaudio.PCM_NORMAL,
                channels=channels,
                rate=self.sampling_freq_hz,
                format=alsaaudio.PCM_FORMAT_S16_LE,
                periodsize=self.period_size,
                device="sysdefault",
                cardindex=self.card_index,
            )
            # Empty numpy buffer.
            in_buffer_int16 = numpy.array([], dtype=numpy.int16)
            while self.capture_active:
                # Read from capture device.
                length, data = pmc_capture.read()
                if length < 0:
                    self.logger.debug("Sound capture overrun: " + str(length))
                elif len(data) > 0:
                    # Convert from string-byte array to int16 array.
                    in_data_int16 = numpy.frombuffer(data, dtype=numpy.int16)

                    # print("CAPTURE: length: ", length, "   data-len: ", len(in_data_int16))

                    # Convert stereo to mono by using either left or right channel.
                    if self.channels.upper() == "MONO-LEFT":
                        in_data_int16 = in_data_int16[0::2].copy()
                    if self.channels.upper() == "MONO-RIGHT":
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
                                message = (
                                    "Failed to put captured sound on queue: " + str(e)
                                )
                                self.logger.error(message)
                                if not self.main_loop.is_running():
                                    # Terminate.
                                    self.capture_active = False
                                    break
        #
        except Exception as e:
            self.logger.error("EXCEPTION Sound capture: " + str(e))
        finally:
            self.capture_active = False
            if pmc_capture:
                pmc_capture.close()
            self.logger.debug("Sound capture ended.")
