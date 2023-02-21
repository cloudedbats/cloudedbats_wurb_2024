#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org, https://github.com/cloudedbats
# Copyright (c) 2023-present Arnold Andreasson
# License: MIT License (see LICENSE or http://opensource.org/licenses/mit).

import logging
import fastapi
import fastapi.templating
from fastapi.responses import JSONResponse
from typing import Union
import wurb_core

logger = logging.getLogger(wurb_core.used_logger)
templates = fastapi.templating.Jinja2Templates(directory="wurb_app/templates")
annotations_router = fastapi.APIRouter()


@annotations_router.get(
    "/pages/annotations",
    tags=["HTML pages"],
    description="Annotations page loaded as HTML.",
)
async def load_annotations_page(request: fastapi.Request):
    """ """
    try:
        logger.debug("API called: module_annotations.")
        return templates.TemplateResponse(
            "annotations.html",
            {
                "request": request,
                "wurb_version": wurb_core.__version__,
            },
        )
    except Exception as e:
        logger.debug("Exception: module_annotations: " + str(e))


@annotations_router.get(
    "/annotations/sources",
    tags=["Annotations"],
    description="Get source directories for recordings.",
)
async def get_annotations_sources(request: fastapi.Request):
    """ """
    try:
        logger.debug("API called: get_source_dirs.")
        # json_data = {"source_dirs": ["../wurb_recordings", "../../wurb_recordings"]}
        json_data = wurb_core.record_manager.get_rec_sources()
        return JSONResponse(content=json_data)
    except Exception as e:
        logger.debug("Exception: get_source_dirs: " + str(e))


@annotations_router.get(
    "/annotations/nights",
    tags=["Annotations"],
    description="Get directories for recording nights.",
)
async def get_recording_nights(
    sourceId: str,
):
    """ """
    try:
        logger.debug("API called: get_source_dirs.")
        json_data = wurb_core.record_manager.get_rec_nights(source_id=sourceId)
        return JSONResponse(content=json_data)
    except Exception as e:
        logger.debug("Exception: get_source_dirs: " + str(e))


@annotations_router.get(
    "/annotations/record-info",
    tags=["Annotations"],
    description="Get info for one sound recording.",
)
async def get_recording_info(
    sourceId: str,
    nightId: str,
    recordId: Union[str, None] = None,
):
    """ """
    try:
        logger.debug("API called: get_recording_info.")
        json_data = wurb_core.record_manager.get_rec_info(
            source_id=sourceId,
            night_id=nightId,
            record_id=recordId,
        )
        return JSONResponse(content=json_data)
    except Exception as e:
        logger.debug("Exception: get_recording_info: " + str(e))
