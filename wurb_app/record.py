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
record_router = fastapi.APIRouter()


@record_router.get("/ajax-record/", tags=["AJAX"], description="Record module as AJAX.")
async def ajax_record(request: fastapi.Request):
    """ """
    try:
        logger.debug("API called: ajax_record.")
        return templates.TemplateResponse(
            "record.html",
            {
                "request": request,
                "wurb_version": wurb_core.__version__,
            },
        )
    except Exception as e:
        logger.debug("Exception: ajax_record: " + str(e))
