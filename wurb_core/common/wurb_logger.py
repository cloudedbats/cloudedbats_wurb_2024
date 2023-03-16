#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org, https://github.com/cloudedbats
# Copyright (c) 2020-present Arnold Andreasson
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import asyncio
import datetime
import logging
from logging import handlers


class WurbLogger(object):
    """ """

    def __init__(self, config=None, logger_name="DefaultLogger"):
        """ """
        if config == None:
            self.config = {}
        else:
            self.config = config
        self.logger = logging.getLogger(logger_name)
        #
        self.clear()
        self.event_loop = asyncio.get_event_loop()
        self.logging_event = asyncio.Event()

    def clear(self):
        """ """
        self.client_messages = []
        self.max_client_messages = 10

    def configure(self):
        """ """
        self.max_client_messages = self.config.get(
            "wurb_logger.max_client_messages", self.max_client_messages
        )

    def startup(self):
        """ """
        self.configure()

    def shutdown(self):
        """ """
        self.logging_event.set()

    def info(self, message):
        """ """
        self.logger.info(message)
        self.write_log("info", message)

    def warning(self, message):
        """ """
        self.logger.warning(message)
        self.write_log("warning", message)

    def error(self, message):
        """ """
        self.logger.error(message)
        self.write_log("error", message)

    def debug(self, message):
        """ """
        self.logger.debug(message)
        # self.write_log("debug", message)

    def write_log(self, msg_type, message):
        """ """
        # Run the rest in the main asyncio event loop.
        datetime_local = datetime.datetime.now()
        asyncio.run_coroutine_threadsafe(
            self.write_log_async(msg_type, datetime_local, message),
            self.event_loop,
        )

    async def write_log_async(self, msg_type, datetime_local, message):
        """ """
        try:
            time_str = datetime_local.strftime("%H:%M:%S")
            # datetime_str = datetime_local.strftime("%Y-%m-%d %H:%M:%S%z")
            if message:
                if msg_type in ["info", "warning", "error"]:
                    if msg_type in ["warning", "error"]:
                        self.client_messages.append(
                            time_str + " - " + msg_type.capitalize() + ": " + message
                        )
                    else:
                        self.client_messages.append(time_str + " - " + message)
                    # Log list too large. Remove oldest item.
                    if len(self.client_messages) > self.max_client_messages:
                        del self.client_messages[0]
                    # Trigger an event.
                    self.trigger_logging_event()
        except Exception as e:
            # Can't log this, must use print.
            print("Exception: Logging: write_log_async: ", e)

    async def trigger_logging_event(self):
        """ """
        # Event: Create a new and release the old.
        old_event = self.logging_event
        self.logging_event = asyncio.Event()
        old_event.set()

    async def get_logging_event(self):
        """ """
        return self.logging_event

    async def get_client_messages(self):
        """ """
        return self.client_messages[::-1]
