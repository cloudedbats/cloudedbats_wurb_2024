#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org, https://github.com/cloudedbats
# Copyright (c) 2023-present Arnold Andreasson
# License: MIT License (see LICENSE or http://opensource.org/licenses/mit).

import logging
import fastapi
import fastapi.templating
from fastapi.responses import JSONResponse
import wurb_core

logger = logging.getLogger(wurb_core.used_logger)
templates = fastapi.templating.Jinja2Templates(directory="wurb_app/templates")
admin_router = fastapi.APIRouter()


@admin_router.get("/ajax-admin/", tags=["File administration"], description="Administration module as AJAX.")
async def ajax_admin(request: fastapi.Request):
    """ """
    try:
        logger.debug("API called: ajax_admin.")
        return templates.TemplateResponse(
            "administration.html",
            {
                "request": request,
                "wurb_version": wurb_core.__version__,
            },
        )
    except Exception as e:
        logger.debug("Exception: ajax_admin: " + str(e))

@admin_router.get("/ajax-admin/get-source-dirs", tags=["File administration"], description="Get source directories.")
async def get_source_dirs(request: fastapi.Request):
    """ """
    try:
        logger.debug("API called: get_source_dirs.")
        json_data = {"source_dirs": ["../wurb_recordings", "../../wurb_recordings"]}
        return JSONResponse(content=json_data)
    except Exception as e:
        logger.debug("Exception: get_source_dirs: " + str(e))

@admin_router.get("/ajax-admin/get-events-dirs", tags=["File administration"], description="Get source directories.")
async def get_source_dirs(request: fastapi.Request):
    """ """
    try:
        logger.debug("API called: get_source_dirs.")
        json_data = [
            "Taberg_2022-12-30", 
            "Taberg_2022-12-31",
            "Taberg_2023-01-01",
            "Taberg_2023-01-02",
            "Taberg_2023-01-03",
            "Taberg_2023-01-04",
            "Taberg_2023-01-05",
            ]
        return JSONResponse(content=json_data)
    except Exception as e:
        logger.debug("Exception: get_source_dirs: " + str(e))
