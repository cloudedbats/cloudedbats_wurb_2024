#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Cloudedbats WURB-2024.

from wurb_api.record import record_router
from wurb_api.live import live_router
from wurb_api.annotations import annotations_router
from wurb_api.administration import admin_router
from wurb_api.about import about_router

from wurb_api.main import app

