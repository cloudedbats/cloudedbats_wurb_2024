#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org, https://github.com/cloudedbats
# Copyright (c) 2020-present Arnold Andreasson
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import asyncio
import logging

import wurb_core


class RecManager(object):
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
        self.event_loop = asyncio.get_event_loop()
        self.rec_event = asyncio.Event()

    def clear(self):
        """ """
        self.gps_loop = None
        self.control_loop = None
        self.control_loop_interval_s = 10

    def configure(self):
        """ """
        self.control_loop_interval_s = self.config.get(
            "rec_manager.max_client_messages", self.control_loop_interval_s
        )

    def startup(self):
        """ """
        self.configure()
        wurb_core.gps.startup()
        wurb_core.wurb_scheduler.startup()
        self.gps_loop = asyncio.create_task(
            self.gps_control_loop(), name="RecManager gps-loop"
        )
        self.control_loop = asyncio.create_task(
            self.rec_control_loop(), name="RecManager gps-loop"
        )

    async def shutdown(self):
        """ """
        self.rec_event.set()
        if self.gps_loop:
            self.gps_loop.cancel()
        if self.control_loop:
            self.control_loop.cancel()

    async def rec_control_loop(self):
        """ """
        try:
            settings_event = wurb_core.wurb_settings.get_settings_event()
            location_event = wurb_core.wurb_settings.get_location_event()
            latlong_event = wurb_core.gps.get_latlong_event()
            while True:
                events = [
                    asyncio.sleep(self.control_loop_interval_s),
                    settings_event.wait(),
                    location_event.wait(),
                    latlong_event.wait(),
                ]
                await asyncio.wait(events, return_when=asyncio.FIRST_COMPLETED)

                if settings_event.is_set():
                    # await self.check_status()
                    settings_event = wurb_core.wurb_settings.get_settings_event()
                if location_event.is_set():
                    # await self.check_status()
                    location_event = wurb_core.wurb_settings.get_location_event()
                if latlong_event.is_set():
                    # await self.check_status()
                    latitude, longitude = wurb_core.gps.get_latitude_longitude()
                    await wurb_core.wurb_settings.save_latlong(latitude, longitude)
                    latlong_event = wurb_core.gps.get_latlong_event()

                await self.check_status()

        except asyncio.CancelledError:
            pass
        except Exception as e:
            # Logging error.
            message = "Rec control loop: " + str(e)
            self.logger.debug(message)
        finally:
            # Logging error.
            message = "Rec control loop terminated."
            self.logger.error(message)

    async def check_status(self):
        """ """
        try:
            is_rec_mode_on = False
            is_scheduler_used = False
            is_sound_detection_used = False
            status_info_text = ""

            # Check rec mode and scheduler.
            rec_mode = wurb_core.wurb_settings.get_setting("recMode")
            if rec_mode in ["mode-off"]:
                is_rec_mode_on = False
                is_scheduler_used = False
            elif rec_mode in ["mode-on", "mode-auto", "mode-manual"]:
                is_rec_mode_on = True
                is_scheduler_used = False
            elif rec_mode in ["mode-scheduler-on", "mode-scheduler-auto"]:
                is_rec_mode_on = True
                is_scheduler_used = True
            # Check sound detection.
            if rec_mode in ["mode-auto", "mode-scheduler-auto"]:
                is_sound_detection_used = False

            # Perform action.
            if is_rec_mode_on:
                # is_mic_available = wurb_core.wurb_recorder.is_mic_available()
                is_mic_available = True
                if is_mic_available:
                    if is_scheduler_used:
                        # check scheduler...
                        scheduler_on = wurb_core.wurb_scheduler.check_scheduler()
                        if scheduler_on:
                            status_info_text = "Rec. on by scheduler."
                            # await wurb_core.rec_manager.start_rec(
                            #     is_sound_detection_used
                            # )
                        else:
                            status_info_text = "Rec. off by scheduler."
                            # await wurb_core.rec_manager.stop_rec()
                    else:
                        status_info_text = "Rec. on."
                        # await wurb_core.rec_manager.start_rec(is_sound_detection_used)
                else:
                    status_info_text = "No microphone available."
                    # await wurb_core.rec_manager.stop_rec()
            else:
                status_info_text = "Rec. off."
                # await wurb_core.rec_manager.stop_rec()

            print("REC MANAGER: ", status_info_text)

        except Exception as e:
            # Logging error.
            message = "Scheduler update status: " + str(e)
            self.logger.error(message)

        #     is_mic_available = wurb_core.wurb_recorder.is_mic_available()
        #     if is_mic_available:
        #         rec_mode = wurb_core.wurb_settings.get_setting("recMode")
        #         self.current_mode = rec_mode

        #         if rec_mode in ["mode-on", "mode-auto", "mode-manual"]:
        #             await wurb_core.rec_manager.start_rec()

        #         elif rec_mode in ["mode-off"]:
        #             await wurb_core.rec_manager.stop_rec()

        #         elif rec_mode in ["mode-scheduler-on", "mode-scheduler-auto"]:
        #             is_schedule_active = wurb_core.wurb_scheduler.is_schedule_active()
        #             if is_schedule_active
        #                 await wurb_core.rec_manager.start_rec()
        #             else:
        #                 await wurb_core.rec_manager.stop_rec()

        #             await self.check_scheduler()
        #     else:
        #         await wurb_core.rec_manager.stop_rec()

        #     # Logging of changes in state.
        #     if self.current_mode != self.last_used_mode:
        #         mode_humans = self.user_mode_for_humans.get(
        #             self.current_mode, "Undefined"
        #         )
        #         message = "Mode: " + mode_humans
        #         self.logger.info(message)
        #         self.last_used_mode = self.current_mode
        #     if self.current_scheduler_state != self.last_used_scheduler_state:
        #         message = "Scheduler state: " + self.current_scheduler_state
        #         self.logger.info(message)
        #         self.last_used_scheduler_state = self.current_scheduler_state
        # except Exception as e:
        #     # Logging error.
        #     message = "Scheduler update status: " + str(e)
        #     self.logger.error(message)

    async def gps_control_loop(self):
        """ """
        try:
            old_number_of_satellites = 0
            # while True:
            #     latlong_event = wurb_core.gps.get_latlong_event()
            #     events = [
            #         latlong_event.wait(),
            #     ]
            #     await asyncio.wait(events, return_when=asyncio.FIRST_COMPLETED)

            #     if latlong_event.is_set():
            #         latlong_event = wurb_core.gps.get_latlong_event()

            #         # print("GPS event triggered.")
            #         lat, long = wurb_core.gps.get_latitude_longitude()
            #         number_of_satellites = wurb_core.gps.number_of_satellites
            #         if old_number_of_satellites != number_of_satellites:
            #             old_number_of_satellites = number_of_satellites
            #             print("GPS: ", lat, "  ", long, "   ", number_of_satellites)

        except Exception as e:
            message = "Rec manager: gps_control_loop: " + str(e)
            wurb_core.wurb_logger.error(message)

    def get_rec_event(self):
        """Used for synchronization."""
        return self.rec_event

    def trigger_rec_event(self):
        """Used for synchronization."""
        # Create a new event and release the old.
        old_rec_event = self.rec_event
        self.rec_event = asyncio.Event()
        old_rec_event.set()

    # def clear(self):
    #     """ """
    #     try:
    #         self.rec_status = "Not started"
    #         self.notification_event = None
    #         self.ultrasound_devices = None
    #         # self.wurb_recorder = None
    #         self.update_status_task = None
    #         self.manual_trigger_activated = False

    #     except Exception as e:
    #         print("Exception: ", e)

    # async def startup(self):
    #     """ """
    #     try:
    #         await wurb_core.gps.startup()
    #         await wurb_core.wurb_scheduler.startup()

    #         # self.wurb_logger = wurb_core.WurbLogging(self)
    #         # self.wurb_rpi = wurb_core.WurbRaspberryPi(self)
    #         # self.wurb_settings = wurb_core.WurbSettings(self)
    #         # self.wurb_audiofeedback = wurb_core.WurbPitchShifting(self)
    #         # self.ultrasound_devices = wurb_core.UltrasoundDevices(self)
    #         # self.wurb_recorder = wurb_core.WurbRecorder(self)
    #         # self.wurb_gps = wurb_core.WurbGps(self)
    #         # self.wurb_scheduler = wurb_core.WurbScheduler(self)
    #         self.update_status_task = asyncio.create_task(self.update_status())
    #         await wurb_core.wurb_logger.startup()
    #         await wurb_core.wurb_settings.startup()
    #         # await self.wurb_scheduler.startup()
    #         # await self.wurb_audiofeedback.startup()
    #         self.manual_trigger_activated = False
    #         # Logging.
    #         message = "Detector started."
    #         wurb_core.wurb_logger.info(message)
    #     except Exception as e:
    #         # Logging error.
    #         message = "Manager: startup: " + str(e)
    #         wurb_core.wurb_logger.error(message)

    # async def shutdown(self):
    #     """ """
    #     try:
    #         await self.wurb_recorder.stop_streaming(stop_immediate=True)

    #         if self.wurb_audiofeedback:
    #             await self.wurb_audiofeedback.shutdown()
    #             self.wurb_audiofeedback = None
    #         if self.wurb_gps:
    #             await self.wurb_gps.shutdown()
    #             self.wurb_gps = None
    #         if self.wurb_scheduler:
    #             await self.wurb_scheduler.shutdown()
    #             self.wurb_scheduler = None
    #         if wurb_core.wurb_settings:
    #             await wurb_core.wurb_settings.shutdown()
    #             wurb_core.wurb_settings = None
    #         if self.update_status_task:
    #             self.update_status_task.cancel()
    #             self.update_status_task = None
    #         if wurb_core.wurb_logger:
    #             await wurb_core.wurb_logger.shutdown()
    #             wurb_core.wurb_logger = None
    #     except Exception as e:
    #         # Logging error.
    #         message = "Manager: shutdown:" + str(e)
    #         wurb_core.wurb_logger.error(message)

    # async def start_rec(self):
    #     """ """
    #     try:
    #         rec_status = await self.wurb_recorder.get_rec_status()
    #         if rec_status == "Microphone is on.":
    #             return  # Already running.

    #         # await self.ultrasound_devices.stop_checking_devices()
    #         await self.ultrasound_devices.check_devices()

    #         device_name = self.ultrasound_devices.device_name
    #         card_index = self.ultrasound_devices.card_index
    #         sampling_freq_hz = self.ultrasound_devices.sampling_freq_hz
    #         if (len(device_name) > 1) and sampling_freq_hz > 0:
    #             # Audio feedback.
    #             await self.wurb_audiofeedback.set_sampling_freq(
    #                 sampling_freq=sampling_freq_hz
    #             )
    #             await self.wurb_audiofeedback.startup()
    #             # Rec.
    #             self.manual_trigger_activated = False
    #             await self.wurb_recorder.set_device(
    #                 device_name, card_index, sampling_freq_hz
    #             )
    #             await self.wurb_recorder.start_streaming()
    #             # Logging.
    #             message = "Rec. started."
    #             wurb_core.wurb_logger.info(message)
    #         else:
    #             await self.wurb_recorder.set_rec_status("Failed: No valid microphone.")
    #             # Logging.
    #             message = "Failed: No valid microphone."
    #             wurb_core.wurb_logger.info(message)
    #     except Exception as e:
    #         # Logging error.
    #         message = "Manager: start_rec: " + str(e)
    #         wurb_core.wurb_logger.error(message)

    # async def stop_rec(self):
    #     """ """
    #     try:
    #         rec_status = await self.wurb_recorder.get_rec_status()
    #         if rec_status == "Microphone is on.":
    #             # Logging.
    #             message = "Rec. stopped."
    #             wurb_core.wurb_logger.info(message)

    #         # Audio feedback.
    #         await self.wurb_audiofeedback.shutdown()
    #         # Rec.
    #         await self.wurb_recorder.set_rec_status("")
    #         await self.wurb_recorder.stop_streaming(stop_immediate=True)
    #         await self.ultrasound_devices.reset_devices()
    #     except Exception as e:
    #         # Logging error.
    #         message = "Manager: stop_rec: " + str(e)
    #         wurb_core.wurb_logger.error(message)

    # async def restart_rec(self):
    #     """ """
    #     try:
    #         rec_status = await self.wurb_recorder.get_rec_status()
    #         if rec_status == "Microphone is on.":
    #             # Logging.
    #             # message = "Rec. restart initiated."
    #             # wurb_core.wurb_logger.info(message)
    #             await self.stop_rec()
    #             await asyncio.sleep(1.0)
    #             await wurb_core.wurb_manager.start_rec()
    #     except Exception as e:
    #         # Logging error.
    #         message = "Manager: restart_rec: " + str(e)
    #         wurb_core.wurb_logger.error(message)

    # async def get_notification_event(self):
    #     """ """
    #     try:
    #         if self.notification_event == None:
    #             self.notification_event = asyncio.Event()
    #         return self.notification_event
    #     except Exception as e:
    #         # Logging error.
    #         message = "Manager: get_notification_event: " + str(e)
    #         wurb_core.wurb_logger.error(message)

    # async def get_status_dict(self):
    #     """ """
    #     try:
    #         # Avoid too long device names in the user interface.
    #         device_name = self.ultrasound_devices.device_name
    #         device_name = device_name.replace("USB Ultrasound Microphone", "")
    #         if len(device_name) > 25:
    #             device_name = device_name[:24] + "..."
    #         status_dict = {
    #             "rec_status": self.wurb_recorder.rec_status,
    #             "device_name": device_name,
    #             "sample_rate": str(self.ultrasound_devices.sampling_freq_hz),
    #         }
    #         return status_dict
    #     except Exception as e:
    #         # Logging error.
    #         message = "Manager: get_status_dict: " + str(e)
    #         wurb_core.wurb_logger.error(message)

    # async def update_status(self):
    #     """ """
    #     try:
    #         while True:
    #             try:
    #                 device_notification = (
    #                     await self.ultrasound_devices.get_notification_event()
    #                 )
    #                 rec_notification = await self.wurb_recorder.get_notification_event()
    #                 events = [
    #                     device_notification.wait(),
    #                     rec_notification.wait(),
    #                 ]
    #                 await asyncio.wait(events, return_when=asyncio.FIRST_COMPLETED)

    #                 # Create a new event and release all from the old event.
    #                 old_notification_event = self.notification_event
    #                 self.notification_event = asyncio.Event()
    #                 if old_notification_event:
    #                     old_notification_event.set()
    #             except asyncio.CancelledError:
    #                 exit
    #     except Exception as e:
    #         # Logging error.
    #         message = "Manager: update_status: " + str(e)
    #         wurb_core.wurb_logger.error(message)
    #     finally:
    #         # Logging error.
    #         message = "Manager update_status terminated."
    #         wurb_core.wurb_logger.debug(message=message)

    # async def manual_trigger(self):
    #     """ """
    #     # Will be checked and resetted in wurb_sound_detection.py
    #     self.manual_trigger_activated = True
    #     # Logging.
    #     message = "Manually triggered."
    #     wurb_core.wurb_logger.info(message)
