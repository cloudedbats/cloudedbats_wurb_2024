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
        self.report_columns = [
            {
                "header": "Prefix",
                "sourceKey": "recording.prefix",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 15,
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
                "header": "detectionAlgorithm",
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
                "header": "deviceName",
                "sourceKey": "recording.deviceName",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 40,
            },
            {
                "header": "geoSource",
                "sourceKey": "recording.geoSource",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 10,
            },
            {
                "header": "maxPeakDbfs",
                "sourceKey": "recording.maxPeakDbfs",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 10,
            },
            {
                "header": "maxPeakFreqHz",
                "sourceKey": "recording.maxPeakFreqHz",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 10,
            },
            {
                "header": "moonPhase",
                "sourceKey": "recording.moonPhase",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 10,
            },
            {
                "header": "recFileName",
                "sourceKey": "recording.recFileName",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 10,
            },
            {
                "header": "schedulerStartEvent",
                "sourceKey": "recording.schedulerStartEvent",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 10,
            },
            {
                "header": "schedulerStartAdjust",
                "sourceKey": "recording.schedulerStartAdjust",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 10,
            },
            {
                "header": "schedulerStopEvent",
                "sourceKey": "recording.schedulerStopEvent",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 10,
            },
            {
                "header": "schedulerStopAdjust",
                "sourceKey": "recording.schedulerStopAdjust",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 10,
            },
            {
                "header": "sunriseLocal",
                "sourceKey": "recording.sunriseLocal",
                # "sourceKeyList": [""],
                # "text": "",
                "format": "text",
                "columnWidth": 10,
            },
            {
                "header": "sunsetLocal",
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

    async def create_report(
        self,
        source_id,
        night_id,
        report_path="EXCEL-TEST.xlsx",
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
        report_worksheet = workbook.add_worksheet("Recordings")
        about_worksheet = workbook.add_worksheet("About")

        # Create cell formats.
        self.bold_format = workbook.add_format({"bold": True})

        # === Sheet: Report. ===
        # Header.
        headers = []
        for column_dict in self.report_columns:
            header = column_dict.get("header", "")
            headers.append(header)
        report_worksheet.write_row(0, 0, headers, self.bold_format)
        # Rows.
        row_nr = 1
        for metadata_row in metadata_rows:
            row = []
            for column_dict in self.report_columns:
                source_key = column_dict.get("sourceKey", "")
                format = column_dict.get("format", "")
                value = metadata_row.get(source_key, "")
                #
                row.append(value)
            #
            report_worksheet.write_row(row_nr, 0, row)
            row_nr += 1

        # === Adjust column width. ===
        index = 0
        for column_dict in self.report_columns:
            width = column_dict.get("columnWidth", 10)
            report_worksheet.set_column(index, index, int(width))
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


###############################
###############################

# class ExcelExportWriter:
#     """ """

#     def __init__(self, sample_object):
#         """ """
#         self.sample_object = sample_object
#         #
#         self.load_overview_mappings()

#     def to_excel(self, export_target_dir, export_target_filename):
#         """Export to Excel."""
#         self.export_target_filename = export_target_filename
#         # Create Excel document.
#         filepathname = pathlib.Path(export_target_dir, export_target_filename)
#         workbook = xlsxwriter.Workbook(filepathname)
#         # Add worksheets.
#         self.summary_worksheet = workbook.add_worksheet("Sample summary")
#         self.sampleinfo_worksheet = workbook.add_worksheet("sample_info.txt")
#         self.sampledata_worksheet = workbook.add_worksheet("sample_data.txt")
#         self.samplemethod_worksheet = workbook.add_worksheet("counting_method.txt")
#         self.readme_worksheet = workbook.add_worksheet("README")
#         # Adjust column width.
#         self.sampleinfo_worksheet.set_column("A:B", 40)
#         self.sampledata_worksheet.set_column("A:C", 30)
#         self.sampledata_worksheet.set_column("D:U", 20)
#         self.samplemethod_worksheet.set_column("A:Q", 30)
#         self.readme_worksheet.set_column("A:A", 100)
#         # Create cell formats.
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

#         # Prepare sample info header and rows.
#         self.sample_data_header = self.sample_object.get_header()
#         self.sample_data_rows = self.sample_object.get_rows()
#         # Prepare method header and rows.
#         self.sample_method_header = []
#         self.sample_method_rows = []
#         sample_path = self.sample_object.get_dir_path()
#         if pathlib.Path(sample_path, "counting_method.txt").exists():
#             (
#                 self.sample_method_header,
#                 self.sample_method_rows,
#             ) = plankton_core.PlanktonCounterMethods().get_counting_method_table(
#                 sample_path, "counting_method.txt"
#             )

#         # === Sheet: Sample info. ===
#         sample_info_header = ["key", "value"]
#         sample_info_header_order = [
#             "plankton_toolbox_version",
#             "sample_name",
#             "sample_id",
#             "sample_date",
#             "sample_time",
#             "visit_year",
#             "country_code",
#             "platform_code",
#             "sampling_series",
#             "sampling_laboratory",
#             "orderer",
#             "project_code",
#             "project_name",
#             "method_documentation",
#             "method_reference_code",
#             "station_name",
#             "station_code",
#             "sample_latitude_dm",
#             "sample_longitude_dm",
#             "sample_latitude_dd",
#             "sample_longitude_dd",
#             "sample_min_depth_m",
#             "sample_max_depth_m",
#             "water_depth_m",
#             "sampler_type_code",
#             "sampled_volume_l",
#             "net_type_code",
#             "sampler_area_m2",
#             "net_mesh_size_um",
#             "wire_angle_deg",
#             "net_tow_length_m",
#             "analytical_laboratory",
#             "analysis_date",
#             "analysed_by",
#             "sample_comment",
#         ]
#         sample_info_rows = []
#         self.sample_info_dict = self.sample_object.get_sample_info()
#         for header_item in sample_info_header_order:
#             sample_info_rows.append(
#                 [header_item, self.sample_info_dict.get(header_item, "")]
#             )
#         # Sample info header.
#         self.sampleinfo_worksheet.write_row(0, 0, sample_info_header, self.bold_format)
#         # Rows.
#         row_nr = 1
#         for row in sample_info_rows:
#             self.sampleinfo_worksheet.write_row(row_nr, 0, row)
#             row_nr += 1
#         # Extra info for restart of counting session.
#         row_nr += 1
#         for key in self.sample_info_dict.keys():
#             if key == "last_used_method_step":
#                 self.sampleinfo_worksheet.write_row(
#                     row_nr, 0, [key, self.sample_info_dict.get(key, "")]
#                 )
#                 row_nr += 1
#             if key.startswith("max_count_area<+>"):
#                 self.sampleinfo_worksheet.write_row(
#                     row_nr, 0, [key, self.sample_info_dict.get(key, "")]
#                 )
#                 row_nr += 1

#         # === Sheet: Sample data. ===
#         self.sampledata_worksheet.title = "sample_data.txt"
#         # Header.
#         self.sampledata_worksheet.write_row(
#             0, 0, self.sample_data_header, self.bold_format
#         )
#         # Rows.
#         row_nr = 1
#         for row in self.sample_data_rows:
#             self.sampledata_worksheet.write_row(row_nr, 0, row)
#             row_nr += 1

#         # === Sheet: Sample method. ===
#         # Header.
#         self.samplemethod_worksheet.write_row(
#             0, 0, self.sample_method_header, self.bold_format
#         )
#         # Rows.
#         row_nr = 1
#         for row in self.sample_method_rows:
#             self.samplemethod_worksheet.write_row(row_nr, 0, row)
#             row_nr += 1

#         # === Sheet: README. ===
#         # Header.
#         self.readme_worksheet.write_row(
#             0, 0, ["Plankton Toolbox - Plankton counter"], self.bold_format
#         )
#         # Rows.
#         readme_text = [
#             [""],
#             ["This Excel file is generated by Plankton Toolbox."],
#             [""],
#             [
#                 "The file represents one counted plankton sample. It can be used for export and import "
#             ],
#             [
#                 "between different computers running Plankton Toolbox, or as an archive file."
#             ],
#             [""],
#             [
#                 "NOTE: Don\"t edit or rename the sheets "sample_info.txt", "sample_data.txt" or "
#             ],
#             [
#                 ""counting_method.txt" if the file should be imported later to Plankton Toolbox."
#             ],
#             [""],
#             ["Generated sheets:"],
#             [
#                 "- Sample summary: Contains information in a compact format. May be used printed for archive purposes."
#             ],
#             [
#                 "- sample_info.txt: Copy of the internally used file for information connected to a sample (metadata)."
#             ],
#             [
#                 "- sample_data.txt: Copy of the internally used file for counted sample rows."
#             ],
#             [
#                 "- counting_method.txt: Copy of the internally used file for parameters related to the counting method."
#             ],
#             ["- README: This text."],
#             [""],
#             [
#                 "More info at: http://nordicmicroalgae.org and http://plankton-toolbox.org "
#             ],
#         ]
#         #
#         row_nr = 1
#         for row in readme_text:
#             self.readme_worksheet.write_row(row_nr, 0, row)
#             row_nr += 1

#         # === Sheet: Sample summary. ===
#         self.create_overview_sheet()

#         # Done. Close the Excel document.
#         workbook.close()

#     def load_overview_mappings(self):
#         """ """
#         self.overview_info_mapping = [
#             ["label", "Plankton Toolbox:", 0, 1, "text"],
#             ["sample_info", "plankton_toolbox_version", 0, 2, "text"],
#             # VISIT.
#             ["label", "SAMPLING EVENT", 2, 1, "text"],
#             ["label", "Station:", 3, 1, "text"],
#             ["sample_info", "station_name", 3, 2, "text"],
#             ["label", "Date:", 4, 1, "text"],
#             ["sample_info", "sample_date", 4, 2, "text"],
#             ["label", "Time:", 5, 1, "text"],
#             ["sample_info", "sample_time", 5, 2, "text"],
#             ["label", "Series:", 6, 1, "text"],
#             ["sample_info", "sampling_series", 6, 2, "text"],
#             ["label", "Platform:", 7, 1, "text"],
#             ["sample_info", "platform_code", 7, 2, "text"],
#             ["label", "Lat/long (DD):", 8, 1, "text"],
#             ["sample_info", "sample_latitude_dd", 8, 2, "text"],  # , "pos_dd"],
#             ["sample_info", "sample_longitude_dd", 8, 3, "text"],  # , "pos_dd"],
#             ["label", "Lat/long (DM):", 9, 1, "text"],
#             ["sample_info", "sample_latitude_dm", 9, 2, "text"],
#             ["sample_info", "sample_longitude_dm", 9, 3, "text"],
#             ["label", "Water depth (m):", 10, 1, "text"],
#             ["sample_info", "water_depth_m", 10, 2, "decimal"],
#             ["label", "Project code:", 11, 1, "text"],
#             ["sample_info", "project_code", 11, 2, "text"],
#             ["label", "Project name:", 12, 1, "text"],
#             ["sample_info", "project_name", 12, 2, "text"],
#             # SAMPLE.
#             ["label", "SAMPLE", 2, 5, "text"],
#             ["label", "Sampler type code:", 3, 5, "text"],
#             ["sample_info", "sampler_type_code", 3, 7, "text"],
#             ["label", "Min depth (m):", 4, 5, "text"],
#             ["sample_info", "sample_min_depth_m", 4, 7, "decimal"],
#             ["label", "Max depth (m):", 5, 5, "text"],
#             ["sample_info", "sample_max_depth_m", 5, 7, "decimal"],
#             ["label", "Analysed by/taxonomist:", 7, 5, "text"],
#             ["sample_info", "analysed_by", 7, 7, "text"],
#             ["label", "Analysis date:", 8, 5, "text"],
#             ["sample_info", "analysis_date", 8, 7, "text"],
#             ["label", "Sample comment:", 9, 5, "text"],
#             ["sample_info", "sample_comment", 9, 7, "text"],
#             ["label", "Sampled volume (l):", 10, 5, "text"],
#             ["sample_info", "sampled_volume_l", 10, 7, "decimal"],
#             # SIGNATURE.
#             ["label", "SIGNATURE", 2, 9, "text"],
#             ["label", "Date:", 4, 9, "text"],
#             ["label", "Institute:", 6, 9, "text"],
#             ["label", "Signature:", 8, 9, "text"],
#         ]
#         self.overview_method_mapping = [
#             # METOD STEP.
#             ["label", "Method step", 15, 1, "text"],
#             ["counting_method", "counting_method_step", 16, 1, "text"],
#             ["label", "Preservative", 15, 3, "text"],
#             ["counting_method", "preservative", 16, 3, "text"],
#             ["label", "Counted volume (ml)", 15, 5, "text_r"],
#             ["counting_method", "counted_volume_ml", 16, 5, "decimal"],
#             ["label", "Microscope", 15, 7, "text"],
#             ["counting_method", "microscope", 16, 7, "text"],
#             ["label", "Magnification", 15, 9, "text_r"],
#             ["counting_method", "magnification", 16, 9, "integer"],
#         ]
#         self.overview_sample_mapping = [
#             ["label", "Class", 15, 1, "text"],
#             ["sample_data", "taxon_class", 15, 1, "text"],
#             ["label", "Scientific name", 15, 2, "text"],
#             ["sample_data", "scientific_full_name", 15, 2, "text"],
#             ["label", "Trophic type", 15, 4, "text"],
#             ["sample_data", "trophic_type", 15, 4, "text"],
#             ["label", "Size class", 15, 5, "text_r"],
#             ["sample_data", "size_class", 15, 5, "integer"],
#             ["label", "Counted", 15, 6, "text_r"],
#             ["sample_data", "counted_units", 15, 6, "integer"],
#             ["label", "Coeff.", 15, 7, "text_r"],
#             ["sample_data", "coefficient", 15, 7, "integer"],
#             ["label", "Abundance (units/l)", 15, 8, "text_r"],
#             ["sample_data", "abundance_units_l", 15, 8, "integer"],
#             ["label", "Volume (mm3/l)", 15, 9, "text_r"],
#             ["sample_data", "volume_mm3_l", 15, 9, "decimal_6"],
#             ["label", "Carbon (ugc/l)", 15, 10, "text_r"],
#             ["sample_data", "carbon_ugc_l", 15, 10, "decimal"],
#             ["label", "Volume/unit (um3)", 15, 11, "text_r"],
#             ["sample_data", "volume_um3_unit", 15, 11, "decimal"],
#             ["label", "Counted trans/views", 15, 12, "text_r"],
#             ["sample_data", "count_area_number", 15, 12, "integer"],
#         ]

#     def create_overview_sheet(self):
#         """ """
#         # Excel page setup.
#         self.summary_worksheet.set_paper(9)  # A4
#         self.summary_worksheet.set_landscape()
#         self.summary_worksheet.fit_to_pages(1, 0)
#         self.summary_worksheet.set_footer(
#             "Plankton Toolbox   -   &F   -   &D &T   -   Page: &P (&N)"
#         )
#         # Image.
#         ### worksheet.insert_image("G2", "plankton_toolbox_icon.png")
#         # Column width.
#         xlsx_layout = [
#             {"columns": "A:A", "width": 2},
#             {"columns": "B:D", "width": 20},
#             {"columns": "E:F", "width": 12},
#             {"columns": "G:G", "width": 20},
#             {"columns": "H:H", "width": 10},
#             {"columns": "I:I", "width": 20},
#             {"columns": "J:K", "width": 15},
#             {"columns": "L:M", "width": 20},
#         ]
#         for row in xlsx_layout:
#             if ("columns" in row.keys()) and ("width" in row.keys()):
#                 self.summary_worksheet.set_column(row["columns"], row["width"])
#         #
#         method_steps_dict = {}
#         for data in self.sample_method_rows:
#             # print(index)
#             step_dict = dict(zip(self.sample_method_header, data))
#             method_steps_dict[step_dict["counting_method_step"]] = step_dict
#         # Write file name.
#         self.summary_worksheet.write(
#             0, 3, self.export_target_filename, self.bold_format
#         )
#         #
#         for row in self.overview_info_mapping:
#             source, field, cell_row, cell_col, cell_format = row

#             try:
#                 value = ""
#                 if source == "label":
#                     if cell_format == "text_r":
#                         self.summary_worksheet.write(
#                             cell_row, cell_col, field, self.bold_right_format
#                         )
#                     else:
#                         self.summary_worksheet.write(
#                             cell_row, cell_col, field, self.bold_format
#                         )

#                 elif source == "sample_info":
#                     if field in self.sample_info_dict:
#                         value = self.sample_info_dict[field]

#                         cell_style_obj = None
#                         if cell_format == "integer":
#                             cell_style_obj = self.integer_format
#                             if value != "":
#                                 value = int(float(value))
#                         elif cell_format == "decimal":
#                             cell_style_obj = self.decimal_format
#                             if value != "":
#                                 value = float(value)
#                         elif cell_format == "decimal_6":
#                             cell_style_obj = self.decimal_6_format
#                             if value != "":
#                                 value = float(value)
#                         elif cell_format == "pos_dd":
#                             cell_style_obj = self.latlong_dd_format
#                             if value != "":
#                                 value = float(value)
#                         #
#                         self.summary_worksheet.write(
#                             cell_row, cell_col, value, cell_style_obj
#                         )

#             except:
#                 print(row)

#             # Methods and row data.
#             row_offset = 0
#             header = True
#             last_used_method_step = "not defined"

#             # Sort order: method_step, "scientific_full_name, size_class.
#             sorted_data_rows = self.sample_data_rows.copy()
#             sorted_data_rows.sort(key=operator.itemgetter(4, 0, 3))

#             for data_row in sorted_data_rows:

#                 data_row_dict = dict(zip(self.sample_data_header, data_row))
#                 used_method_step = data_row_dict.get("method_step", "")
#                 if used_method_step:
#                     method_dict = method_steps_dict[used_method_step]
#                 else:
#                     method_dict = {}
#                 # New method step.
#                 if used_method_step != last_used_method_step:
#                     row_offset += 1
#                     self.overview_sheet_method(method_dict, row_offset)
#                     row_offset += 3
#                     header = True
#                     last_used_method_step = used_method_step
#                 # Header for data rows.
#                 if header:
#                     self.overview_sheet_data(data_row_dict, row_offset, header)
#                     header = False
#                     row_offset += 1
#                 # Data rows.
#                 self.overview_sheet_data(data_row_dict, row_offset, header)
#                 row_offset += 1

#     def overview_sheet_method(self, method_dict, row_offset):
#         """ """
#         for row in self.overview_method_mapping:
#             source, field, cell_row, cell_col, cell_format = row

#             try:
#                 value = ""
#                 if source == "label":
#                     if cell_format == "text_r":
#                         self.summary_worksheet.write(
#                             cell_row + row_offset,
#                             cell_col,
#                             field,
#                             self.bold_right_format,
#                         )
#                     else:
#                         self.summary_worksheet.write(
#                             cell_row + row_offset, cell_col, field, self.bold_format
#                         )

#                 elif source == "counting_method":
#                     if field in method_dict:
#                         value = method_dict[field]

#                         cell_style_obj = None
#                         if cell_format == "integer":
#                             cell_style_obj = self.integer_format
#                             if value != "":
#                                 value = int(float(value))
#                                 # Don"t write zero values.
#                                 if value == 0:
#                                     value = ""
#                                     cell_style_obj = None
#                         elif cell_format == "decimal":
#                             cell_style_obj = self.decimal_format
#                             if value != "":
#                                 value = float(value)
#                                 # Don"t write zero values.
#                                 if value == 0.0:
#                                     value = ""
#                                     cell_style_obj = None
#                         elif cell_format == "decimal_6":
#                             cell_style_obj = self.decimal_6_format
#                             if value != "":
#                                 value = float(value)
#                                 # Don"t write zero values.
#                                 if value == 0.0:
#                                     value = ""
#                                     cell_style_obj = None
#                         #
#                         self.summary_worksheet.write(
#                             cell_row + row_offset, cell_col, value, cell_style_obj
#                         )
#             #
#             except Exception as e:
#                 print(str(row), "   Exception: ", str(e))

#     def overview_sheet_data(self, sample_data_dict, row_offset, header=True):
#         """ """
#         for row in self.overview_sample_mapping:
#             source, field, cell_row, cell_col, cell_format = row

#             try:
#                 value = ""
#                 if header:
#                     if source == "label":
#                         if cell_format == "text_r":
#                             self.summary_worksheet.write(
#                                 cell_row + row_offset,
#                                 cell_col,
#                                 field,
#                                 self.bold_right_format,
#                             )
#                         else:
#                             self.summary_worksheet.write(
#                                 cell_row + row_offset, cell_col, field, self.bold_format
#                             )
#                 else:
#                     if source == "sample_data":
#                         if field in sample_data_dict:
#                             value = sample_data_dict[field]

#                             # Special for qualitative analysis.
#                             if (field == "counted_units") and (value == ""):
#                                 value = sample_data_dict["abundance_class"]
#                                 #
#                                 if value == "1":
#                                     value = "1 (Observed)"
#                                 elif value == "2":
#                                     value = "2 (Several cells)"
#                                 elif value == "3":
#                                     value = "3 (1-10%)"
#                                 elif value == "4":
#                                     value = "4 (10-50%)"
#                                 elif value == "5":
#                                     value = "5 (50-100%)"
#                                 #
#                                 cell_format = "text"
#                             #
#                             cell_style_obj = None
#                             if cell_format == "integer":
#                                 cell_style_obj = self.integer_format
#                                 if value != "":
#                                     value = int(float(value))
#                                     # Don"t write zero values.
#                                     if value == 0:
#                                         value = ""
#                                         cell_style_obj = None
#                             elif cell_format == "decimal":
#                                 cell_style_obj = self.decimal_format
#                                 if value != "":
#                                     value = float(value)
#                                     # Don"t write zero values.
#                                     if value == 0.0:
#                                         value = ""
#                                         cell_style_obj = None
#                             elif cell_format == "decimal_6":
#                                 cell_style_obj = self.decimal_6_format
#                                 if value != "":
#                                     value = float(value)
#                                     # Don"t write zero values.
#                                     if value == 0.0:
#                                         value = ""
#                                         cell_style_obj = None
#                             #
#                             self.summary_worksheet.write(
#                                 cell_row + +row_offset, cell_col, value, cell_style_obj
#                             )
#             #
#             except Exception as e:
#                 print(str(row), "   Exception: ", str(e))


###############################
###############################
# def define_headers(self):
#         """ """
#         self.chiroptera_summary_header = [
#             "family",
#             "genus",
#             "scientific_name",
#             "main_common_name",
#             "category",
#             "countries",
#         ]
#         #
#         self.chiroptera_checklist_header = [
#             "scientific_name",
#             "taxonid",
#         ]
#         #
#         self.chiroptera_info_header = [
#             "scientific_name",
#             "taxonid",
#             "kingdom",
#             "phylum",
#             "class",
#             "order",
#             "family",
#             "genus",
#             "main_common_name",
#             "authority",
#             "published_year",
#             "category",
#             "criteria",
#             "marine_system",
#             "freshwater_system",
#             "terrestrial_system",
#             "aoo_km2",
#             "eoo_km2",
#             "elevation_upper",
#             "elevation_lower",
#             "depth_upper",
#             "depth_lower",
#             "assessor",
#             "reviewer",
#             "errata_flag",
#             "errata_reason",
#             "amended_flag",
#             "amended_reason",
#         ]
#         #
#         self.country_header = [
#             "isocode",
#             "country",
#         ]
#         #
#         self.chiroptera_by_country_header = [
#             "country_isocode",
#             "taxonid",
#             "scientific_name",
#             "category",
#         ]


#     def create_excel(self, dirpath="."):
#         """ Export to Excel. """
#         #
#         excel_filepathname = pathlib.Path(
#             dirpath, "redlist_chiroptera_" + self.get_redlist_version() + ".xlsx"
#         )
#         # Create Excel document.
#         workbook = xlsxwriter.Workbook(str(excel_filepathname))

#         # Add worksheets.
#         summary_worksheet = workbook.add_worksheet("Chiroptera summary")
#         info_worksheet = workbook.add_worksheet("Chiroptera info")
#         countries_worksheet = workbook.add_worksheet("Countries")
#         species_by_country_worksheet = workbook.add_worksheet("Chiroptera by country")
#         citation_worksheet = workbook.add_worksheet("Citation")
#         about_worksheet = workbook.add_worksheet("About")

#         # Create cell formats.
#         self.bold_format = workbook.add_format({"bold": True})

#         # === Sheet: Chiroptera summary. ===
#         # Header.
#         summary_worksheet.write_row(
#             0, 0, self.chiroptera_summary_header, self.bold_format
#         )
#         # Rows.
#         row_nr = 1
#         for key in sorted(self.chiroptera_info_dict.keys()):
#             species_dict = self.chiroptera_info_dict[key]
#             row = []
#             for item in self.chiroptera_summary_header:
#                 value = str(species_dict.get(item, ""))
#                 if value == "None":
#                     value = ""
#                 elif item == "family":
#                     value = value.capitalize()
#                 elif item == "countries":
#                     countries = []
#                     taxonid = species_dict.get("taxonid", "")
#                     for country_row in self.chiroptera_by_country_list:
#                         if country_row[1] == taxonid:
#                             countries.append(country_row[0])
#                     value = ", ".join(sorted(countries))
#                 #
#                 row.append(value)
#             #
#             summary_worksheet.write_row(row_nr, 0, row)
#             row_nr += 1

#         # === Sheet: Chiroptera info. ===
#         # Header.
#         info_worksheet.write_row(0, 0, self.chiroptera_info_header, self.bold_format)
#         # Rows.
#         row_nr = 1
#         for key in sorted(self.chiroptera_info_dict.keys()):
#             species_dict = self.chiroptera_info_dict[key]
#             row = []
#             for item in self.chiroptera_info_header:
#                 value = str(species_dict.get(item, ""))
#                 if value == "None":
#                     value = ""
#                 row.append(value)
#             #
#             info_worksheet.write_row(row_nr, 0, row)
#             row_nr += 1

#         # === Sheet: Countries. ===
#         # Header.
#         countries_worksheet.write_row(0, 0, self.country_header, self.bold_format)
#         # Rows.
#         row_nr = 1
#         for key in sorted(self.country_dict.keys()):
#             countries_worksheet.write_row(row_nr, 0, [key, self.country_dict[key]])
#             row_nr += 1

#         # === Sheet: Chiroptera by country. ===
#         # Header.
#         species_by_country_worksheet.write_row(
#             0, 0, self.chiroptera_by_country_header, self.bold_format
#         )
#         # Rows.
#         row_nr = 1
#         for row in sorted(self.chiroptera_by_country_list):
#             species_by_country_worksheet.write_row(row_nr, 0, row)
#             row_nr += 1

#         # === Sheet: Citation. ===
#         # Header.
#         citation_worksheet.write_row(0, 0, ["IUCN Redlist citation"], self.bold_format)
#         # Rows.
#         readme_text = [
#             [""],
#             ["IUCN Redlist citation:"],
#             [""],
#             ["    " + self.get_redlist_citation()],
#             [""],
#         ]
#         #
#         row_nr = 1
#         for row in readme_text:
#             citation_worksheet.write_row(row_nr, 0, row)
#             row_nr += 1

#         # === Sheet: Source code. ===
#         # Header.
#         about_worksheet.write_row(0, 0, ["About"], self.bold_format)
#         # Rows.
#         readme_text = [
#             [""],
#             ["This Excel file is a part of the open source "],
#             ["project CloudedBats.org: http://cloudedbats.org "],
#             [""],
#             ["Source code to generate the Excel file can be "],
#             ["found in this GitHub repository: "],
#             ["- https://github.com/cloudedbats/cloudedbats_species "],
#             [""],
#             ["Notes: "],
#             ["- You must ask IUCN for a personal token to access "],
#             ["  their API: https://apiv3.iucnredlist.org/api/v3/token "],
#             ["- Commercial use of the Red List API is not allowed. "],
#             ["- Do not forget the acknowledgement and citation text "],
#             ["  when using it. "],
#             [""],
#         ]
#         #
#         row_nr = 1
#         for row in readme_text:
#             about_worksheet.write_row(row_nr, 0, row)
#             row_nr += 1

#         # === Adjust column width. ===
#         summary_worksheet.set_column("A:B", 20)
#         summary_worksheet.set_column("C:D", 40)
#         summary_worksheet.set_column("E:E", 10)
#         summary_worksheet.set_column("F:F", 40)

#         info_worksheet.set_column("A:A", 40)

#         countries_worksheet.set_column("A:A", 20)
#         countries_worksheet.set_column("B:B", 40)

#         species_by_country_worksheet.set_column("A:B", 20)
#         species_by_country_worksheet.set_column("C:C", 40)
#         species_by_country_worksheet.set_column("D:D", 20)

#         citation_worksheet.set_column("A:A", 100)
#         about_worksheet.set_column("A:A", 100)

#         # === Done. Close the Excel document. ===
#         workbook.close()
