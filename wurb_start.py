#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org, https://github.com/cloudedbats
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
    logger = logging.getLogger(wurb_core.used_logger)
    logger.info("\n\n")
    logger.info("Welcome to CloudedBats WURB-2023")
    logger.info("Project page: https://cloudedbats.github.io")
    logger.info("Source code: https://github.com/cloudedbats_wurb_2023")
    logger.info("======================= ^ö^ =========================")
    logger.info("")

    # WURB configuration.
    wurb_core.config.load_config(
        config_dir=settings_dir,
        config_file="wurb_config.yaml",
        config_default_dir="",
        config_default_file="wurb_config_default.yaml",
    )

    # WURB core startup.
    logger.debug("WURB startup.")
    await wurb_core.manager.startup()

    # App config.
    port = wurb_core.config.get("wurb_app.port", default="8001")
    port = int(port)
    host = wurb_core.config.get("wurb_app.host", default="0.0.0.0")
    log_level = wurb_core.config.get("wurb_app.log_level", default="info")

    logger.debug("Uvicorn startup at port: " + str(port) + ".")
    config = uvicorn.Config(
        "wurb_app:app", loop="asyncio", host=host, port=port, log_level=log_level
    )
    server = uvicorn.Server(config)
    await server.serve()

    # WURB core shutdown.
    logger.debug("WURB shutdown started.")
    wurb_core.manager.shutdown()
    logger.debug("WURB shutdown done.")


if __name__ == "__main__":
    """ """
    asyncio.run(main())
