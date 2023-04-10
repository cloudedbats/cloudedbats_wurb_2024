#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: https://cloudedbats.github.io, https://github.com/cloudedbats
# Copyright (c) 2023-present Arnold Andreasson
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import asyncio
import concurrent.futures
import logging
import pathlib
import yaml
import matplotlib
import matplotlib.figure
from scipy import signal
from scipy.io import wavfile
import numpy
import gc

import wurb_core


class SpectrogramGenerator:
    """ """

    def __init__(self, config=None, logger=None, logger_name="DefaultLogger"):
        """ """
        if config == None:
            self.config = {}
        else:
            self.config = config
        if logger == None:
            self.logger = logging.getLogger(logger_name)
        else:
            self.logger = logger
        #
        self.clear()

    def clear(self):
        """ """
        # Plot.
        self.figure = None
        self.ax1 = None

    def generate_spectrogram_in_executor(self, rec_file_path):
        """ """
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(self.generate_spectrogram, rec_file_path)
            print(future.result())

    def generate_spectrogram(self, rec_file_path):
        """ """
        img_file_path = wurb_core.record_manager.get_spectrogram_file_path(
            rec_file_path
        )
        img_file_path = pathlib.Path(img_file_path)

        if pathlib.Path(img_file_path).exists():
            print("Spectrogram already generated. Skipped.")
            return

        if not img_file_path.parent.exists():
            img_file_path.parent.mkdir(parents=True)

        self.create_spectrogram(rec_file_path, img_file_path)

        return "Spectrogram generated: " + img_file_path.name

    def init_matplotlib(self):
        """ """
        matplotlib.rcParams.update({"font.size": 6})
        self.figure = matplotlib.figure.Figure(
            figsize=(10, 3),
            # dpi=500,
            dpi=400,
            # Plot figure.
        )
        self.ax1 = self.figure.add_subplot(111)

    def create_spectrogram(self, source_path, target_path):
        """ """
        if pathlib.Path(target_path).exists():
            print("Already done. Skipped.")
            return

        if self.figure == None:
            self.init_matplotlib()

        try:
            sample_rate, samples = wavfile.read(source_path)
            # Change from time expanded, TE, to full scan, FS.
            if sample_rate < 90000:
                sample_rate *= 10

            start_ix = int(sample_rate * 4.7)
            end_ix = int(sample_rate * 4.9)
            start_ix = int(sample_rate * 2.0)
            end_ix = int(sample_rate * 2.5)

            # Calculate spectrogram.
            frequencies, times, spectrogram = signal.spectrogram(
                samples,
                # samples[start_ix:end_ix],
                sample_rate,
                window="blackmanharris",
                nperseg=1024,
                noverlap=768,
                # nperseg=512,
                # noverlap=400,
            )
            # From Hz to kHz.
            frequencies = frequencies / 1000.0
            # Fix colours, use logarithmic scale.

            for row in spectrogram:
                row[row < 0.001] = None

            ### Available color maps. ###
            # 'Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r',
            # 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r',
            # 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r',
            # 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r',
            # 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r',
            # 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r',
            # 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r',
            # 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r',
            # 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r',
            # 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix', 'cubehelix_r',
            # 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat', 'gist_heat_r', 'gist_ncar',
            # 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot',
            # 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno', 'inferno_r', 'jet',
            # 'jet_r', 'magma', 'magma_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma',
            # 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer',
            # 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r',
            # 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r',
            # 'viridis', 'viridis_r', 'winter', 'winter_r'

            self.ax1.grid(False)
            self.ax1.pcolormesh(
                times, frequencies, numpy.log10(spectrogram), cmap="YlOrBr"
            )

            # Title and labels.
            self.ax1.set_title(
                "File: " + str(pathlib.Path(source_path).name), fontsize=8
            )
            # Axes.
            self.ax1.set_ylabel("Frequency (kHz)")
            self.ax1.set_xlabel("Time (s)")
            self.ax1.set_ylim((0, 100))
            # Grid.
            self.ax1.minorticks_on()
            self.ax1.grid(which="major", linestyle="-", linewidth="0.5", alpha=0.7)
            self.ax1.grid(which="minor", linestyle="-", linewidth="0.5", alpha=0.3)
            self.ax1.tick_params(
                which="both", top="off", left="off", right="off", bottom="off"
            )
            # Save.
            self.figure.tight_layout()
            self.figure.savefig(target_path)
            self.ax1.cla()
            # Run garbage collector to avoid memory overload.
            gc.collect()

        except Exception as e:
            message = "SpectrogramGenerator - create_spectrogram. Exception: " + e
            self.logger.debug(message)
