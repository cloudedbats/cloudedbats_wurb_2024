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
        self.rec_event = None
        self.notification_event = None

    def clear(self):
        """ """
        self.gps_loop = None
        self.control_loop = None
        self.control_loop_interval_s = 10
        self.last_used_rec_mode = ""
        self.manual_trigger_activated = False
        self.status_info_text = ""

    def configure(self):
        """ """
        self.control_loop_interval_s = self.config.get(
            "rec_manager.max_client_messages", self.control_loop_interval_s
        )

    def startup(self):
        """ """
        self.configure()

        wurb_core.gps.startup()
        self.gps_loop = asyncio.create_task(
            self.gps_control_loop(), name="RecManager gps task"
        )
        self.control_loop = asyncio.create_task(
            self.rec_control_loop(), name="RecManager control task"
        )

    def shutdown(self):
        """ """
        wurb_core.gps.shutdown()
        if self.rec_event:
            self.rec_event.set()
        if self.notification_event:
            self.notification_event.set()
        if self.gps_loop:
            self.gps_loop.cancel()
        if self.control_loop:
            self.control_loop.cancel()

    async def rec_control_loop(self):
        """ """
        try:
            self.manual_trigger_activated = False
            await self.check_status()

            settings_event = wurb_core.wurb_settings.get_settings_event()
            location_event = wurb_core.wurb_settings.get_location_event()
            latlong_event = wurb_core.gps.get_latlong_event()
            while True:
                task_1 = asyncio.create_task(asyncio.sleep(self.control_loop_interval_s), name="debug-7")
                task_2 = asyncio.create_task(settings_event.wait(), name="debug-8")
                task_3 = asyncio.create_task(location_event.wait(), name="debug-9")
                task_4 = asyncio.create_task(latlong_event.wait(), name="debug-10")
                events = [
                    task_1,
                    task_2,
                    task_3,
                    task_4,
                ]
                done, pending = await asyncio.wait(events, return_when=asyncio.FIRST_COMPLETED)
                for task in done:
                    task.cancel()
                    # print("Done REC: ", task.get_name())
                for task in pending:
                    task.cancel()

                if settings_event.is_set():
                    settings_event = wurb_core.wurb_settings.get_settings_event()
                if location_event.is_set():
                    location_event = wurb_core.wurb_settings.get_location_event()
                if latlong_event.is_set():
                    latitude, longitude = wurb_core.gps.get_latitude_longitude()
                    print("Lat-long: ", latitude, "   ", longitude)
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
            is_rec_to_be_activated = False
            self.status_info_text = ""

            # Check rec mode and scheduler.
            rec_mode = wurb_core.wurb_settings.get_setting("recMode")

            if rec_mode != self.last_used_rec_mode:
                self.last_used_rec_mode = rec_mode
                wurb_core.rec_worker.stop_recording()

            if rec_mode in ["mode-off"]:
                is_rec_mode_on = False
                is_scheduler_used = False
            elif rec_mode in ["mode-on", "mode-auto", "mode-manual"]:
                is_rec_mode_on = True
                is_scheduler_used = False
            elif rec_mode in ["mode-scheduler-on", "mode-scheduler-auto"]:
                is_rec_mode_on = True
                is_scheduler_used = True

            # Perform action.
            if is_rec_mode_on:
                is_mic_available = wurb_core.rec_devices.is_mic_available()
                if is_mic_available:
                    if is_scheduler_used:
                        # Check scheduler...
                        scheduler_on = wurb_core.rec_scheduler.check_scheduler()
                        if scheduler_on:
                            is_rec_to_be_activated = True
                            self.status_info_text = "Recording on by scheduler."
                        else:
                            is_rec_to_be_activated = False
                            self.status_info_text = "Recording off by scheduler."
                            # await wurb_core.rec_manager.stop_rec()
                    else:
                        is_rec_to_be_activated = True
                        self.status_info_text = "Recording on."
                else:
                    is_rec_to_be_activated = False
                    self.status_info_text = "No microphone available."
                    # await wurb_core.rec_manager.stop_rec()
            else:
                is_rec_to_be_activated = False
                self.status_info_text = "Recording off."
                # await wurb_core.rec_manager.stop_rec()

            print("REC MANAGER: ", self.status_info_text)

            if is_rec_to_be_activated:
                wurb_core.rec_worker.start_recording()
            else:
                wurb_core.rec_worker.stop_recording()




            self.trigger_notification_event()





        except Exception as e:
            # Logging error.
            message = "Scheduler update status: " + str(e)
            self.logger.error(message)

    async def gps_control_loop(self):
        """ """
        try:
            old_number_of_satellites = 0
            # while True:
            #     latlong_event = wurb_core.gps.get_latlong_event()
            #     events = [
            #         asyncio.create_task(latlong_event.wait(), name="debug-12"),
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
            self.logger.error(message)

    def get_rec_event(self):
        """Used for synchronization."""
        if self.rec_event == None:
            self.rec_event = asyncio.Event()
        return self.rec_event

    def trigger_rec_event(self):
        """Used for synchronization."""
        # Create a new event and release the old.
        old_rec_event = self.get_rec_event()
        self.rec_event = asyncio.Event()
        old_rec_event.set()

    def get_notification_event(self):
        """Used for synchronization."""
        if self.notification_event == None:
            self.notification_event = asyncio.Event()
        return self.notification_event

    def trigger_notification_event(self):
        """Used for synchronization."""
        # Create a new event and release the old.
        old_notification_event = self.get_notification_event()
        self.notification_event = asyncio.Event()
        old_notification_event.set()

    async def restart_rec(self):
        """ """
        try:
            wurb_core.rec_worker.stop_recording()
            await asyncio.sleep(1.0)
            await self.check_status()
        except Exception as e:
            # Logging error.
            message = "Manager: restart_rec: " + str(e)
            self.logger.error(message)

    async def get_status_dict(self):
        """ """
        try:
            # status_dict = {
            #     "rec_status": "TEST-STATUS",
            #     "device_name": "TEST-DEV",
            #     "sample_rate": "1234556",
            # }
            # return(status_dict)

            # Avoid too long device names in the user interface.
            device_name = wurb_core.rec_worker.get_connected_device_name()
            device_freq_hz = wurb_core.rec_worker.get_connected_device_freq_hz()
            device_name = device_name.replace("USB Ultrasound Microphone", "")
            if len(device_name) > 25:
                device_name = device_name[:24] + "..."
            status_dict = {
                "rec_status": self.status_info_text,
                "device_name": device_name,
                "sample_rate": str(device_freq_hz),
                # "rec_status": self.wurb_recorder.rec_status,
                # "device_name": device_name,
                # "sample_rate": str(self.ultrasound_devices.sampling_freq_hz),
            }
            return status_dict
        except Exception as e:
            # Logging error.
            message = "Manager: get_status_dict: " + str(e)
            self.logger.error(message)

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

    #                 # Trigger event.
    #                 self.trigger_notification_event()
    #             except asyncio.CancelledError:
    #                 exit
    #     except Exception as e:
    #         # Logging error.
    #         message = "Manager: update_status: " + str(e)
    #         self.logger.error(message)
    #     finally:
    #         # Logging error.
    #         message = "Manager update_status terminated."
    #         self.logger.debug(message=message)

    async def manual_trigger(self):
        """ """
        # Will be checked and resetted in wurb_sound_detection.py.
        self.manual_trigger_activated = True
        # Logging.
        message = "Manually triggered."
        self.logger.info(message)
