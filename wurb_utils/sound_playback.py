#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Main project: https://github.com/cloudedbats
# Copyright (c) 2023-present Arnold Andreasson
# License: MIT License (see LICENSE or http://opensource.org/licenses/mit).

import asyncio
import logging
import numpy


class SoundPlayback:
    """ """

    def __init__(self, audio, logger_name="DefaultLogger"):
        """ """
        self.logger = logging.getLogger(logger_name)
        self.audio = audio
        self.queue = None
        self.clear()

    def clear(self):
        self.device_index = None
        self.channels = None
        self.sampling_freq_hz = None
        self.frames = None
        self.buffer_size = None
        self.buffer_max_size = None

        self.playback_active = False
        self.playback_queue_active = False
        self.playback_executor = None
        self.buffer_int16 = None

    def get_playback_devices(self, part_of_name=None):
        """ """
        devices = []
        try:
            number_of_devices = self.audio.get_device_count()
            for index in range(number_of_devices):
                device_info = self.audio.get_device_info_by_index(index)
                device_name = device_info.get("name", "")
                output_channels = device_info.get("maxOutputChannels", "")
                if int(output_channels) > 0:
                    if part_of_name == None:
                        devices.append(device_info)
                    else:
                        if part_of_name in device_name:
                            devices.append(device_info)
        except:
            pass
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
        # Use executor for the IO-blocking part.
        event_loop = asyncio.get_event_loop()
        self.playback_executor = event_loop.run_in_executor(None, self.run_playback)
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
        # self.logger.debug("DEBUG DATA ADDED. Length: " + str(len(data)))
        if self.buffer_int16 is None:
            self.buffer_int16 = numpy.array([], dtype=numpy.int16)
        # Avoid to long delay.
        if len(self.buffer_int16) <= self.buffer_max_size:
            self.buffer_int16 = numpy.concatenate((self.buffer_int16, data))
        else:
            self.logger.debug("SKIP. Len: " + str(self.buffer_int16.size))

    def run_playback(self):
        """ """
        self.playback_active = True
        channels = 1
        if self.channels.upper() in ["STEREO", "MONO-LEFT", "MONO-RIGHT"]:
            channels = 2
        try:
            # p = pyaudio.PyAudio()
            stream = self.audio.open(
                format=self.audio.get_format_from_width(2),
                channels=channels,
                rate=self.sampling_freq_hz,
                input=False,
                output=True,
                output_device_index=self.device_index,
                frames_per_buffer=self.frames,
            )
            # To be used when no data in buffer.
            silent_buffer = numpy.zeros((self.frames, 1), dtype=numpy.float16)
            # Loop over the IO blocking part.
            while self.playback_active:
                try:
                    # Use silent buffer as default.
                    buffer_int16 = silent_buffer
                    #
                    if (self.buffer_int16 is not None) and (
                        self.buffer_int16.size >= self.frames
                    ):
                        # Copy part to be used.
                        buffer_int16 = self.buffer_int16[: self.frames]
                        # Remove used part.
                        self.buffer_int16 = self.buffer_int16[self.frames :]

                    #     self.logger.debug("SOUND. Len: " + str(self.buffer_int16.size))
                    # else:
                    #     if self.buffer_int16 is not None:
                    #         self.logger.debug("SILENCE. Len: " + str(self.buffer_int16.size))

                    # Convert to byte buffer and write.
                    buffer_bytes = buffer_int16.tobytes()
                    stream.write(buffer_bytes, exception_on_underflow=False)

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
            stream.close()
            # p.terminate()
            self.logger.debug("PLAYBACK ENDED.")
