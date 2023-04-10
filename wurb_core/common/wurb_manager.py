#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org, https://github.com/cloudedbats
# Copyright (c) 2023-present Arnold Andreasson
# License: MIT License (see LICENSE or http://opensource.org/licenses/mit).

import asyncio
import logging

import wurb_core


class WurbManager(object):
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

    def clear(self):
        """ """
        # self.wurb_loop = None

    def configure(self):
        """ """
        # self.max_client_messages = self.config.get(
        #     "wurb_logger.max_client_messages", self.max_client_messages
        # )

    def startup(self):
        """ """
        self.configure()

        wurb_core.wurb_logger.startup()
        wurb_core.rec_manager.startup()
        # self.wurb_loop = asyncio.create_task(
        #     self.wurb_control_loop(), name="Wurb manager control loop"
        # )

    async def shutdown(self):
        """ """
        try:
            # await wurb_core.wurb_logger.shutdown()
            await wurb_core.rec_manager.shutdown()
            # if self.wurb_loop:
            #     self.wurb_loop.cancel()

            # Get a list of all running tasks.
            await asyncio.sleep(0)
            all_running_tasks = asyncio.all_tasks()
            # Remove current task from list.
            current_task = asyncio.current_task()
            all_running_tasks.remove(current_task)
            # Cancel all remaining tasks.
            self.logger.debug(
                "WurbManager shutdown. Number of remaining tasks: "
                + str(len(all_running_tasks))
            )
            for task in all_running_tasks:
                task_name = task.get_name()
                self.logger.debug("- Cancel task: " + task_name)
                task.cancel()
        except Exception as e:
            message = "WurbManager - shutdown. Exception: " + str(e)
            self.logger.debug(message)

    # async def wurb_control_loop(self):
    #     """ """
    #     try:
    #         while True:
    #             print("DEBUG wurb_manager main loop.")
    #             await asyncio.sleep(10.0)
    #     except Exception as e:
    #         message = "WurbManager - wurb_control_loop. Exception: " + str(e)
    #         self.logger.debug(message)
