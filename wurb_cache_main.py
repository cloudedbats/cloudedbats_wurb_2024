#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: https://cloudedbats.github.io
# Copyright (c) 2023-present Arnold Andreasson
# License: MIT License (see LICENSE or http://opensource.org/licenses/mit).

import asyncio
import pathlib
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import concurrent.futures

from wurb_core.annotations.spectrogram import create_spectrogram


async def main():
    """ """
    rec_path = pathlib.Path("../wurb_recordings")
    cache_path = pathlib.Path("../wurb_cache")
    spectrograms_path = pathlib.Path(cache_path, "spectrograms")

    event_handler = FileCreateHandler()
    # Create an observer.
    observer = Observer()
    # Attach the observer to the event handler.
    # observer.schedule(event_handler, ".", recursive=True)
    observer.schedule(event_handler, rec_path, recursive=True)
    # Start the observer.
    observer.start()
    try:
        while observer.is_alive():
            observer.join(10)
    finally:
        observer.stop()
        observer.join()


class FileCreateHandler(FileSystemEventHandler):
    def on_created(self, event):
        print("Created: " + event.src_path)
        ### May be called too early, use on_modified.
        ### self.plot_spectrogram(event.src_path)

    def on_deleted(self, event):
        print("Deleted: " + event.src_path)
        self.delete_spectrogram(event.src_path)

    def on_modified(self, event):
        print("Modified: " + event.src_path)
        self.plot_spectrogram(event.src_path)

    def delete_spectrogram(self, rec_file_path):
        """ """
        rec_path = pathlib.Path(rec_file_path)
        if rec_path.suffix == ".wav":
            spectrogram_path = self.get_spectrogram_path_by_rec(rec_file_path)
            if spectrogram_path.exists():
                print("Spectrogram deleted: ", spectrogram_path.name)
                spectrogram_path.unlink()
            else:
                print("Spectrogram not found for deletion.")

    def plot_spectrogram(self, rec_file_path):
        """ """
        rec_path = pathlib.Path(rec_file_path)
        if rec_path.suffix == ".wav":
            spectrogram_path = self.get_spectrogram_path_by_rec(rec_file_path)
            # Create dir.
            target_dir_path = spectrogram_path.parent
            if not target_dir_path.exists():
                target_dir_path.mkdir(parents=True)
            # Check if already done.
            if not spectrogram_path.exists():
                print("--- DEBUG: Plot-1: ", spectrogram_path.name)
                # Wait to avoid multiple on_modified calls,
                # similar events in queue will be merged by watchdog.
                # Also to avoid reading wave file too early.
                time.sleep(2.0)
                print("--- DEBUG: Plot-2: ", spectrogram_path.name)
                with concurrent.futures.ProcessPoolExecutor() as executor:
                    # with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(
                        create_spectrogram, str(rec_file_path), str(spectrogram_path)
                    )
                    concurrent.futures.wait([future])
                    message = str(future.result())
                    print("--- DEBUG: Future-3: ", message)
                print("--- DEBUG: Plot-4: ", spectrogram_path.name)

    def get_spectrogram_path_by_rec(self, rec_file_path):
        """ """
        rec_path_str = str(rec_file_path)
        rec_path_str = rec_path_str.replace(
            "/wurb_recordings",
            "/wurb_cache/spectrograms",
        )
        rec_path_str = rec_path_str.replace(".wav", "_SPECTROGRAM.jpg")
        return pathlib.Path(rec_path_str)


if __name__ == "__main__":
    """ """
    asyncio.run(main())
