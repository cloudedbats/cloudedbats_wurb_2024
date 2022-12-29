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


class SoundPlayback:
    """ """

    def __init__(self, logger="DefaultLogger"):
        """ """
        self.config = None
        self.queue = None
        self.card_index = None
        self.sampling_freq_hz = None
        self.channels = None
        self.buffer_size = None
        self.period_size = None
        self.buffer_max_size = None
        self.playback_active = False
        self.playback_queue_active = False
        self.playback_executor = None
        self.buffer_int16 = None
        self.logger = logging.getLogger(logger)

    def setup(self, card_index, config):
        """ """
        self.config = config
        self.card_index = int(card_index)
        # Setup queue for data in.
        in_queue_length = int(self.config["in_queue_length"])
        self.queue = asyncio.Queue(maxsize=in_queue_length)
        # Setup for sound playback.
        self.sampling_freq_hz = int(self.config["sampling_freq_hz"])
        self.channels = self.config["channels"]
        self.buffer_size = int(self.config["buffer_size"])
        self.period_size = int(self.config["period_size"])
        self.buffer_max_size = int(self.config["buffer_max_size"])

    def get_queue(self):
        """ """
        return self.queue

    async def start(self):
        """ """
        # Use executor for the IO-blocking part.
        main_loop = asyncio.get_event_loop()
        self.playback_executor = main_loop.run_in_executor(None, self.run_playback)
        await asyncio.sleep(0.1)
        # Clear queue.
        while not self.queue.empty():
            self.queue.get_nowait()
            self.queue.task_done()
        # Copy data from queue to buffer.
        self.playback_queue_active = True
        while self.playback_queue_active:
            try:
                data_dict = await self.queue.get()
                if "data" in data_dict:
                    self.add_data(data_dict["data"])
            except asyncio.CancelledError:
                break
            except Exception as e:
                # Logging error.
                message = "SoundPlayback, failed to read data queue: " + str(e)
                self.logger.debug(message)

    async def stop(self):
        """ """
        self.playback_active = False
        self.playback_queue_active = False
        if self.playback_executor:
            self.playback_executor.cancel()
            self.playback_executor = None

    def add_data(self, data):
        """ """
        # self.logger.debug("DEBUG DATA ADDED. Length: ", len(data))
        if self.buffer_int16 is None:
            self.buffer_int16 = numpy.array([], dtype=numpy.int16)
        # Avoid to long delay.
        if len(self.buffer_int16) <= self.buffer_max_size:
            self.buffer_int16 = numpy.concatenate((self.buffer_int16, data))
        else:
            self.logger.debug("SKIP. Len: " + str(self.buffer_int16.size))

    def run_playback(self):
        """ """
        pmc_play = None
        channels = 1
        if self.channels.upper() == "STEREO":
            channels = 2
        self.playback_active = True
        try:
            # Setup ALSA for playback.
            pmc_play = alsaaudio.PCM(
                alsaaudio.PCM_PLAYBACK,
                alsaaudio.PCM_NORMAL,
                channels=channels,
                rate=self.sampling_freq_hz,
                format=alsaaudio.PCM_FORMAT_S16_LE,
                periodsize=self.period_size,
                device="sysdefault",
                cardindex=self.card_index,
            )
            # To be used when no data in buffer.
            silent_buffer = numpy.zeros((self.period_size, 1), dtype=numpy.float16)
            # Loop over the IO blocking part.
            while self.playback_active:
                try:
                    # Use silent buffer as default.
                    buffer_int16 = silent_buffer
                    #
                    if (self.buffer_int16 is not None) and (
                        self.buffer_int16.size >= self.period_size
                    ):
                        # Copy part to be used.
                        buffer_int16 = self.buffer_int16[: self.period_size]
                        # Remove used part.
                        self.buffer_int16 = self.buffer_int16[self.period_size :]

                    #     self.logger.debug("SOUND. Len: " + str(self.buffer_int16.size))
                    # else:
                    #     if self.buffer_int16 is not None:
                    #         self.logger.debug("SILENCE. Len: " + str(self.buffer_int16.size))

                    # Convert to byte buffer and write.
                    buffer_bytes = buffer_int16.tobytes()
                    pmc_play.write(buffer_bytes)

                except asyncio.CancelledError:
                    break
                except Exception as e:
                    self.logger.error("EXCEPTION PLAYBACK-1: " + str(e))
        #
        except asyncio.CancelledError:
            pass
        except Exception as e:
            self.logger.error("EXCEPTION PLAYBACK-2: " + str(e))
        finally:
            self.playback_active = False
            if pmc_play:
                pmc_play.close()
            self.logger.debug("PLAYBACK ENDED.")
