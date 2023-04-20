#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: https://cloudedbats.github.io
# Copyright (c) 2023-present Arnold Andreasson
# License: MIT License (see LICENSE or http://opensource.org/licenses/mit).

import asyncio
import pathlib
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
        self.plot_spectrogram(event.src_path)

    def on_deleted(self, event):
        print("Deleted: " + event.src_path)
        self.delete_spectrogram(event.src_path)

    def on_modified(self, event):
        print("Modified: " + event.src_path)

    def delete_spectrogram(self, rec_file_path):
        """ """
        rec_path = pathlib.Path(self.get_spectrogram_file_path(rec_file_path))
        if rec_path.exists():
            print("Spectrogram deleted: ", rec_path.name)
            rec_path.unlink()
        else:
            print("Spectrogram not found for deletion.")

    def get_spectrogram_file_path(self, rec_file_path):
        """ """
        rec_path_str = str(rec_file_path)
        rec_path_str = rec_path_str.replace(
            "/wurb_recordings",
            "/wurb_cache/spectrograms",
        )
        rec_path_str = rec_path_str.replace(".wav", "_SPECTROGRAM.jpg")
        return str(rec_path_str)

    def plot_spectrogram(self, rec_file_path):
        """ """
        img_file_path = self.get_spectrogram_file_path(
            rec_file_path
        )

        target_dir_path = pathlib.Path(img_file_path).parent
        if not target_dir_path.exists():
            target_dir_path.mkdir()

        print("--- DEBUG: plot_spectrogram - 1.")

        with concurrent.futures.ProcessPoolExecutor() as executor:
        # with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(create_spectrogram, rec_file_path, img_file_path)
            concurrent.futures.wait([future])
            message = str(future.result())
            print("Future: ", message)

        print("--- DEBUG: plot_spectrogram - 2.")


if __name__ == "__main__":
    """ """
    asyncio.run(main())
