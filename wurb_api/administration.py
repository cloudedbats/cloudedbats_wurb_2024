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

logger = logging.getLogger(wurb_core.logger_name)
templates = fastapi.templating.Jinja2Templates(directory="wurb_app/templates")
admin_router = fastapi.APIRouter()


@admin_router.get(
    "/pages/admin",
    tags=["HTML pages"],
    description="Administration page loaded as HTML.",
)
async def load_admin_page(request: fastapi.Request):
    """ """
    try:
        logger.debug("API called: module_admin.")
        return templates.TemplateResponse(
            "administration.html",
            {
                "request": request,
                "wurb_version": wurb_core.__version__,
            },
        )
    except Exception as e:
        message = "API - load_admin_page. Exception: " + str(e)
        logger.debug(message)


@admin_router.get(
    "/administration/sources",
    tags=["Administration"],
    description="Get source directories for recordings.",
)
async def get_recording_sources(request: fastapi.Request):
    """ """
    try:
        logger.debug("API called: get_source_dirs.")
        json_data = wurb_core.record_manager.get_rec_sources()
        return JSONResponse(content=json_data)
    except Exception as e:
        message = "API - get_recording_sources. Exception: " + str(e)
        logger.debug(message)


@admin_router.get(
    "/administration/nights",
    tags=["Administration"],
    description="Get directories for recording events/nights.",
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
        message = "API - get_recording_nights. Exception: " + str(e)
        logger.debug(message)


@admin_router.get(
    "/administration/info",
    tags=["Administration"],
    description="Get info for one recording event/night.",
)
async def get_administration_info(
    sourceId: str,
    nightId: str,
):
    """ """
    try:
        logger.debug("API called: get_administration_info.")
        json_data = await wurb_core.admin_info.extract_info(
            source_id=sourceId, night_id=nightId
        )
        return JSONResponse(content=json_data)
    except Exception as e:
        message = "API - get_administration_info. Exception: " + str(e)
        logger.debug(message)


@admin_router.post(
    "/administration/command",
    tags=["Administration"],
    description="Get info for one recording event/night.",
)
async def administration_command(
    sourceId: str,
    nightId: str,
    command: str,
):
    """ """
    try:
        logger.debug("API called: administration_command: " + command)

        if command == "removeQ0":
            await wurb_core.cleanup.remove_q0(source_id=sourceId, night_id=nightId)
        elif command == "removeNa":
            await wurb_core.cleanup.remove_not_assigned(
                source_id=sourceId, night_id=nightId
            )
        elif command == "deleteMonitoringNight":
            await wurb_core.cleanup.delete_monitoring_night(
                source_id=sourceId, night_id=nightId
            )
        elif command == "createReport":
            await wurb_core.report_excel.create_report(
                source_id=sourceId, night_id=nightId
            )
    except Exception as e:
        message = "API - administration_command. Exception: " + str(e)
        logger.debug(message)
