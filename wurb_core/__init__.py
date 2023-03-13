#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Cloudedbats WURB-2023.

__version__ = "2023.0.0-development"
used_logger = "WurbLogger"

import wurb_utils

from wurb_api.app_manager import AppManager
from wurb_core.common.settings import WurbSettings
from wurb_core.admin.sources_and_files import SourcesAndFiles
from wurb_core.annotations.metadata import Metadata
from wurb_core.annotations.metadata_table import MetadataTable
from wurb_core.annotations.record_manager import RecordManager
from wurb_core.record.gps_reader import GpsReader
from wurb_core.record.gps_reader import ReadGpsSerialNmea
from wurb_api.app_logger import AppLogger
from wurb_core.record.rec_manager import WurbRecManager
from wurb_core.record.sound_recorder import UltrasoundDevices
from wurb_core.record.sound_recorder import WurbRecorder
from wurb_core.record.sound_recorder import WaveFileWriter
from wurb_core.record.rpi_control import WurbRaspberryPi
from wurb_core.record.rec_scheduler import WurbScheduler
from wurb_core.record.sound_detection import SoundDetectionBase
from wurb_core.record.sound_detection import SoundDetection
from wurb_core.record.sound_detection import SoundDetectionNone
from wurb_core.record.sound_detection import SoundDetectionSimple


# To be used similar to singleton objects.
logger = wurb_utils.Logger(logger=used_logger)
config = wurb_utils.Configuration(logger=used_logger)
wurb_logger = AppLogger(logger=used_logger)

gps = GpsReader(logger=used_logger)
app_manager = AppManager(logger=used_logger)

sources_and_files = SourcesAndFiles(logger=used_logger)
metadata = Metadata(logger=used_logger)
metadata_table = MetadataTable(logger=used_logger)
record_manager = RecordManager(logger=used_logger)


### sound_stream_manager = SoundStreamManager()
wurb_rpi = WurbRaspberryPi(logger=used_logger)
wurb_settings = WurbSettings(logger=used_logger)


wurb_manager = WurbRecManager(logger=used_logger)
wurb_ultrasond_device = UltrasoundDevices(logger=used_logger)
wurb_recorder = WurbRecorder(logger=used_logger)
wurb_wave_file_writer = WaveFileWriter(logger=used_logger)
wurb_scheduler = WurbScheduler(logger=used_logger)
###wurb_settings = WurbSettings(logger=used_logger)
wurb_sound_detection_base = SoundDetectionBase(logger=used_logger)
wurb_sound_detection = SoundDetection(logger=used_logger)
wurb_sound_detection_none = SoundDetectionNone(logger=used_logger)
wurb_sound_detection_simple = SoundDetectionSimple(logger=used_logger)
