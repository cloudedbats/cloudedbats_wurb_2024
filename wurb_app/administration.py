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


@admin_router.get("/module-admin/", tags=["File administration"], description="Administration module as module.")
async def module_admin(request: fastapi.Request):
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
        logger.debug("Exception: module_admin: " + str(e))

@admin_router.get("/module-admin/get-rec-sources", tags=["File administration"], description="Get source directories.")
async def get_rec_sources(request: fastapi.Request):
    """ """
    try:
        logger.debug("API called: get_source_dirs.")
        # json_data = {"source_dirs": ["../wurb_recordings", "../../wurb_recordings"]}
        json_data = wurb_core.sources_and_files.get_rec_sources()
        return JSONResponse(content=json_data)
    except Exception as e:
        logger.debug("Exception: get_source_dirs: " + str(e))

@admin_router.get("/module-admin/get-rec-nights", tags=["File administration"], description="Get source directories.")
async def get_rec_nights(request: fastapi.Request):
    """ """
    try:
        logger.debug("API called: get_source_dirs.")
        json_data = wurb_core.sources_and_files.get_rec_nights(source_dir="../wurb_recordings")
        return JSONResponse(content=json_data)
    except Exception as e:
        logger.debug("Exception: get_source_dirs: " + str(e))
