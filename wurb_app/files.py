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
files_router = fastapi.APIRouter()


@files_router.get("/ajax-files/", tags=["AJAX"], description="Files module as AJAX.")
async def ajax_files(request: fastapi.Request):
    """ """
    try:
        logger.debug("API called: ajax_files.")
        return templates.TemplateResponse(
            "files.html",
            {
                "request": request,
                "wurb_version": wurb_core.__version__,
            },
        )
    except Exception as e:
        logger.debug("Exception: ajax_files: " + str(e))
