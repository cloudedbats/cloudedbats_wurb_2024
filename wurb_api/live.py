#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: https://cloudedbats.github.io
# Author: Arnold Andreasson, info@cloudedbats.org
# License: MIT License (see LICENSE or http://opensource.org/licenses/mit).

import logging
import pathlib
import fastapi
import fastapi.templating
import wurb_core

logger = logging.getLogger(wurb_core.logger_name)
templates_path = pathlib.Path(wurb_core.workdir_path, "wurb_app/templates")
templates = fastapi.templating.Jinja2Templates(directory=templates_path)
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
        message = "API - load_live_page. Exception: " + str(e)
        logger.debug(message)


@live_router.get("/live/set-audio-feedback/", tags=["Live"], description="Live...")
# @app.get("/set-audio-feedback/")
async def set_audio_feedback(volume: str, pitch: str):
    try:
        # Logging debug.
        message = "API called: set-audio-feedback."
        logger.debug(message)
        await wurb_core.rec_manager.wurb_settings.set_audio_feedback(volume, pitch)
    except Exception as e:
        message = "API - set_audio_feedback. Exception: " + str(e)
        logger.debug(message)
