#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org, https://github.com/cloudedbats
# Copyright (c) 2023-present Arnold Andreasson
# License: MIT License (see LICENSE or http://opensource.org/licenses/mit).

import logging
import fastapi
import fastapi.templating
import wurb_core

logger = logging.getLogger(wurb_core.used_logger)
templates = fastapi.templating.Jinja2Templates(directory="wurb_app/templates")
live_router = fastapi.APIRouter()


@live_router.get(
    "/pages/live", tags=["HTML pages"], description="Live page loaded as HTML."
)
async def load_live_page(request: fastapi.Request):
    """ """
    try:
        logger.debug("API called: module_live.")
        return templates.TemplateResponse(
            "live.html",
            {
                "request": request,
                "wurb_version": wurb_core.__version__,
            },
        )
    except Exception as e:
        logger.debug("Exception: module_live: " + str(e))


@live_router.get(
    "/live/set-audio-feedback/", tags=["Live"], description="Live..."
)
# @app.get("/set-audio-feedback/")
async def set_audio_feedback(volume: str, pitch: str):
    try:
        global wurb_rec_manager
        # Logging debug.
        message = "API called: set-audio-feedback."
        wurb_rec_manager.wurb_logging.debug(message=message)
        await wurb_rec_manager.wurb_settings.set_audio_feedback(volume, pitch)
    except Exception as e:
        # Logging error.
        message = "Called: set_audio_feedback: " + str(e)
        wurb_rec_manager.wurb_logging.error(message, short_message=message)
