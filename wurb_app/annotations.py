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
annotations_router = fastapi.APIRouter()


@annotations_router.get(
    "/ajax-annotations/", tags=["AJAX"], description="Annotations module as AJAX."
)
async def ajax_annotations(request: fastapi.Request):
    """ """
    try:
        logger.debug("API called: ajax_annotations.")
        return templates.TemplateResponse(
            "annotations.html",
            {
                "request": request,
                "wurb_version": wurb_core.__version__,
            },
        )
    except Exception as e:
        logger.debug("Exception: ajax_annotations: " + str(e))


@annotations_router.get(
    "/ajax-annotations/get-annotations",
    tags=["File administration"],
    description="Get annotations for recordings in sampling event.",
)
async def get_annotations(request: fastapi.Request):
    """ """
    try:
        logger.debug("API called: get_annotations.")
        json_data = [
            {
                "waveFileName": "w53.......",
                "quality": "Q2",
                "tags": ["FM-QCF", "Social"],
                "comments": "Comment...",
            },
            {
                "waveFileName": "w53.......",
                "quality": "Q2",
                "tags": ["FM-QCF", "Social"],
                "comments": "Comment...",
            },
            {
                "waveFileName": "w53.......",
                "quality": "Q2",
                "tags": ["FM-QCF", "Social"],
                "comments": "Comment...",
            },
        ]
        return JSONResponse(content=json_data)
    except Exception as e:
        logger.debug("Exception: get_annotations: " + str(e))


@annotations_router.get(
    "/ajax-annotations/get-recording-info",
    tags=["File administration"],
    description="Get info for one sound recording.",
)
async def get_recording_info(request: fastapi.Request):
    """ """
    try:
        logger.debug("API called: get_recording_info.")
        json_data = {
            "fileIndex": 1,
            "maxIndex": 70,
            "eventPath": "wurb_recordings",
            "waveFileName": "w53.......",
            "spectrogramPath": "wurb_recordings",
            "spectrogramName": "Taberg_2022-12-30_PEAKS.png",
            "overviewPath": "wurb_recordings",
            "overviewName": "Taberg_2022-12-30_PEAKS.png",
            "quality": "Q2",
            "tags": ["FM-QCF", "Social"],
            "comments": "Comment...",
        }
        return JSONResponse(content=json_data)
    except Exception as e:
        logger.debug("Exception: get_recording_info: " + str(e))
