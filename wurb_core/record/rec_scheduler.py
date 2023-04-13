#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org, https://github.com/cloudedbats
# Copyright (c) 2023-present Arnold Andreasson
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import asyncio
import logging
import datetime

import wurb_core


class WurbScheduler(object):
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
        self.solartime_lookup_dict = {}
        self.solartime_last_used_key = ""

    def configure(self):
        """ """
        # self.max_client_messages = self.config.get(
        #     "rec_scheduler.main_loop_interval_s", self.main_loop_interval_s
        # )

    def check_scheduler(self):
        """ """
        is_rec_active = False
        # Start/stop time.
        start_event_local, stop_event_local = self.calculate_start_stop()
        if (start_event_local is None) or (stop_event_local is None):
            # Can't calculate start or stop.
            self.current_scheduler_state = "Time or position is missing."
            # await wurb_core.rec_manager.stop_rec()
            is_rec_active = False
            return is_rec_active

        # Evaluate action.
        now_local = datetime.datetime.now().astimezone()
        if start_event_local == stop_event_local:
            # Always off.
            # await wurb_core.rec_manager.stop_rec()
            is_rec_active = False
        elif start_event_local < stop_event_local:
            # Same day.
            if (start_event_local < now_local) and (now_local < stop_event_local):
                self.current_scheduler_state = "Recording active."
                # await wurb_core.rec_manager.start_rec()
                is_rec_active = True
            else:
                self.current_scheduler_state = "Recording not active."
                # await wurb_core.rec_manager.stop_rec()
                is_rec_active = False
        else:
            # Different days.
            start_local_new = start_event_local
            stop_local_new = stop_event_local
            # Prepare.
            if now_local < stop_event_local:
                start_local_new = start_event_local - datetime.timedelta(days=1)
            if now_local > stop_event_local:
                stop_local_new = stop_event_local + datetime.timedelta(days=1)
            # Check.
            if (start_local_new < now_local) and (now_local < stop_local_new):
                self.current_scheduler_state = "Recording active."
                # await wurb_core.rec_manager.start_rec()
                is_rec_active = True
            else:
                self.current_scheduler_state = "Recording not active."
                # await wurb_core.rec_manager.stop_rec()
                is_rec_active = False

        return is_rec_active

    def calculate_start_stop(self):
        """ """
        # Get settings.
        start_event = wurb_core.wurb_settings.get_setting("schedulerStartEvent")
        start_event_adjust = wurb_core.wurb_settings.get_setting("schedulerStartAdjust")
        stop_event = wurb_core.wurb_settings.get_setting("schedulerStopEvent")
        stop_event_adjust = wurb_core.wurb_settings.get_setting("schedulerStopAdjust")
        # Get sunset, sunrise, etc.
        solartime_dict = self.get_solartime_data()
        # Start event.
        if start_event in ["on-sunset", "on-dusk", "on-dawn", "on-sunrise"]:
            if not solartime_dict:
                # Lat/long needed to calculate start.
                return (None, None)
            start_event = start_event.replace("on-", "") + "_utc"
            start_event_utc = solartime_dict.get(start_event, None)
            start_event_local = start_event_utc.astimezone()
        else:
            start_event = start_event.replace("on-", "") + "_utc"
            start_event_hour = int(float(start_event))
            start_event_local = datetime.datetime.now().astimezone()
            start_event_local = start_event_local.replace(
                hour=start_event_hour, minute=0, second=0, microsecond=0
            )
        # Stop event.
        if stop_event in ["off-sunset", "off-dusk", "off-dawn", "off-sunrise"]:
            if not solartime_dict:
                # Lat/long needed to calculate stop.
                return (None, None)
            stop_event = stop_event.replace("off-", "") + "_utc"
            stop_event_utc = solartime_dict.get(stop_event, None)
            stop_event_local = stop_event_utc.astimezone()
        else:
            stop_event = stop_event.replace("off-", "") + "_utc"
            stop_event_hour = int(float(stop_event))
            stop_event_local = datetime.datetime.now().astimezone()
            stop_event_local = stop_event_local.replace(
                hour=stop_event_hour, minute=0, second=0, microsecond=0
            )
        # Adjust time.
        start_event_local += datetime.timedelta(minutes=int(float(start_event_adjust)))
        stop_event_local += datetime.timedelta(minutes=int(float(stop_event_adjust)))

        return (start_event_local, stop_event_local)

    def get_solartime_data(self, print_new=True):
        """ """
        latitude, longitude = wurb_core.wurb_settings.get_valid_location()
        if (latitude == 0.0) or (longitude == 0.0):
            # No lat/long found.
            return None

        date_local = datetime.datetime.now().date()
        latitude_short = round(latitude, 2)
        longitude_short = round(longitude, 2)
        solartime_dict = {}
        lookup_key = (
            str(date_local) + "<->" + str(latitude_short) + "<->" + str(longitude_short)
        )
        if lookup_key in self.solartime_lookup_dict:
            sun_moon_dict = self.solartime_lookup_dict.get(lookup_key, {})
        else:
            # solartime_dict = self.solartime.sun_utc(date_local, latitude, longitude)
            sun_moon_dict = wurb_core.sun_moon.get_sun_moon_info(latitude, longitude)
            self.solartime_lookup_dict[lookup_key] = sun_moon_dict

        if lookup_key != self.solartime_last_used_key:
            self.solartime_last_used_key = lookup_key
            # Logging.
            sunset_utc = sun_moon_dict.get("sunset", None)
            dusk_utc = sun_moon_dict.get("dusk", None)
            dawn_utc = sun_moon_dict.get("dawn", None)
            sunrise_utc = sun_moon_dict.get("sunrise", None)
            if sunset_utc and dusk_utc and dawn_utc and sunrise_utc:
                if print_new:
                    sunset_local = sunset_utc.astimezone()
                    dusk_local = dusk_utc.astimezone()
                    dawn_local = dawn_utc.astimezone()
                    sunrise_local = sunrise_utc.astimezone()
                    message = "Solartime recalculated: "
                    message += " Sunset: " + sunset_local.strftime("%H:%M:%S")
                    message += " Dusk: " + dusk_local.strftime("%H:%M:%S")
                    message += " Dawn: " + dawn_local.strftime("%H:%M:%S")
                    message += " Sunrise: " + sunrise_local.strftime("%H:%M:%S")
                    self.logger.info(message)
            else:
                return None

        return sun_moon_dict
