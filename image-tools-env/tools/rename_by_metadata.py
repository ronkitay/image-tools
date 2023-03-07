#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import argparse

from exifread import process_file
import ffmpeg

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


def _rename_based_on_metadata(directory, file_name, debug_mode, metadata_extractor):
    original_file_name = os.path.join(directory, file_name)

    file_time_stamp = metadata_extractor(original_file_name)

    if file_time_stamp:
        new_file_name = os.path.join(
            directory, '{}.{}'.format(file_time_stamp, _get_extension(file_name)))

        if new_file_name == original_file_name:
            print('{} already has the correct name, skipping'.format(
                original_file_name))
            return

        while os.path.exists(new_file_name):
            # print("{} already exists, trying {}".format(
            #     new_file_name, new_file_name+"-1"))
            # new_file_name = new_file_name+"-1"
            file_time_stamp = file_time_stamp + "-1"
            new_file_name = os.path.join(
                directory, '{}.{}'.format(file_time_stamp, _get_extension(file_name)))

        print("Renaming {} to be {}".format(
            original_file_name, new_file_name))
        if not debug_mode:
            os.rename(original_file_name, new_file_name)


def _is_image(file_name):
    return _get_extension(file_name) in image_extensions


def _get_extension(file_name):
    return file_name.split('.')[-1].lower()


def _extract_metadata_from_image_file(full_file_name):
    raw_original_date_time = None
    f = open(full_file_name, 'rb')
    tags = process_file(f)
    if tags.__contains__("EXIF DateTimeOriginal"):
        raw_original_date_time = tags["EXIF DateTimeOriginal"].printable
    elif tags.__contains__("Image DateTime"):
        raw_original_date_time = tags["Image DateTime"].printable
    else:
        print("No date/time in tags for {}".format(full_file_name))

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


def _is_video(file_name):
    return _get_extension(file_name) in video_extensions


def _extract_metadata_from_video_file(full_file_name):
    all_metadata = ffmpeg.probe(full_file_name)

    if 'format' in all_metadata:
        format = all_metadata['format']
        if 'tags' in format:
            tags = format['tags']
            if 'creation_time' in tags:
                from zoneinfo import ZoneInfo
                # print(tags['creation_time'])
                from dateutil import parser
                parsered_date = parser.isoparse(tags['creation_time'])
                # print(parsered_date)
                timestamp = parsered_date.astimezone(
                    ZoneInfo('Asia/Jerusalem'))
                # timestamp = tags['creation_time'].replace('-', '').replace(
                #     ':', '').replace(' ', '').replace('T', '').split('.')[0]
                year = timestamp.year
                month = timestamp.month
                day = timestamp.day
                hour = timestamp.hour
                minute = timestamp.minute
                second = timestamp.second
                return '{}-{:02d}-{:02d} {:02d}.{:02d}.{:02d}'.format(year, month, day, hour, minute, second)

    return None


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
