# CloudedBats WURB-2023

Next major release - work in progress...

## For ordinary users

Please use the older version called CloudedBats WURB-2020.
That one is well tested by many users and works well both as a mobile detector
as well as for stationary use.

More info here:
https://github.com/cloudedbats/cloudedbats_wurb_2020

## What to expect

The functionality in the bat detector part is mainly the same as in the WURB-2020 version.
There are some changes in the user interface to make it easier to extend with new functionality
and add more settings options.

A new page for "Field annotations" is added where it is possible to check an automatically
generated spectrogram and assign quality stamps, tags and to add comments on each recorded file.

Another page called "Administration" can then use this information in various ways.
For example, it will be possible to remove trash files directly in the detector,
or to generate an Excel report containing field notes, etc.

## For developers

The code is reorganized and some parts are completely rewritten.
Settings are now stored in the YAML format, and there is a new configuration file,
also using YAML.

There is a new service used to generate the spectrograms. That was needed to separate since
that process disturbed the sound data stream when it was running in the same process.

It is possible to run WURB-2020 and WURB-2023 on the same Raspberry Pi, just stop or
start the services used for each version. The old version uses txt-files for setting and
the new one uses YAML, therefore there will be no clashes.

Note that WURB-2023 uses port 8080 for the web page where WURB-2020 uses port 8000 as default.

The same installation process as for WURB-2020 can be used, but check out WURB-2023 instead
and install the two services called "wurb_2023.service" and "wurb_2023_cache.service".

To be able to generate the spectrograms as jpeg this one must be installed.

    sudo apt install libopenjp2-7

There are two files for pip install and "requirements.txt" should be used when using Raspberry Pi.
The other one "requirements_pyaudio.txt" uses another python library on top of ALSA. I use that
one for development on macos since pyalsaaudio was not possible to install there. That may
also be useful for others who want to run the WURB detector on other hardware platforms.

The YAML-based configuration is not implemented yet, and the main directories to be used when
running the detector have fix locations. They are "../wurb_settings", "../wurb_recordings",
"../wurb_logging" and "../wurb_cache".

And a final note:

There is still a huge amount of programming/testing to be done and I'm working directly
into the main branch. Something that works one day may be broken the next day.

And since it is a spare time hobby project there are no deadlines...

## Contact

Arnold Andreasson, Sweden.

info@cloudedbats.org
