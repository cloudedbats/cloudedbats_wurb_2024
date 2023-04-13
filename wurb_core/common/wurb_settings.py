#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org, https://github.com/cloudedbats
# Copyright (c) 2023-present Arnold Andreasson
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import asyncio
import logging
import pathlib
import yaml

import wurb_core


class WurbSettings(object):
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
        self.loaded_settings = {}
        self.default_settings = None
        self.default_location = None
        self.current_settings = None
        self.current_location = None
        self.settings_dir = ""
        self.settings_event = None
        self.location_event = None
        self.latlong_event = None
        self.audiofeedback_event = None

    def configure(self):
        """ """
        self.settings_header_rows = ["# Settings for CloudedBats WURB-2023.", "---"]

    async def startup(self, settings_dir):
        """ """
        try:
            # Settings file and defaults.
            self.settings_file_name = "wurb_settings.yaml"
            self.define_default_settings()
            self.define_default_location()
            # Load.
            self.settings_dir = settings_dir
            self.load_settings_from_file()
            # Select settings for startup.
            startup_option = self.loaded_settings.get("startupOption", "")
            if startup_option == "startup-settings":
                self.current_settings = self.loaded_settings["startupSettings"].copy()
                self.current_location = self.loaded_settings["startupLocation"].copy()
            else:
                self.current_settings = self.loaded_settings["currentSettings"].copy()
                self.current_location = self.loaded_settings["currentLocation"].copy()
            # GPS.
            await self.save_latlong(0.0, 0.0)
        except Exception as e:
            message = "WurbSettings - startup. Exception: " + str(e)
            self.logger.debug(message)

    async def shutdown(self):
        """ """
        try:
            # Release events.
            if self.settings_event:
                self.settings_event.set()
            if self.location_event:
                self.location_event.set()
            if self.latlong_event:
                self.latlong_event.set()
            if self.audiofeedback_event:
                self.audiofeedback_event.set()
        except Exception as e:
            message = "WurbSettings - shutdown. Exception: " + str(e)
            self.logger.debug(message)

    def define_default_settings(self):
        """ """
        self.default_settings = {
            "recMode": "mode-off",
            "fileDirectory": "Station-1",
            "fileDirectoryDateOption": "date-post-before",
            "filenamePrefix": "wurb",
            "detectionLimitKhz": 17.0,
            "detectionSensitivityDbfs": -50,
            "detectionAlgorithm": "detection-simple",
            "recLengthS": 5,
            "recType": "FS",
            "feedbackOnOff": "feedback-off",
            "feedbackVolume": 50,
            "feedbackPitch": 30,
            "feedbackFilterLowKhz": 15,
            "feedbackFilterHighKhz": 150,
            "startupOption": "as-last-session",
            "schedulerStartEvent": "on-sunset",
            "schedulerStartAdjust": -15,
            "schedulerStopEvent": "off-sunrise",
            "schedulerStopAdjust": 15,
            "schedulerPostAction": "post-none",
            "schedulerPostActionDelay": 5,
        }

    def define_default_location(self):
        """ """
        self.default_location = {
            "geoSource": "geo-not-used",
            "latitudeDd": 0.0,
            "longitudeDd": 0.0,
            "manualLatitudeDd": 0.0,
            "manualLongitudeDd": 0.0,
            "lastGpsLatitudeDd": 0.0,
            "lastGpsLongitudeDd": 0.0,
        }

    async def save_settings(self, settings_dict={}, settings_type=None):
        """ """
        try:
            is_changed = False
            for key, value in settings_dict.items():
                if value is not None:
                    # Clean up filename_prefix.
                    if key == "filenamePrefix":
                        value = value.replace(" ", "-")
                        value = value.replace("_", "-")
                    #
                    old_value = self.current_settings.get(key, "")
                    self.current_settings[key] = value
                    #
                    try:
                        if str(old_value) != str(value):
                            is_changed = True
                            # Logging.
                            message = (
                                "Settings changed: "
                                + str(key)
                                + " from: "
                                + str(old_value)
                                + " to: "
                                + str(value)
                            )
                            self.logger.debug(message)
                    except Exception as e:
                        # Logging.
                        message = "Error when comparing saved settings. " + str(e)
                        self.logger.debug(message)

            # Copy startupOption to top level.
            startupOption = settings_dict.get("startupOption", "")
            self.loaded_settings["startupOption"] = startupOption

            if is_changed:
                self.loaded_settings["currentSettings"] = self.current_settings.copy()
                self.save_settings_to_file()
                # Trigger an event.
                self.trigger_settings_event()
                #
                message = "Settings saved."
                self.logger.info(message)

            if settings_type is not None:
                if settings_type == "user-default":
                    self.loaded_settings["userSettings"] = self.current_settings.copy()
                    self.loaded_settings["userLocation"] = self.current_location.copy()
                    self.save_settings_to_file()
                if settings_type == "startup":
                    self.loaded_settings[
                        "startupSettings"
                    ] = self.current_settings.copy()
                    self.loaded_settings[
                        "startupLocation"
                    ] = self.current_location.copy()
                    self.save_settings_to_file()
        except Exception as e:
            message = "WurbSettings - save_settings. Exception: " + str(e)
            self.logger.debug(message)

    def get_setting(self, key=None):
        """ """
        if key:
            return self.current_settings.get(key, "")
        return ""

    def set_setting_without_saving(self, key=None, value=""):
        """ """
        if key:
            self.current_settings[key] = value

    async def get_settings(self, default=False):
        """ """
        try:
            if default:
                return self.default_settings
            return self.current_settings
        except Exception as e:
            message = "WurbSettings - get_settings. Exception: " + str(e)
            self.logger.debug(message)

    async def save_location(self, location_dict={}):
        """ """
        try:
            for key, value in location_dict.items():
                if value is not None:
                    self.current_location[key] = value

            geo_source = self.current_location["geoSource"]
            # Manual.
            if geo_source == "geo-manual":
                self.current_location["latitudeDd"] = self.current_location[
                    "manualLatitudeDd"
                ]
                self.current_location["longitudeDd"] = self.current_location[
                    "manualLongitudeDd"
                ]
            # GPS.
            if geo_source in ["geo-gps", "geo-gps-or-manual", "geo-last-gps-or-manual"]:
                self.current_location["latitudeDd"] = 0.0
                self.current_location["longitudeDd"] = 0.0

            self.loaded_settings["currentLocation"] = self.current_location.copy()

            self.save_settings_to_file()
            # Trigger an event.
            self.trigger_location_event()
        except Exception as e:
            message = "WurbSettings - save_location. Exception: " + str(e)
            self.logger.debug(message)

    async def save_latlong(self, latitude_dd, longitude_dd):
        """ """
        try:
            geo_source = self.current_location["geoSource"]
            # Manual.
            if geo_source in ["geo-gps", "geo-gps-or-manual", "geo-last-gps-or-manual"]:
                self.current_location["latitudeDd"] = latitude_dd
                self.current_location["longitudeDd"] = longitude_dd
                if (latitude_dd > 0.0) and (longitude_dd > 0.0):
                    self.current_location["lastGpsLongitudeDd"] = latitude_dd
                    self.current_location["lastGpsLongitudeDd"] = longitude_dd

            self.loaded_settings["currentLocation"] = self.current_location.copy()
            self.save_settings_to_file()

            # Trigger an event.
            self.trigger_latlong_event()
        except Exception as e:
            message = "WurbSettings - save_latlong. Exception: " + str(e)
            self.logger.debug(message)

    def get_valid_location(self):
        """ """
        latitude = 0.0
        longitude = 0.0
        location_dict = self.get_location_dict()
        latitude = float(location_dict.get("latitudeDd", "0.0"))
        longitude = float(location_dict.get("longitudeDd", "0.0"))
        manual_latitude = float(location_dict.get("manualLatitudeDd", "0.0"))
        manual_longitude = float(location_dict.get("manualLongitudeDd", "0.0"))
        last_gps_latitude = float(location_dict.get("lastGpsLongitudeDd", "0.0"))
        last_gps_longitude = float(location_dict.get("lastGpsLongitudeDd", "0.0"))
        geo_source = location_dict.get("geoSource", "")
        if (latitude == 0.0) or (longitude == 0.0):
            if geo_source in ["geo-gps-or-manual"]:
                latitude = manual_latitude
                longitude = manual_longitude
        if (latitude == 0.0) or (longitude == 0.0):
            if geo_source in ["geo-last-gps-or-manual"]:
                latitude = last_gps_latitude
                longitude = last_gps_longitude
                if (latitude == 0.0) or (longitude == 0.0):
                    latitude = manual_latitude
                    longitude = manual_longitude
        # Result.
        return latitude, longitude

    def get_location_status(self):
        """ """
        lat, long = self.get_valid_location()
        if (lat == 0.0) and (long == 0.0):
            return "Not valid. Scheduler not started."
        else:
            geo_source = self.get_location_dict().get("geoSource", "")
            if geo_source == "geo-gps":
                if wurb_core.gps_reader:
                    no_of_satellites = wurb_core.gps_reader.get_number_of_satellites()
                    return "Number of satellites: " + str(no_of_satellites)
            else:
                return "Lat: " + str(lat) + " Long: " + str(long)

    def get_location_dict(self):
        """ """
        return self.current_location

    async def get_location(self):
        """ """
        try:
            return self.current_location
        except Exception as e:
            message = "WurbSettings - get_location. Exception: " + str(e)
            self.logger.debug(message)

    async def set_audio_feedback(self, volume, pitch):
        """ """
        try:
            self.current_settings["feedbackVolume"] = volume
            self.current_settings["feedbackPitch"] = pitch
            # audiofeedback = wurb_core.wurb_audiofeedback
            # if audiofeedback:
            #     await audiofeedback.set_volume(volume)
            #     await audiofeedback.set_pitch(pitch)
            # Trigger an event.
            self.trigger_audiofeedback_event()
        except Exception as e:
            message = "WurbSettings - set_audio_feedback. Exception: " + str(e)
            self.logger.debug(message)

    def trigger_settings_event(self):
        """ """
        # Event: Create a new and release the old.
        old_event = self.get_settings_event()
        self.settings_event = asyncio.Event()
        old_event.set()

    def get_settings_event(self):
        """ """
        if self.settings_event == None:
            self.settings_event = asyncio.Event()
        return self.settings_event

    def trigger_location_event(self):
        """ """
        # Event: Create a new and release the old.
        old_event = self.get_location_event()
        self.location_event = asyncio.Event()
        old_event.set()

    def get_location_event(self):
        """ """
        if self.location_event == None:
            self.location_event = asyncio.Event()
        return self.location_event

    def trigger_latlong_event(self):
        """ """
        # Event: Create a new and release the old.
        old_event = self.get_latlong_event()
        self.latlong_event = asyncio.Event()
        old_event.set()

    def get_latlong_event(self):
        """ """
        if self.latlong_event == None:
            self.latlong_event = asyncio.Event()
        return self.latlong_event

    def trigger_audiofeedback_event(self):
        """ """
        # Event: Create a new and release the old.
        old_event = self.get_audiofeedback_event()
        self.audiofeedback_event = asyncio.Event()
        old_event.set()

    def get_audiofeedback_event(self):
        """ """
        if self.audiofeedback_event == None:
            self.audiofeedback_event = asyncio.Event()
        return self.audiofeedback_event

    async def load_settings(self, settings_type):
        """ """
        try:
            if settings_type == "user-default":
                self.current_settings = self.loaded_settings["userSettings"].copy()
                self.current_location = self.loaded_settings["userLocation"].copy()
            elif settings_type == "start-up":
                self.current_settings = self.loaded_settings["startupSettings"].copy()
                self.current_location = self.loaded_settings["startupLocation"].copy()
            elif settings_type == "factory-default":
                self.current_settings = self.default_settings.copy()
                self.current_location = self.default_location.copy()

            # Copy startupOption to top level.
            startupOption = self.current_settings.get("startupOption", "")
            self.loaded_settings["startupOption"] = startupOption

            # Trigger an event.
            self.trigger_settings_event()
            self.trigger_location_event()
        except Exception as e:
            message = "WurbSettings - load_settings. Exception: " + str(e)
            self.logger.debug(message)

    def load_settings_from_file(self, settings_file_name=None):
        """Load from file."""
        if settings_file_name is None:
            settings_file_name = self.settings_file_name
        settings_file_path = pathlib.Path(self.settings_dir, settings_file_name)
        if settings_file_path.exists():
            with open(settings_file_path) as settings_file:
                self.loaded_settings = yaml.safe_load(settings_file)
        else:
            # Use
            self.loaded_settings["startupOption"] = "as-last-session"
            self.loaded_settings["currentSettings"] = self.default_settings.copy()
            self.loaded_settings["startupSettings"] = self.default_settings.copy()
            self.loaded_settings["userSettings"] = self.default_settings.copy()
            self.loaded_settings["currentLocation"] = self.default_location.copy()
            self.loaded_settings["startupLocation"] = self.default_location.copy()
            self.loaded_settings["userLocation"] = self.default_location.copy()
            self.save_settings_to_file()

    def save_settings_to_file(self):
        """Save to file."""
        settings_file_path = pathlib.Path(self.settings_dir, self.settings_file_name)
        with settings_file_path.open("w") as settings_file:
            settings_file.writelines("\n".join(self.settings_header_rows) + "\n")
            data = self.loaded_settings
            yaml.safe_dump(data, settings_file)
