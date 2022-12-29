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


@live_router.get("/ajax-live/", tags=["AJAX"], description="live module as AJAX.")
async def ajax_live(request: fastapi.Request):
    """ """
    try:
        logger.debug("API called: ajax_live.")
        return templates.TemplateResponse(
            "live.html",
            {
                "request": request,
                "wurb_version": wurb_core.__version__,
            },
        )
    except Exception as e:
        logger.debug("Exception: ajax_live: " + str(e))
