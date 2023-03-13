#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org, https://github.com/cloudedbats
# Copyright (c) 2023-present Arnold Andreasson
# License: MIT License (see LICENSE or http://opensource.org/licenses/mit).

import asyncio
import logging


class AppManager(object):
    """ """

    def __init__(self, logger="DefaultLogger"):
        """ """
        self.logger_name = logger
        self.logger = logging.getLogger(logger)

    async def startup(self):
        """ """
        #

    def shutdown(self):
        """ """
        # Get a list of all running tasks.
        all_running_tasks = asyncio.all_tasks()
        # Remove current task.
        current_task = asyncio.current_task()
        all_running_tasks.remove(current_task)
        # Cancel all remaining tasks.
        self.logger.debug(
            "WurbManager shutdown. Number of tasks: " + str(len(all_running_tasks))
        )
        for task in all_running_tasks:
            task_name = task.get_name()
            self.logger.debug("- Cancel task: " + task_name)
            task.cancel()
