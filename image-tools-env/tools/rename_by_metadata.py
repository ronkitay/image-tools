#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import argparse

from exifread import process_file
import ffmpeg

from zoneinfo import ZoneInfo
from dateutil import parser

image_extensions = {"jpg", "jpeg", "gif"}
video_extensions = {"mp4", "mov", "avi"}


def _rename_files_based_on_metadata(directory, debug_mode):
    for file_name in os.listdir(directory):
        metadata_extractor = None
        if _is_image(file_name):
            metadata_extractor = _extract_metadata_from_image_file
        if _is_video(file_name):
            metadata_extractor = _extract_metadata_from_video_file

        if metadata_extractor:
            _rename_based_on_metadata(
                directory, file_name, debug_mode, metadata_extractor)


def _is_image(file_name):
    return _matches_extension(file_name, image_extensions)


def _is_video(file_name):
    return _matches_extension(file_name, video_extensions)


def _matches_extension(file_name, extensions):
    return _get_extension(file_name) in extensions


def _get_extension(file_name):
    return file_name.split('.')[-1].lower()


def _extract_metadata_from_image_file(full_file_name):
    raw_original_date_time = _extract_date_time_from_image_file(full_file_name)

    if raw_original_date_time:
        formatted_date = raw_original_date_time.replace(
            ':', '').replace(' ', '')
        year = formatted_date[0:4]
        month = formatted_date[4:6]
        day = formatted_date[6:8]
        hour = formatted_date[8:10]
        minute = formatted_date[10:12]
        second = formatted_date[12:14]
        return '{}-{}-{} {}.{}.{}'.format(year, month, day, hour, minute, second)
    else:
        return None


def _extract_date_time_from_image_file(full_file_name):
    f = open(full_file_name, 'rb')
    tags = process_file(f)
    if tags.__contains__("EXIF DateTimeOriginal"):
        return tags["EXIF DateTimeOriginal"].printable
    elif tags.__contains__("Image DateTime"):
        return tags["Image DateTime"].printable
    else:
        return None


def _extract_metadata_from_video_file(full_file_name):
    timestamp = _extract_timestamp_from_video_file(full_file_name)

    if timestamp:
        year = timestamp.year
        month = timestamp.month
        day = timestamp.day
        hour = timestamp.hour
        minute = timestamp.minute
        second = timestamp.second
        return '{}-{:02d}-{:02d} {:02d}.{:02d}.{:02d}'.format(year, month, day, hour, minute, second)
    else:
        return None


def _extract_timestamp_from_video_file(full_file_name):
    all_metadata = ffmpeg.probe(full_file_name)

    if 'format' in all_metadata:
        format = all_metadata['format']
        if 'tags' in format:
            tags = format['tags']
            if 'creation_time' in tags:
                parsered_date = parser.isoparse(tags['creation_time'])
                return parsered_date.astimezone(ZoneInfo('Asia/Jerusalem'))

    return None


def _rename_based_on_metadata(directory, file_name, debug_mode, metadata_extractor):
    original_file_name = os.path.join(directory, file_name)

    file_time_stamp = metadata_extractor(original_file_name)

    if file_time_stamp:
        extension = _get_extension(file_name)
        new_file_name = _get_new_file_name(
            directory, file_time_stamp, extension)

        if new_file_name == original_file_name:
            print('{} already has the correct name, skipping'.format(
                original_file_name))
            return

        while os.path.exists(new_file_name):
            print("{} already exists, adding a suffix".format(new_file_name))
            file_time_stamp = file_time_stamp + "-1"
            new_file_name = _get_new_file_name(
                directory, file_time_stamp, extension)

        print("Renaming {} to be {}".format(
            original_file_name, new_file_name))
        if not debug_mode:
            os.rename(original_file_name, new_file_name)
    else:
        print("No date/time in tags for {}".format(original_file_name))


def _get_new_file_name(directory, file_timestamp, extension):
    new_file_name = '{}.{}'.format(file_timestamp, extension)
    return os.path.join(directory, new_file_name)


def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', dest="debug_mode",
                        action='store_true')
    parser.add_argument(dest="path", type=str,
                        help='The path to scan for images')

    arguments = parser.parse_args(args)

    if arguments.debug_mode:
        print('Running in DEBUG mode')

    print('working on files in {}'.format(arguments.path))

    _rename_files_based_on_metadata(arguments.path, arguments.debug_mode)


if __name__ == '__main__':
    main(sys.argv[1:])
