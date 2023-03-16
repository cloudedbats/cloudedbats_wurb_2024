#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: https://cloudedbats.github.io, 
# Copyright (c) 2023-present Arnold Andreasson
# License: MIT License (see LICENSE or http://opensource.org/licenses/mit).

import asyncio
import uvicorn
import logging
import wurb_core


async def main():
    """ """
    # logging_dir = "../wurb_logging"
    # settings_dir = "../wurb_settings"
    # Used during development:
    logging_dir = "DEV_wurb_logging"
    settings_dir = "DEV_wurb_settings"

    # WURB logger.
    wurb_core.logger.setup_rotating_log(
        logging_dir=logging_dir,
        log_name="info_log.txt",
        debug_log_name="debug_log.txt",
    )
    logger_name = wurb_core.logger.get_logger_name()
    logger = logging.getLogger(logger_name)
    logger.info("\n\n")
    logger.info("Welcome to CloudedBats WURB-2023")
    logger.info("Project: https://cloudedbats.github.io")
    logger.info("================ ^ö^ =================")
    logger.info("")

    # WURB configuration.
    wurb_core.config.load_config(
        config_dir=settings_dir,
        config_file="wurb_config.yaml",
        config_default_dir="",
        config_default_file="wurb_config_default.yaml",
    )

    # WURB settings.
    wurb_core.wurb_settings.load_settings(
        settings_dir=settings_dir,
        # settings_file="wurb_settings.yaml",
    )

    # WURB core startup.
    logger.debug("WURB startup.")
    wurb_core.wurb_manager.startup()
    await asyncio.sleep(0)

    # API and App config.
    port = wurb_core.config.get("wurb_app.port", default="8080")
    port = int(port)
    host = wurb_core.config.get("wurb_app.host", default="0.0.0.0")
    log_level = wurb_core.config.get("wurb_app.log_level", default="info")

    logger.debug("Uvicorn startup at port: " + str(port) + ".")
    config = uvicorn.Config(
        "wurb_api:app", loop="asyncio", host=host, port=port, log_level=log_level
    )

    # WURB startup.
    server = uvicorn.Server(config)
    await server.serve()

    # WURB shutdown.
    logger.debug("WURB shutdown started.")
    await wurb_core.wurb_manager.shutdown()
    logger.debug("WURB shutdown done.")


if __name__ == "__main__":
    """ """
    asyncio.run(main())
