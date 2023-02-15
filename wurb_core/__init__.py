#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Cloudedbats WURB-2023.

import wurb_utils

__version__ = "2023.0.0-development"
used_logger = "WurbLogger"

from wurb_core.wurb_gps import WurbGps
from wurb_core.wurb_manager import WurbManager

from wurb_core.admin.sources_and_files import SourcesAndFiles
from wurb_core.annotate.rec_metadata import MetadataRec
from wurb_core.annotate.rec_metadata_table import MetadataRecTable


# To be used similar to singleton objects.
logger = wurb_utils.Logger(logger=used_logger)
config = wurb_utils.Configuration(logger=used_logger)
gps = WurbGps(logger=used_logger)
manager = WurbManager(logger=used_logger)

sources_and_files = SourcesAndFiles(logger=used_logger)
metadata_rec = MetadataRec(logger=used_logger)
metadata_rec_table = MetadataRecTable(logger=used_logger)
