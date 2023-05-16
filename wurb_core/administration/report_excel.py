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
                "format": "text",
                "columnWidth": 30,
            },
            {
                "header": "Date",
                "sourceKey": "recording.dateLocal",
                "format": "date",
                "columnWidth": 10,
            },
            {
                "header": "Time",
                "sourceKey": "recording.timeLocal",
                "format": "time",
                "columnWidth": 10,
            },
            {
                "header": "Quality",
                "sourceKey": "annotations.wurb-user.quality",
                "format": "text",
                "columnWidth": 15,
            },
            {
                "header": "Tags",
                "sourceKey": "annotations.wurb-user.tags",
                "format": "text",
                "columnWidth": 20,
            },
            {
                "header": "Comments",
                "sourceKey": "annotations.wurb-user.comments",
                "format": "text",
                "columnWidth": 40,
            },
            {
                "header": "Peak (kHz)",
                "sourceKey": "recording.peakKhz",
                "format": "decimal",
                "columnWidth": 10,
            },
            {
                "header": "Peak (dBFS)",
                "sourceKey": "recording.peakDbfs",
                "format": "decimal",
                "columnWidth": 10,
            },
            {
                "header": "Latitude (DD)",
                "sourceKey": "recording.latitude",
                "format": "decimal_4",
                "columnWidth": 12,
            },
            {
                "header": "Longitude (DD)",
                "sourceKey": "recording.longitude",
                "format": "decimal_4",
                "columnWidth": 12,
            },
            {
                "header": "File name",
                "sourceKey": "recording.recFileName",
                "format": "text",
                "columnWidth": 60,
            },
        ]
        self.detailed_columns = [
            {
                "header": "Monitoring night",
                "sourceKey": "recording.monitoringNight",
                "format": "text",
                "columnWidth": 30,
            },
            {
                "header": "Date",
                "sourceKey": "recording.dateLocal",
                "format": "date",
                "columnWidth": 10,
            },
            {
                "header": "Time",
                "sourceKey": "recording.timeLocal",
                "format": "time",
                "columnWidth": 10,
            },
            {
                "header": "Quality",
                "sourceKey": "annotations.wurb-user.quality",
                "format": "text",
                "columnWidth": 15,
            },
            {
                "header": "Tags",
                "sourceKey": "annotations.wurb-user.tags",
                "format": "text",
                "columnWidth": 20,
            },
            {
                "header": "Comments",
                "sourceKey": "annotations.wurb-user.comments",
                "format": "text",
                "columnWidth": 40,
            },
            {
                "header": "Peak (kHz)",
                "sourceKey": "recording.peakKhz",
                "format": "decimal",
                "columnWidth": 10,
            },
            {
                "header": "Peak (dBFS)",
                "sourceKey": "recording.peakDbfs",
                "format": "decimal",
                "columnWidth": 10,
            },
            {
                "header": "Latitude (DD)",
                "sourceKey": "recording.latitude",
                "format": "decimal_4",
                "columnWidth": 12,
            },
            {
                "header": "Longitude (DD)",
                "sourceKey": "recording.longitude",
                "format": "decimal_4",
                "columnWidth": 12,
            },
            {
                "header": "File name",
                "sourceKey": "recording.recFileName",
                "format": "text",
                "columnWidth": 60,
            },
            {
                "header": "Device name",
                "sourceKey": "recording.deviceName",
                "format": "text",
                "columnWidth": 40,
            },
            {
                "header": "Detection algorithm",
                "sourceKey": "recording.detectionAlgorithm",
                "format": "text",
                "columnWidth": 15,
            },
            {
                "header": "Limit kHz",
                "sourceKey": "recording.detectionLimitKhz",
                "format": "decimal",
                "columnWidth": 15,
            },
            {
                "header": "Sensitivity dBFS",
                "sourceKey": "recording.detectionSensitivityDbfs",
                "format": "decimal",
                "columnWidth": 15,
            },
            {
                "header": "Datetime UTC",
                "sourceKey": "recording.dateTimeUtc",
                "format": "text",
                "columnWidth": 25,
            },
            {
                "header": "Geo source",
                "sourceKey": "recording.geoSource",
                "format": "text",
                "columnWidth": 15,
            },
            {
                "header": "Scheduler start event",
                "sourceKey": "recording.schedulerStartEvent",
                "format": "text",
                "columnWidth": 15,
            },
            {
                "header": "Scheduler start adjust",
                "sourceKey": "recording.schedulerStartAdjust",
                "format": "decimal",
                "columnWidth": 15,
            },
            {
                "header": "Scheduler stop event",
                "sourceKey": "recording.schedulerStopEvent",
                "format": "text",
                "columnWidth": 15,
            },
            {
                "header": "Scheduler stop adjust",
                "sourceKey": "recording.schedulerStopAdjust",
                "format": "decimal",
                "columnWidth": 15,
            },
            {
                "header": "Sunset local",
                "sourceKey": "recording.sunsetLocal",
                "format": "time",
                "columnWidth": 15,
            },
            {
                "header": "Sunrise local",
                "sourceKey": "recording.sunriseLocal",
                "format": "time",
                "columnWidth": 15,
            },
            {
                "header": "Moon phase",
                "sourceKey": "recording.moonPhase",
                "format": "text",
                "columnWidth": 15,
            },
        ]

    def get_report_path(self, source_id, night_id):
        """ """
        report_path = ""
        if (source_id) and (night_id):
            source_dir = pathlib.Path(
                wurb_core.record_manager.get_source_dir(source_id)
            )
            data_dir = pathlib.Path(source_dir, night_id, "data")
            if not data_dir.exists():
                data_dir.mkdir(parents = True)
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
            # Get metadata for recording.
            metadata = wurb_core.metadata.get_metadata(rec_file)
            flat_metadata = wurb_core.metadata.flatten_metadata(metadata)
            metadata_rows.append(flat_metadata)

        # Create Excel workbook.
        await asyncio.sleep(0.0)
        workbook = xlsxwriter.Workbook(str(report_path))
        self.define_cell_formats(workbook)

        # Summary worksheets.
        summary_worksheet = workbook.add_worksheet("Summary")
        self.add_content(summary_worksheet, metadata_rows, self.summary_columns)
        # Detailed worksheets.
        detailed_worksheet = workbook.add_worksheet("Detailed")
        self.add_content(detailed_worksheet, metadata_rows, self.detailed_columns)
        # About worksheets.
        about_worksheet = workbook.add_worksheet("About")
        self.add_about_content(about_worksheet)

        # === Done. Close workbook. ===
        await asyncio.sleep(0.0)
        workbook.close()

    def add_content(self, worksheet, metadata_rows, columns):
        """ """
        # Header.
        headers = []
        for column_dict in columns:
            header = column_dict.get("header", "")
            headers.append(header)
        #
        worksheet.write_row(0, 0, headers, self.format_bold)
        # Rows.
        for row_nr, metadata_row in enumerate(metadata_rows):
            for column_nr, column_dict in enumerate(columns):
                source_key = column_dict.get("sourceKey", "")
                value = metadata_row.get(source_key, "")
                format = column_dict.get("format", "")
                if format == "integer":
                    try:
                        value_int = int(round(float(value), 0))
                        worksheet.write_number(
                            row_nr + 1, column_nr, value_int, self.format_integer
                        )
                    except:
                        worksheet.write_blank(
                            row_nr + 1, column_nr, "", self.format_integer
                        )
                elif format == "decimal":
                    try:
                        value_float = float(value)
                        worksheet.write_number(
                            row_nr + 1, column_nr, value_float, self.format_decimal
                        )
                    except:
                        worksheet.write_blank(
                            row_nr + 1, column_nr, "", self.format_decimal
                        )
                elif format == "decimal_2":
                    try:
                        value_float = float(value)
                        worksheet.write_number(
                            row_nr + 1, column_nr, value_float, self.format_decimal_2
                        )
                    except:
                        worksheet.write_blank(
                            row_nr + 1, column_nr, "", self.format_decimal_2
                        )
                elif format == "decimal_4":
                    try:
                        value_float = float(value)
                        worksheet.write_number(
                            row_nr + 1, column_nr, value_float, self.format_decimal_4
                        )
                    except:
                        worksheet.write_blank(
                            row_nr + 1, column_nr, "", self.format_decimal_4
                        )
                elif format == "decimal_6":
                    try:
                        value_float = float(value)
                        worksheet.write_number(
                            row_nr + 1, column_nr, value_float, self.format_decimal_6
                        )
                    except:
                        worksheet.write_blank(
                            row_nr + 1, column_nr, "", self.format_decimal_6
                        )
                elif format == "date":
                    try:
                        worksheet.write(row_nr + 1, column_nr, value, self.format_date)
                    except:
                        worksheet.write_blank(
                            row_nr + 1, column_nr, "", self.format_date
                        )
                elif format == "time":
                    try:
                        worksheet.write(row_nr + 1, column_nr, value, self.format_time)
                    except:
                        worksheet.write_blank(
                            row_nr + 1, column_nr, "", self.format_time
                        )
                else:
                    value_str = str(value)
                    worksheet.write_string(row_nr + 1, column_nr, value_str)

        # === Adjust column width. ===
        index = 0
        for column_dict in columns:
            width = column_dict.get("columnWidth", 10)
            worksheet.set_column(index, index, int(width))
            index += 1

    def add_about_content(self, worksheet):
        """ """
        # === Sheet: About. ===
        # Header.
        worksheet.write_row(0, 0, ["About"], self.format_bold)
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
            worksheet.write_row(row_nr, 0, row)
            row_nr += 1

        # === Adjust column width. ===
        worksheet.set_column("A:A", 100)

    def define_cell_formats(self, workbook):
        """ """
        self.format_bold = workbook.add_format({"bold": True})
        #
        self.format_bold_right = workbook.add_format({"bold": True, "align": "right"})
        #
        self.format_date = workbook.add_format()
        self.format_date.set_num_format("yyyy-mm-dd")
        #
        self.format_time = workbook.add_format()
        self.format_time.set_num_format("hh:mm:ss")
        #
        self.format_integer = workbook.add_format()
        self.format_integer.set_num_format("0")
        #
        self.format_decimal = workbook.add_format()
        self.format_decimal.set_num_format("0.0")
        #
        self.format_decimal_2 = workbook.add_format()
        self.format_decimal_2.set_num_format("0.00")
        #
        self.format_decimal_4 = workbook.add_format()
        self.format_decimal_4.set_num_format("0.0000")
        #
        self.format_decimal_6 = workbook.add_format()
        self.format_decimal_6.set_num_format("0.000000")
