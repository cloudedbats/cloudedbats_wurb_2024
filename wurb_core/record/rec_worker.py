#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: https://cloudedbats.github.io, https://github.com/cloudedbats
# Copyright (c) 2023-present Arnold Andreasson
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import asyncio
import logging
from collections import deque

import wurb_core


class RecWorker(object):
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
        self.source_worker = None
        self.process_worker = None
        self.target_worker = None
        self.from_source_queue = None
        self.to_target_queue = None

    def configure(self):
        """ """
        self.queue_max_size = 100
        self.rec_timeout_before_restart_s = 30
        self.max_adc_time_diff_s = 10
        self.restart_activated = False
        self.connected_device_name = ""
        self.connected_device_index = ""
        self.connected_input_channels = ""
        self.connected_sampling_freq_hz = ""

    def start_recording(self):
        """ """
        try:
            if self.from_source_queue == None:
                self.from_source_queue = asyncio.Queue(maxsize=self.queue_max_size)
                wurb_core.audio_capture.add_out_queue(self.from_source_queue)
            # else:
            #     # Clear queue.
            #     while not self.from_source_queue.empty():
            #         self.from_source_queue.get_nowait()
            #         self.from_source_queue.task_done()

            if self.to_target_queue == None:
                self.to_target_queue = asyncio.Queue(maxsize=self.queue_max_size)
            # else:
            #     # Clear queue.
            #     while not self.to_target_queue.empty():
            #         self.to_target_queue.get_nowait()
            #         self.to_target_queue.task_done()

            if self.source_worker == None:
                self.source_worker = asyncio.create_task(
                    self.rec_source_worker(), name="RecWorker source task"
                )
                self.logger.debug("REC SOURCE STARTED.")

            if self.process_worker == None:
                self.process_worker = asyncio.create_task(
                    self.rec_process_worker(), name="RecWorker process task"
                )
                self.logger.debug("REC PROCESS STARTED.")

            if self.target_worker == None:
                self.target_worker = asyncio.create_task(
                    self.rec_target_worker(), name="RecWorker target task"
                )
                self.logger.debug("REC TARGET STARTED.")
        except Exception as e:
            self.logger.debug("RecWorker, start_recording: " + str(e))

    async def stop_recording(self):
        """ """
        try:
            if self.source_worker != None:
                await wurb_core.audio_capture.stop()
                self.source_worker.cancel()
                self.source_worker = None
                self.logger.debug("REC SOURCE CANCELED.")
            if self.process_worker != None:
                self.process_worker.cancel()
                self.process_worker = None
                self.logger.debug("REC PROCESS CANCELED.")
            if self.target_worker != None:
                self.target_worker.cancel()
                self.target_worker = None
                self.logger.debug("REC TARGET CANCELED.")
        except Exception as e:
            self.logger.debug("RecWorker, stop_recording: " + str(e))

    async def rec_source_worker(self):
        """ """
        try:
            # Check available microphones.
            device_info = wurb_core.rec_devices.get_capture_device_info()
            self.connected_device_name = device_info.get("device_name", "")
            self.connected_device_index = device_info.get("device_index", "")
            self.connected_input_channels = device_info.get("input_channels", "")
            self.connected_sampling_freq_hz = device_info.get("sampling_freq_hz", "")
            if self.connected_device_index == None:
                self.logger.debug("NO MIC.")
                return
        except Exception as e:
            message = "RecWorker - rec_source_worker. Exception: " + str(e)
            self.logger.debug(message)

        # Process buffer 0.5 sec.
        process_buffer = int(float(self.connected_sampling_freq_hz) / 2)
        wurb_core.audio_capture.setup(
            device_index=self.connected_device_index,
            channels="MONO",
            sampling_freq_hz=int(self.connected_sampling_freq_hz),
            frames=int(1024 * 8),
            buffer_size=process_buffer,
        )

        await wurb_core.audio_capture.start()
        self.logger.debug("RecWorker - Sound capture started.")
        # capture_coro = wurb_core.audio_capture.start()
        # try:
        #     tasks = asyncio.gather(
        #         capture_coro,
        #     )
        #     self.gather_result = await tasks
        #     self.logger.debug("Sound capture ended: " + str(self.gather_result))
        # except Exception as e:
        #     self.logger.debug("RecWorker, rec_source_worker: " + str(e))

    async def rec_process_worker(self):
        """ """

        try:
            # Get rec length from settings.
            self.rec_length_s = int(wurb_core.wurb_settings.get_setting("recLengthS"))
            #
            self.process_deque = deque()  # Double ended queue.
            self.process_deque.clear()
            self.process_deque_length = self.rec_length_s * 2
            # self.detection_counter_max = self.process_deque_length - 3  # 1.5 s before.
            self.detection_counter_max = self.process_deque_length - 2  # 1.0 s before.
            #
            first_sound_detected = False
            sound_detected = False
            sound_detected_counter = 0

            sound_detector = wurb_core.sound_detection.get_detection()

            max_peak_freq_hz = None
            max_peak_dbfs = None

            while True:
                try:
                    try:
                        # item = await self.from_source_queue.get()
                        try:
                            item = await asyncio.wait_for(
                                self.from_source_queue.get(),
                                timeout=self.rec_timeout_before_restart_s,
                            )
                        except asyncio.TimeoutError:
                            # Check if restart already is requested.
                            if self.restart_activated:
                                return
                            # Logging.
                            message = (
                                "Lost connection with the microphone. Rec. restarted."
                            )
                            self.logger.warning(message)
                            # Restart recording.
                            self.restart_activated = True
                            loop = asyncio.get_event_loop()
                            asyncio.run_coroutine_threadsafe(
                                wurb_core.rec_manager.restart_rec(),
                                loop,
                            )
                            await self.remove_items_from_queue(self.from_source_queue)
                            await self.from_source_queue.put(False)  # Flush.
                            return
                        #
                        try:
                            # print("REC PROCESS: ", item["adc_time"], item["data"][:5])
                            if item == None:
                                first_sound_detected == False
                                sound_detected_counter = 0
                                self.process_deque.clear()
                                await self.to_target_queue.put(None)  # Terminate.
                                break
                            elif item == False:
                                first_sound_detected == False
                                sound_detected_counter = 0
                                self.process_deque.clear()
                                await self.remove_items_from_queue(self.to_target_queue)
                                await self.to_target_queue.put(False)  # Flush.
                            else:
                                # Compare real time and stream time.
                                adc_time = item["adc_time"]
                                detector_time = item["detector_time"]
                                # Restart if it differ too much.
                                if (
                                    abs(adc_time - detector_time)
                                    > self.max_adc_time_diff_s
                                ):
                                    # Check if restart already is requested.
                                    if self.restart_activated:
                                        return
                                    # Logging.
                                    message = "Warning: Time diff. detected. Rec. will be restarted."
                                    self.logger.warning(message)
                                    message = (
                                        "Warning: Time diff. ADC: "
                                        + str(adc_time)
                                        + " detector: "
                                        + str(detector_time)
                                        + "."
                                    )
                                    self.logger.debug(message)
                                    # Restart recording.
                                    self.restart_activated = True
                                    loop = asyncio.get_event_loop()
                                    asyncio.run_coroutine_threadsafe(
                                        wurb_core.rec_manager.restart_rec(),
                                        loop,
                                    )
                                    await self.remove_items_from_queue(
                                        self.from_source_queue
                                    )
                                    await self.from_source_queue.put(False)  # Flush.
                                    return

                                # Store in list-
                                new_item = {}
                                new_item["status"] = "data-Counter-" + str(
                                    sound_detected_counter
                                )
                                new_item["adc_time"] = item["adc_time"]
                                new_item["data"] = item["data"]

                                self.process_deque.append(new_item)
                                # Remove oldest items if the list is too long.
                                while (
                                    len(self.process_deque) > self.process_deque_length
                                ):
                                    self.process_deque.popleft()

                                # Check for sound.
                                detection_result = sound_detector.check_for_sound(
                                    (item["adc_time"], item["data"])
                                )
                                (
                                    sound_detected,
                                    peak_freq_hz,
                                    peak_dbfs,
                                ) = detection_result

                                if (not first_sound_detected) and sound_detected:
                                    first_sound_detected = True
                                    sound_detected_counter = 0
                                    max_peak_freq_hz = peak_freq_hz
                                    max_peak_dbfs = peak_dbfs
                                    # Log first detected sound.
                                    if max_peak_dbfs and peak_dbfs:
                                        # Logging.
                                        message = (
                                            "Sound peak: "
                                            + str(round(peak_freq_hz / 1000.0, 1))
                                            + " kHz / "
                                            + str(round(peak_dbfs, 1))
                                            + " dBFS."
                                        )
                                        self.logger.info(message)

                                # Accumulate in file queue.
                                if first_sound_detected == True:
                                    sound_detected_counter += 1
                                    if max_peak_dbfs and peak_dbfs:
                                        if peak_dbfs > max_peak_dbfs:
                                            max_peak_freq_hz = peak_freq_hz
                                            max_peak_dbfs = peak_dbfs
                                    if (
                                        sound_detected_counter
                                        >= self.detection_counter_max
                                    ) and (
                                        len(self.process_deque)
                                        >= self.process_deque_length
                                    ):
                                        first_sound_detected = False
                                        sound_detected_counter = 0
                                        # Send to target.
                                        for index in range(
                                            0, self.process_deque_length
                                        ):
                                            to_file_item = self.process_deque.popleft()
                                            #
                                            if index == 0:
                                                to_file_item["status"] = "new_file"
                                                to_file_item[
                                                    "max_peak_freq_hz"
                                                ] = max_peak_freq_hz
                                                to_file_item[
                                                    "max_peak_dbfs"
                                                ] = max_peak_dbfs
                                            if index == (self.process_deque_length - 1):
                                                to_file_item["status"] = "close_file"
                                            #
                                            if not self.to_target_queue.full():
                                                await self.to_target_queue.put(
                                                    to_file_item
                                                )
                        finally:
                            self.from_source_queue.task_done()
                            await asyncio.sleep(0)

                    except asyncio.QueueFull:
                        await self.remove_items_from_queue(self.to_target_queue)
                        self.process_deque.clear()
                        await self.to_target_queue.put(False)  # Flush.
                except asyncio.CancelledError:
                    self.logger.debug("Sound Sound process was cancelled.")
                    break
                except Exception as e:
                    message = "RecWorker - rec_process_worker(1). Exception: " + str(e)
                    self.logger.debug(message)

                await asyncio.sleep(0)
            # While end.

        except Exception as e:
            message = "RecWorker - rec_process_worker(2). Exception: " + str(e)
            self.logger.debug(message)
        finally:
            pass

    async def rec_target_worker(self):
        """Worker for sound targets. Mainly files or streams."""
        wave_file_writer = None
        try:
            while True:
                try:
                    item = await self.to_target_queue.get()
                    try:
                        if item == None:
                            # Terminated by process.
                            break
                        elif item == False:
                            await self.remove_items_from_queue(self.to_target_queue)
                            if wave_file_writer:
                                wave_file_writer.close()
                                wave_file_writer = None
                        else:
                            # New.
                            if item["status"] == "new_file":
                                if wave_file_writer:
                                    wave_file_writer.close()
                                # Create new file writer.
                                max_peak_freq_hz = item.get("max_peak_freq_hz", None)
                                max_peak_dbfs = item.get("max_peak_dbfs", None)
                                wave_file_writer = wurb_core.RecFileWriter()
                                wave_file_writer.prepare(
                                    self.connected_device_name,
                                    self.connected_sampling_freq_hz,
                                    item["adc_time"],
                                    max_peak_freq_hz,
                                    max_peak_dbfs,
                                )
                                wave_file_writer.open()
                            # Data.
                            if wave_file_writer:
                                data_array = item["data"]
                                wave_file_writer.write(data_array)
                            # File.
                            if item["status"] == "close_file":
                                if wave_file_writer:
                                    wave_file_writer.close()
                                    wave_file_writer = None
                    finally:
                        self.to_target_queue.task_done()
                        await asyncio.sleep(0)

                except asyncio.CancelledError:
                    self.logger.debug("Sound target was cancelled.")
                    break
                except Exception as e:
                    message = "RecWorker - rec_target_worker(1): " + str(e)
                    self.logger.debug(message)

                await asyncio.sleep(0)

        except Exception as e:
            message = "RecWorker - rec_target_worker(2). Exception: " + str(e)
            self.logger.debug(message)
        finally:
            pass

    async def remove_items_from_queue(self, queue):
        """Helper method."""
        try:
            while True:
                try:
                    queue.get_nowait()
                    queue.task_done()
                except asyncio.QueueEmpty:
                    return
        except Exception as e:
            message = "RecWorker - remove_items_from_queue. Exception: " + str(e)
            self.logger.debug(message)
