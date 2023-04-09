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
