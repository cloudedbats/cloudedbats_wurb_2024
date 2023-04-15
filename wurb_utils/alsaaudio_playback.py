#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org, https://github.com/cloudedbats
# Copyright (c) 2023-present Arnold Andreasson
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import asyncio
import logging
import numpy

try:
    import alsaaudio
except:
    pass


class AlsaAudioPlayback:
    """ """

    def __init__(self, logger_name="DefaultLogger"):
        """ """
        self.logger = logging.getLogger(logger_name)
        self.queue = None
        self.clear()

    def clear(self):
        self.device_index = None
        self.sampling_freq_hz = None
        self.channels = None
        self.buffer_size = None
        self.period_size = None
        self.buffer_max_size = None
        #
        self.playback_active = False
        self.playback_queue_active = False
        self.playback_executor = None
        self.buffer_int16 = None

    def get_playback_devices(self):
        """ """
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
            for device in alsaaudio.pcms(alsaaudio.PCM_PLAYBACK):
                if device.startswith("sysdefault:CARD="):
                    card_id = device.replace("sysdefault:CARD=", "").strip()
                    for card_dict in card_list:
                        if card_dict.get("card_id", "") == card_id:
                            card_dict["device"] = device
                            card_index = card_dict.get("card_index", "")
                            if card_index != "":
                                info_dict = {}
                                info_dict["device_name"] = card_dict.get(
                                    "card_name", ""
                                )
                                info_dict["output_channels"] = 1  # TODO.
                                info_dict["device_index"] = card_index

                                # print("ALSA info_dict: ", info_dict)

                                devices.append(info_dict)
        except Exception as e:
            self.logger.error(
                "AlsaAudioPlayback - get_playback_devices. Exception: " + str(e)
            )
        return devices

    def setup(
        self,
        device_index,
        channels,
        sampling_freq_hz,
        frames,
        buffer_size,
        buffer_max_size,
        in_queue_length=10,
    ):
        """ """
        self.device_index = device_index
        self.channels = channels
        self.sampling_freq_hz = sampling_freq_hz
        self.frames = frames
        self.buffer_size = buffer_size
        self.buffer_max_size = buffer_max_size
        # Setup queue for data in.
        self.queue = asyncio.Queue(maxsize=in_queue_length)

    def get_queue(self):
        """ """
        return self.queue

    async def start(self):
        """ """
        try:
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
                    self.logger.debug("AlsaAudioPlayback - Was cancelled.")
                    break
                except Exception as e:
                    message = (
                        "AlsaAudioPlayback - Exception when reading data queue: "
                        + str(e)
                    )
                    self.logger.debug(message)
        except Exception as e:
            message = "AlsaAudioPlayback - start. Exception: " + str(e)
            self.logger.debug(message)

    async def stop(self):
        """ """
        try:
            self.playback_active = False
            self.playback_queue_active = False
            if self.playback_executor != None:
                self.playback_executor.cancel()
                self.playback_executor = None
        except Exception as e:
            message = "AlsaAudioPlayback - stop. Exception: " + str(e)
            self.logger.debug(message)

    def add_data(self, data):
        """ """
        # self.logger.debug("AlsaAudioPlayback - DEBUG DATA ADDED. Length: ", len(data))
        if self.buffer_int16 is None:
            self.buffer_int16 = numpy.array([], dtype=numpy.int16)
        # Avoid to long delay.
        if len(self.buffer_int16) <= self.buffer_max_size:
            self.buffer_int16 = numpy.concatenate((self.buffer_int16, data))
        else:
            self.logger.debug(
                "AlsaAudioPlayback - SKIP. Len: " + str(self.buffer_int16.size)
            )

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
                periodsize=self.frames,
                device="sysdefault",
                cardindex=self.device_index,
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

                    #     self.logger.debug("AlsaAudioPlayback - SOUND. Len: " + str(self.buffer_int16.size))
                    # else:
                    #     if self.buffer_int16 is not None:
                    #         self.logger.debug("AlsaAudioPlayback - SILENCE. Len: " + str(self.buffer_int16.size))

                    # Convert to byte buffer and write.
                    buffer_bytes = buffer_int16.tobytes()
                    pmc_play.write(buffer_bytes)

                except asyncio.CancelledError:
                    self.logger.debug("AlsaAudioPlayback - Was cancelled.")
                    break
                except Exception as e:
                    self.logger.error(
                        "AlsaAudioPlayback - run_playback(1). Exception: " + str(e)
                    )
        #
        except asyncio.CancelledError:
            self.logger.debug("AlsaAudioPlayback - Was cancelled.")
            pass
        except Exception as e:
            self.logger.error(
                "AlsaAudioPlayback - run_playback(2). Exception: " + str(e)
            )
        finally:
            self.playback_active = False
            if pmc_play:
                pmc_play.close()
            self.logger.debug("AlsaAudioPlayback - Playback ended.")
