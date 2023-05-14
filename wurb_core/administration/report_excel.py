#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org, https://github.com/cloudedbats
# Copyright (c) 2023-present Arnold Andreasson
# License: MIT License (see LICENSE or http://opensource.org/licenses/mit).

import asyncio
import logging
import pathlib
import xlsxwriter

import wurb_core


class ReportExcel(object):
    """ """

    def __init__(self, config=None, logger=None, logger_name="DefaultLogger"):
        """ """
        self.config = config
        self.logger = logger
        if self.config == None:
            self.config = {}
        if self.logger == None:
            self.logger = logging.getLogger(logger_name)
        #
        self.clear()
        self.configure()

    def clear(self):
        """ """

    def configure(self):
        """ """
        self.summary_columns = [
            {
                "header": "Monitoring night",
                "sourceKey": "recording.monitoringNight",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 30,
            },
            {
                "header": "Date",
                "sourceKey": "recording.dateLocal",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 10,
            },
            {
                "header": "Time",
                "sourceKey": "recording.timeLocal",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 10,
            },
            {
                "header": "Quality",
                "sourceKey": "annotations.wurb-user.quality",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 10,
            },
            {
                "header": "Tags",
                "sourceKey": "annotations.wurb-user.tags",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 20,
            },
            {
                "header": "Comments",
                "sourceKey": "annotations.wurb-user.comments",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 30,
            },
            {
                "header": "Latitude",
                "sourceKey": "recording.latitude",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 30,
            },
            {
                "header": "Longitude",
                "sourceKey": "recording.longitude",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 30,
            },
            {
                "header": "File name",
                "sourceKey": "recording.recFileName",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 10,
            },
        ]
        self.detailed_columns = [
            {
                "header": "Night",
                "sourceKey": "recording.night",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 25,
            },
            {
                "header": "Date",
                "sourceKey": "recording.dateLocal",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 10,
            },
            {
                "header": "Time",
                "sourceKey": "recording.timeLocal",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 10,
            },
            {
                "header": "Quality",
                "sourceKey": "annotations.wurb-user.quality",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 10,
            },
            {
                "header": "Tags",
                "sourceKey": "annotations.wurb-user.tags",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 20,
            },
            {
                "header": "Comments",
                "sourceKey": "annotations.wurb-user.comments",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 30,
            },
            {
                "header": "Latitude",
                "sourceKey": "recording.latitude",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 30,
            },
            {
                "header": "Longitude",
                "sourceKey": "recording.longitude",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 30,
            },
            {
                "header": "File name",
                "sourceKey": "recording.recFileName",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 10,
            },
            {
                "header": "User",
                "sourceKey": "annotations.wurb-user.user",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 10,
            },
            {
                "header": "Datetime UTC",
                "sourceKey": "recording.dateTimeUtc",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 20,
            },
            {
                "header": "Detection algorithm",
                "sourceKey": "recording.detectionAlgorithm",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 10,
            },
            {
                "header": "Limit kHz",
                "sourceKey": "recording.detectionLimitKhz",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 15,
            },
            {
                "header": "Sensitivity dBFS",
                "sourceKey": "recording.detectionSensitivityDbfs",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 15,
            },
            {
                "header": "Device name",
                "sourceKey": "recording.deviceName",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 40,
            },
            {
                "header": "Geo source",
                "sourceKey": "recording.geoSource",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 10,
            },
            {
                "header": "Max peak dBFS",
                "sourceKey": "recording.maxPeakDbfs",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 10,
            },
            {
                "header": "Max peak freq Hz",
                "sourceKey": "recording.maxPeakFreqHz",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 10,
            },
            {
                "header": "Moon phase",
                "sourceKey": "recording.moonPhase",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 10,
            },
            {
                "header": "Scheduler start event",
                "sourceKey": "recording.schedulerStartEvent",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 10,
            },
            {
                "header": "Scheduler start adjust",
                "sourceKey": "recording.schedulerStartAdjust",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 10,
            },
            {
                "header": "Scheduler stop adjust",
                "sourceKey": "recording.schedulerStopAdjust",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 10,
            },
            {
                "header": "Sunrise local",
                "sourceKey": "recording.sunriseLocal",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 10,
            },
            {
                "header": "Sunset local",
                "sourceKey": "recording.sunsetLocal",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 10,
            },
        ]

    def flatten_metadata(self, metadata):
        """ """
        flat_metadata = {}
        # Recording.
        recording_dict = metadata.get("recording", {})
        for key, value in recording_dict.items():
            flat_metadata["recording." + key] = value
        # Annotations.
        annotations = metadata.get("annotations", {})
        for annotation in annotations:
            user = annotation.get("user", "no-user")
            for key, value in annotation.items():
                flat_metadata["annotations." + user + "." + key] = value
        #
        return flat_metadata

    def get_report_path(self, source_id, night_id):
        """ """
        report_path = ""
        if (source_id) and (night_id):
            source_dir = pathlib.Path(
                wurb_core.record_manager.get_source_dir(source_id)
            )
            data_dir = pathlib.Path(source_dir, night_id, "data")
            if not data_dir.exists():
                data_dir.mkdir(parents == True)
            report_name = night_id + "_report.xlsx"
            report_path = pathlib.Path(data_dir, report_name)

        return report_path

    async def create_report(
        self,
        source_id,
        night_id,
        report_path,
    ):
        """ """
        metadata_rows = []
        # Get files for night.
        for rec_file in wurb_core.record_manager.get_rec_files(source_id, night_id):
            print("FILE: ", str(rec_file))
            # Get metadata for recording.
            metadata = wurb_core.metadata.get_metadata(rec_file)

            flat_metadata = self.flatten_metadata(metadata)

            metadata_rows.append(flat_metadata)

        await asyncio.sleep(0.0)

        # Create Excel document.
        workbook = xlsxwriter.Workbook(str(report_path))

        # Add worksheets.
        summary_worksheet = workbook.add_worksheet("Summary")
        detailed_worksheet = workbook.add_worksheet("Detailed")
        about_worksheet = workbook.add_worksheet("About")

        # Create cell formats.
        self.bold_format = workbook.add_format({"bold": True})
        #         self.bold_format = workbook.add_format({"bold": True})
        #         self.bold_right_format = workbook.add_format({"bold": True, "align": "right"})
        #         self.integer_format = workbook.add_format()
        #         self.integer_format.set_num_format("0")
        #         self.decimal_format = workbook.add_format()
        #         self.decimal_format.set_num_format("0.00")
        #         self.decimal_6_format = workbook.add_format()
        #         self.decimal_6_format.set_num_format("0.000000")
        #         self.latlong_dd_format = workbook.add_format()
        #         self.latlong_dd_format.set_num_format("0.0000")

        # === Sheet: Summary. ===
        # Header.
        headers = []
        for column_dict in self.summary_columns:
            header = column_dict.get("header", "")
            headers.append(header)
        summary_worksheet.write_row(0, 0, headers, self.bold_format)
        # Rows.
        row_nr = 1
        for metadata_row in metadata_rows:
            row = []
            for column_dict in self.summary_columns:
                source_key = column_dict.get("sourceKey", "")
                format = column_dict.get("format", "")
                value = metadata_row.get(source_key, "")
                #
                row.append(value)
            #
            summary_worksheet.write_row(row_nr, 0, row)
            row_nr += 1

        # === Adjust column width. ===
        index = 0
        for column_dict in self.summary_columns:
            width = column_dict.get("columnWidth", 10)
            detailed_worksheet.set_column(index, index, int(width))
            index += 1

        # === Sheet: Detailed. ===
        # Header.
        headers = []
        for column_dict in self.detailed_columns:
            header = column_dict.get("header", "")
            headers.append(header)
        detailed_worksheet.write_row(0, 0, headers, self.bold_format)
        # Rows.
        row_nr = 1
        for metadata_row in metadata_rows:
            row = []
            for column_dict in self.detailed_columns:
                source_key = column_dict.get("sourceKey", "")
                format = column_dict.get("format", "")
                value = metadata_row.get(source_key, "")
                #
                row.append(value)
            #
            detailed_worksheet.write_row(row_nr, 0, row)
            row_nr += 1

        # === Adjust column width. ===
        index = 0
        for column_dict in self.detailed_columns:
            width = column_dict.get("columnWidth", 10)
            detailed_worksheet.set_column(index, index, int(width))
            index += 1

        # === Sheet: About. ===
        # Header.
        about_worksheet.write_row(0, 0, ["About"], self.bold_format)
        # Rows.
        readme_text = [
            [""],
            ["This Excel file is a part of the open source "],
            ["project CloudedBats.org: http://cloudedbats.org "],
            [""],
            ["Source code to generate the Excel file can be "],
            ["found in this GitHub repository: "],
            ["- https://github.com/cloudedbats/cloudedbats_wurb_2023"],
            [""],
        ]
        #
        row_nr = 1
        for row in readme_text:
            about_worksheet.write_row(row_nr, 0, row)
            row_nr += 1

        # === Adjust column width. ===
        about_worksheet.set_column("A:A", 100)

        # === Done. Close the Excel document. ===
        await asyncio.sleep(0.0)

        workbook.close()
