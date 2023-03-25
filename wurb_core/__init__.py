#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Cloudedbats WURB-2023.

__version__ = "2023.0.0-development"
logger_name = "WurbLogger"

import pyaudio
import wurb_utils

from wurb_core.common.wurb_logger import WurbLogger
from wurb_core.common.wurb_settings import WurbSettings
from wurb_core.common.wurb_manager import WurbManager

from wurb_core.administration.sources_and_files import SourcesAndFiles
from wurb_core.annotations.metadata import Metadata
from wurb_core.annotations.metadata_table import MetadataTable
from wurb_core.annotations.record_manager import RecordManager

from wurb_core.record.rec_manager import RecManager
from wurb_core.record.gps_reader import GpsReader
from wurb_core.record.rpi_control import WurbRaspberryPi
from wurb_core.record.rec_scheduler import WurbScheduler
from wurb_core.record.rec_manager import RecManager
from wurb_core.record.rec_devices import RecDevices
from wurb_core.record.rec_worker import RecWorker
from wurb_core.record.rec_sound_detection import SoundDetection
from wurb_core.record.rec_sound_detection import SoundDetectionBase
from wurb_core.record.rec_sound_detection import SoundDetectionNone
from wurb_core.record.rec_sound_detection import SoundDetectionSimple
from wurb_core.record.rec_file_writer import RecFileWriter


# Instances of objects.

# Configuration and logging.
config = wurb_utils.Configuration(logger_name=logger_name)
logger = wurb_utils.Logger(logger_name=logger_name)

# Basic WURB. 
wurb_logger = WurbLogger(config, logger_name=logger_name)
wurb_settings = WurbSettings(config, wurb_logger)
wurb_manager = WurbManager(config, wurb_logger)

# Audio.
audio = pyaudio.PyAudio()
audio_capture = wurb_utils.AudioCapture(audio, logger_name=logger_name)
audio_pitch_shifting = wurb_utils.AudioPitchShifting(logger_name=logger_name)
audio_playback = wurb_utils.AudioPlayback(audio, logger_name=logger_name)

# Record and live.
rec_manager = RecManager(config, wurb_logger)
rec_scheduler = WurbScheduler(config, wurb_logger)
rec_devices = RecDevices(config, wurb_logger)
rec_worker = RecWorker(config, wurb_logger)
### rec_file_writer = RecFileWriter(config, wurb_logger)
sound_detection_base = SoundDetectionBase(config, wurb_logger)
sound_detection = SoundDetection(config, wurb_logger)
sound_detection_none = SoundDetectionNone(config, wurb_logger)
sound_detection_simple = SoundDetectionSimple(config, wurb_logger)
wurb_rpi = WurbRaspberryPi(config, wurb_logger)
gps = GpsReader(config, wurb_logger)

# Annotations and administration.
sources_and_files = SourcesAndFiles(config, wurb_logger)
metadata = Metadata(config, logger)
metadata_table = MetadataTable(config, wurb_logger)
record_manager = RecordManager(config, wurb_logger)


