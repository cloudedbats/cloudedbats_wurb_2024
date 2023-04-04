#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org, https://github.com/cloudedbats
# Copyright (c) 2023-present Arnold Andreasson
# License: MIT License (see LICENSE or http://opensource.org/licenses/mit).

import logging

import time

# import datetime
import asyncio
import fastapi
import fastapi.templating
from pydantic import BaseModel
from typing import Optional
import websockets.exceptions

import wurb_core

logger = logging.getLogger(wurb_core.logger_name)
templates = fastapi.templating.Jinja2Templates(directory="wurb_app/templates")
record_router = fastapi.APIRouter()


@record_router.get(
    "/pages/record", tags=["HTML pages"], description="Record page loaded as HTML."
)
async def load_record_page(request: fastapi.Request):
    """ """
    try:
        logger.debug("API called: module_record.")
        return templates.TemplateResponse(
            "record.html",
            {
                "request": request,
                "wurb_version": wurb_core.__version__,
            },
        )
    except Exception as e:
        logger.debug("Exception: module_record: " + str(e))


# @app.get("/")
# async def webpage(request: fastapi.Request):
#     try:
#         # Logging debug.
#         logger.debug("API called: webpage.")
#         status_dict = await wurb_core.rec_manager.get_status_dict()
#         location_status = wurb_core.wurb_settings.get_location_status()
#         return templates.TemplateResponse(
#             "wurb_rec_web.html",
#             {
#                 "request": request,
#                 "rec_status": status_dict.get("rec_status", ""),
#                 "location_status": location_status,
#                 "device_name": status_dict.get("device_name", ""),
#                 "detector_time": time.strftime("%Y-%m-%d %H:%M:%S"),
#                 "wurb_version": wurb_core.__version__,
#             },
#         )
#     except Exception as e:
#         # Logging error.
#         message = "Called: webpage: " + str(e)
#         logger.error(message)


# Schemas.
class LocationSettings(BaseModel):
    geoSource: Optional[str] = None
    latitudeDd: Optional[float] = None
    longitudeDd: Optional[float] = None
    manualLatitudeDd: Optional[float] = None
    manualLongitudeDd: Optional[float] = None


class DetectorSettings(BaseModel):
    recMode: Optional[str] = None
    fileDirectory: Optional[str] = None
    fileDirectoryDateOption: Optional[str] = None
    filenamePrefix: Optional[str] = None
    detectionLimitKhz: Optional[float] = None
    detectionSensitivityDbfs: Optional[float] = None
    detectionAlgorithm: Optional[str] = None
    recLengthS: Optional[str] = None
    rec_type: Optional[str] = None
    feedbackOnOff: Optional[str] = None
    feedbackVolume: Optional[float] = None
    feedbackPitch: Optional[float] = None
    feedbackFilterLowKhz: Optional[float] = None
    feedbackFilterHighKhz: Optional[float] = None
    startupOption: Optional[str] = None
    schedulerStartEvent: Optional[str] = None
    schedulerStartAdjust: Optional[float] = None
    schedulerStopEvent: Optional[str] = None
    schedulerStopAdjust: Optional[float] = None
    # schedulerPostAction: Optional[str] = None
    # schedulerPostActionDelay: Optional[float] = None


# @record_router.get("/record/start-rec/", tags=["Recorder"], description="Record...")
# # @app.get("/start-rec/")
# async def start_recording():
#     try:
#         # Logging debug.
#         logger.debug("API called: start-rec.")
#         # await wurb_core.rec_manager.start_rec()
#     except Exception as e:
#         # Logging error.
#         message = "Called: start_rec: " + str(e)
#         logger.error(message)


# @record_router.get("/record/stop-rec/", tags=["Recorder"], description="Record...")
# # @app.get("/stop-rec/")
# async def stop_recording():
#     try:
#         # Logging debug.
#         logger.debug("API called: stop-rec.")
#         # await wurb_core.rec_manager.stop_rec()
#     except Exception as e:
#         # Logging error.
#         message = "Called: stop_rec: " + str(e)
#         logger.error(message)


# @record_router.get("/record/get-status/", tags=["Recorder"], description="Record...")
# # @app.get("/get-status/")
# async def get_status():
#     try:
#         # Logging debug.
#         logger.debug("API called: get-status.")
#         status_dict = await wurb_core.rec_manager.get_status_dict()
#         location_status = wurb_core.wurb_settings.get_location_status()
#         return {
#             "rec_status": status_dict.get("rec_status", ""),
#             "location_status": location_status,
#             "device_name": status_dict.get("device_name", ""),
#             "detector_time": time.strftime("%Y-%m-%d %H:%M:%S"),
#         }
#     except Exception as e:
#         # Logging error.
#         message = "Called: get_status: " + str(e)
#         logger.error(message)


@record_router.post(
    "/record/save-location/", tags=["Recorder"], description="Record..."
)
# @app.post("/save-location/")
async def save_location(settings: LocationSettings):
    try:
        # Logging debug.
        logger.debug("API called: save-location.")
        await wurb_core.wurb_settings.save_location(settings.dict())
    except Exception as e:
        # Logging error.
        message = "Called: save_location: " + str(e)
        logger.error(message)


@record_router.get("/record/get-location/", tags=["Recorder"], description="Record...")
# @app.get("/get-location/")
async def get_location(default: bool = False):
    try:
        # Logging debug.
        logger.debug("API called: get-location.")
        current_location_dict = await wurb_core.wurb_settings.get_location()
        return current_location_dict
    except Exception as e:
        # Logging error.
        message = "Called: get_location: " + str(e)
        logger.error(message)


@record_router.get("/record/set-time/", tags=["Recorder"], description="Record...")
# @app.get("/set-time/")
async def set_time(posixtime: str):
    try:
        # Logging debug.
        message = "API called: set-time: " + str(posixtime)
        logger.debug(message)
        posix_time_s = int(int(posixtime) / 1000)
        await wurb_core.wurb_rpi.set_detector_time(posix_time_s, cmd_source="by user")
    except Exception as e:
        # Logging error.
        message = "Called: set_time: " + str(e)
        logger.error(message)


# @record_router.post("/record/save-rec-mode/", tags=["Recorder"], description="Record...")
# # @app.get("/save-rec-mode/")
# async def save_rec_mode(recmode: str):
#     try:
#         # Logging debug.
#         logger.debug("API called: save-rec-mode.")
#         await wurb_core.wurb_settings.save_rec_mode(recmode)
#     except Exception as e:
#         # Logging error.
#         message = "Called: save_rec_mode: " + str(e)
#         logger.error(message)


@record_router.post(
    "/record/save-settings/", tags=["Recorder"], description="Record..."
)
# @app.post("/save-settings/")
async def save_settings(settings: DetectorSettings):
    try:
        # Logging debug.
        logger.debug("API called: save-settings.")
        await wurb_core.wurb_settings.save_settings(settings.dict())
    except Exception as e:
        # Logging error.
        message = "Called: save_settings: " + str(e)
        logger.error(message)


@record_router.post(
    "/record/save-settings-user/", tags=["Recorder"], description="Record..."
)
# @app.post("/save-settings-user/")
async def save_settings_user(settings: DetectorSettings):
    try:
        # Logging debug.
        logger.debug("API called: save-settings-user.")
        await wurb_core.wurb_settings.save_settings(
            settings.dict(), settings_type="user-default"
        )
    except Exception as e:
        # Logging error.
        message = "Called: save-settings-user: " + str(e)
        logger.error(message)


@record_router.post(
    "/record/save-settings-startup/", tags=["Recorder"], description="Record..."
)
# @app.post("/save-settings-startup/")
async def save_settings_startup(settings: DetectorSettings):
    try:
        # Logging debug.
        logger.debug("API called: save-settings-startup.")
        await wurb_core.wurb_settings.save_settings(
            settings.dict(), settings_type="startup"
        )
    except Exception as e:
        # Logging error.
        message = "Called: save-settings-startup: " + str(e)
        logger.error(message)


@record_router.get("/record/get-settings/", tags=["Recorder"], description="Record...")
# @app.get("/get-settings/")
async def get_settings(default: bool = False):
    try:
        # Logging debug.
        logger.debug("API called: get-settings.")
        current_settings_dict = await wurb_core.wurb_settings.get_settings(default)
        return current_settings_dict
    except Exception as e:
        # Logging error.
        message = "Called: get_settings: " + str(e)
        logger.error(message)


@record_router.get("/record/load-settings/", tags=["Recorder"], description="Record...")
# @app.get("/load-settings/")
async def load_settings(settingsType: str):
    try:
        # Logging debug.
        logger.debug("API called: load-settings.")
        await wurb_core.wurb_settings.load_settings(settingsType)
    except Exception as e:
        # Logging error.
        message = "Called: load_settings: " + str(e)
        logger.error(message)


@record_router.get("/record/rec-status/", tags=["Recorder"], description="Record...")
# @app.get("/rec-status/")
async def rec_status():
    try:
        # Logging debug.
        message = "API called: rec-status."
        # logger.debug(message)
        await wurb_core.rec_status.rec_status()
    except Exception as e:
        # Logging error.
        message = "Called: rec-status: " + str(e)
        logger.error(message)


@record_router.get("/record/rpi-control/", tags=["Recorder"], description="Record...")
# @app.get("/rpi-control/")
async def rpi_control(command: str):
    try:
        # Logging debug.
        message = "API called: rpi-control:" + command + "."
        # logger.debug(message)
        await wurb_core.wurb_rpi.rpi_control(command)
    except Exception as e:
        # Logging error.
        message = "Called: rpi_control: " + str(e)
        logger.error(message)


@record_router.get(
    "/record/rec-manual-trigger/", tags=["Recorder"], description="Record..."
)
# @app.get("/rec-manual-trigger/")
async def rec_manual_trigger():
    try:
        # Logging debug.
        message = "API called: manual-trigger."
        logger.debug(message)
        await wurb_core.rec_manager.manual_trigger()
    except Exception as e:
        # Logging error.
        message = "Called: rec_manual_trigger: " + str(e)
        logger.error(message)


@record_router.websocket("/record/ws")
# @app.websocket("/ws")
async def websocket_endpoint(websocket: fastapi.WebSocket):
    try:
        # Logging debug.
        logger.debug("API Websocket initiated.")
        wurb_core.wurb_logger.info("API Websocket initiated.")
        ### await asyncio.sleep(1.0)
        #
        await websocket.accept()
        #
        # Get event notification objects.
        rec_event = wurb_core.rec_manager.get_rec_event()
        location_event = wurb_core.wurb_settings.get_location_event()
        latlong_event = wurb_core.wurb_settings.get_latlong_event()
        settings_event = wurb_core.wurb_settings.get_settings_event()
        logging_event = wurb_core.wurb_logger.get_logging_event()
        # Update client.
        ws_json = {}
        status_dict = await wurb_core.rec_manager.get_status_dict()
        location_status = wurb_core.wurb_settings.get_location_status()
        ws_json["status"] = {
            "recStatus": status_dict.get("rec_status", ""),
            "locationStatus": location_status,
            "deviceName": status_dict.get("device_name", ""),
            "detectorTime": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        ws_json["location"] = await wurb_core.wurb_settings.get_location()
        ws_json["latlong"] = await wurb_core.wurb_settings.get_location()
        ws_json["settings"] = await wurb_core.wurb_settings.get_settings()
        ws_json["logRows"] = wurb_core.wurb_logger.get_client_messages()
        # Send update to client.
        await websocket.send_json(ws_json)
        # Loop.
        while True:
            # Wait for next event to happen.
            task_1 = asyncio.create_task(asyncio.sleep(1.0), name="ws-sleep-event")
            task_2 = asyncio.create_task(rec_event.wait(), name="ws-rec-event")
            task_3 = asyncio.create_task(
                location_event.wait(), name="ws-location-event"
            )
            task_4 = asyncio.create_task(latlong_event.wait(), name="ws-latlong-event")
            task_5 = asyncio.create_task(
                settings_event.wait(), name="ws-settings-event"
            )
            task_6 = asyncio.create_task(logging_event.wait(), name="ws-logging-event")
            events = [
                task_1,
                task_2,
                task_3,
                task_4,
                task_5,
                task_6,
            ]
            done, pending = await asyncio.wait(
                events, return_when=asyncio.FIRST_COMPLETED
            )
            for task in done:
                # print("Done WS: ", task.get_name())
                task.cancel()
            for task in pending:
                task.cancel()

            # Prepare message to client.
            ws_json = {}
            status_dict = await wurb_core.rec_manager.get_status_dict()
            location_status = wurb_core.wurb_settings.get_location_status()
            ws_json["status"] = {
                "recStatus": status_dict.get("rec_status", ""),
                "locationStatus": location_status,
                "deviceName": status_dict.get("device_name", ""),
                "detectorTime": time.strftime("%Y-%m-%d %H:%M:%S"),
            }

            rec_event = wurb_core.rec_manager.get_rec_event()

            if location_event.is_set():
                location_event = wurb_core.wurb_settings.get_location_event()
                ws_json["location"] = await wurb_core.wurb_settings.get_location()
            if latlong_event.is_set():
                latlong_event = wurb_core.wurb_settings.get_latlong_event()
                ws_json["latlong"] = await wurb_core.wurb_settings.get_location()
            if settings_event.is_set():
                settings_event = wurb_core.wurb_settings.get_settings_event()
                ws_json["settings"] = await wurb_core.wurb_settings.get_settings()
            if logging_event.is_set():
                logging_event = wurb_core.wurb_logger.get_logging_event()
                ws_json["logRows"] = wurb_core.wurb_logger.get_client_messages()
            # Send to client.
            await websocket.send_json(ws_json)

    except websockets.exceptions.ConnectionClosed as e:
        pass
    except Exception as e:
        # Logging error.
        message = "Called: websocket_endpoint: " + str(e)
        logger.error(message)
