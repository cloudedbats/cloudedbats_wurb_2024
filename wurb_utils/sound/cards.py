#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org, https://github.com/cloudedbats
# Copyright (c) 2023-present Arnold Andreasson
# License: MIT License (see LICENSE or http://opensource.org/licenses/mit).

import logging
try:
    import alsaaudio
except: pass

class SoundCards:
    """ """

    def __init__(self, logger="DefaultLogger"):
        """ """
        self.logger = logging.getLogger(logger)
        self.clear()

    def clear(self):
        self.card_list = []
        self.capture_card_index_list = []
        self.playback_card_index_list = []

    def update_card_lists(self):
        """ """
        self.clear()
        # List cards and names.
        # Note: Results from card_indexes() and cards() must be mapped.
        card_ids = alsaaudio.cards()
        for id_index, card_index in enumerate(alsaaudio.card_indexes()):
            card_dict = {}
            card_dict["card_index"] = card_index
            card_dict["card_id"] = card_ids[id_index]
            card_name, long_name = alsaaudio.card_name(card_index)
            card_dict["card_name"] = card_name.strip()
            card_dict["card_long_name"] = long_name.strip()
            self.card_list.append(card_dict)
        # Check card devices for capture.
        for device in alsaaudio.pcms(alsaaudio.PCM_CAPTURE):
            if device.startswith("sysdefault:CARD="):
                card_id = device.replace("sysdefault:CARD=", "").strip()
                for card_dict in self.card_list:
                    if card_dict.get("card_id", "") == card_id:
                        card_dict["device"] = device
                        card_index = card_dict.get("card_index", "")
                        if card_index != "":
                            self.capture_card_index_list.append(card_index)
        # Check card devices for playback.
        for device in alsaaudio.pcms(alsaaudio.PCM_PLAYBACK):
            if device.startswith("sysdefault:CARD="):
                card_id = device.replace("sysdefault:CARD=", "").strip()
                for card_dict in self.card_list:
                    if card_dict.get("card_id", "") == card_id:
                        card_dict["device"] = device
                        card_index = card_dict.get("card_index", "")
                        if card_index != "":
                            self.playback_card_index_list.append(card_index)
        # For debug.
        for card_dict in self.card_list:
            card_name = card_dict.get("card_name", "")
            card_index = card_dict.get("card_index", "")
            self.logger.debug(
                "Sound card: " + card_name + "   Index: " + str(card_index)
            )
        self.logger.debug("Sound cards capture: " + str(self.capture_card_index_list))
        self.logger.debug("Sound cards playback: " + str(self.playback_card_index_list))

    def get_capture_card_index_by_name(self, part_of_name):
        """Returns first found."""
        for card_dict in self.card_list:
            card_name = card_dict.get("card_name", "")
            card_index = card_dict.get("card_index", "")
            if card_index in self.capture_card_index_list:
                if part_of_name in card_name:
                    return card_index
        return None

    def get_playback_card_index_by_name(self, part_of_name):
        """Returns first found."""
        for card_dict in self.card_list:
            card_name = card_dict.get("card_name", "")
            card_index = card_dict.get("card_index", "")
            if card_index in self.playback_card_index_list:
                if part_of_name in card_name:
                    return card_index
        return None

    def get_card_dict_by_index(self, card_index):
        """Returns first found."""
        for card_dict in self.card_list:
            if card_index == card_dict.get("card_index", ""):
                return card_dict
        return {}

    def get_max_sampling_freq(self, card_index):
        """Only for capture devices."""
        max_freq = -99
        inp = None
        try:
            try:
                inp = alsaaudio.PCM(
                    alsaaudio.PCM_CAPTURE,
                    alsaaudio.PCM_NORMAL,
                    channels=1,
                    format=alsaaudio.PCM_FORMAT_S16_LE,
                    device="sysdefault",
                    cardindex=card_index,
                )
                # Rates may be list, tuple or a single value.
                rates = inp.getrates()
                if type(rates) in [list, tuple]:
                    max_freq = inp.getrates()[-1]
                else:
                    max_freq = inp.getrates()
            except Exception as e:
                self.logger.debug("Exception: " + str(e))
        finally:
            if inp:
                inp.close()
        return max_freq
