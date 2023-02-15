#!/usr/bin/python3
# -*- coding:utf-8 -*-

import asyncio
import uvicorn
import logging
import wurb_core

import pathlib


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
    logger.info("Welcome to TEST")
    logger.info("===============")
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





    ### FOR TEST - START ###
    print("TEST started.")

    print("")
    sources = wurb_core.sources_and_files.get_rec_sources()
    for source in sources:
        print("")
        print("Source: ", str(source))
        nights = wurb_core.sources_and_files.get_rec_nights(source)
        for night in nights:
            print("")
            print("Night: ", str(night))
            # sound_files = wurb_core.sources_and_files.get_rec_files(night)
            # for sound_file in sound_files:
            #     print("File: ", str(sound_file))
    print("")

    rec_file = "../wurb_recordings/Taberg-1_2022-12-01/w53u384_20221201T200355+0100_N57.67687E14.0827_TE384_24kHz-39dB.wav"
    metadata = wurb_core.metadata_rec.read_metadata(rec_file)
    metadata["annotations"][0] = {
            "user": "wurb-user",
            "quality": "Q2",
            "tags": [
                    "Enil", 
                ],
            "comments": "Foraging.",
        }
    metadata["annotations"].append(
        {
            "user": "AI-user-2",
            "quality": "Q1",
            "tags": [
                    "None", 
                ],
            "comments": "By AI-2.",
        }
    )
    wurb_core.metadata_rec.write_metadata(rec_file, metadata)

    print("First: ", wurb_core.metadata_rec.get_metadata(rec_file, select="first")["recording"]["timeLocal"])
    print("Previous: ", wurb_core.metadata_rec.get_metadata(rec_file, select="previous")["recording"]["timeLocal"])
    print("Same: ", wurb_core.metadata_rec.get_metadata(rec_file, select="")["recording"]["timeLocal"])
    print("Next: ", wurb_core.metadata_rec.get_metadata(rec_file, select="next")["recording"]["timeLocal"])
    print("Last: ", wurb_core.metadata_rec.get_metadata(rec_file, select="last")["recording"]["timeLocal"])

    print("TEST ended.")
    ### FOR TEST - END ###

    # WURB core shutdown.
    logger.debug("WURB shutdown started.")
    wurb_core.manager.shutdown()
    logger.debug("WURB shutdown done.")


if __name__ == "__main__":
    """ """
    asyncio.run(main())
