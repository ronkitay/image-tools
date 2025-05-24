#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import argparse

from exifread import process_file
import ffmpeg

from zoneinfo import ZoneInfo
from dateutil import parser

import os
from PIL import Image
from pillow_heif import register_heif_opener

image_extensions = {"jpg", "jpeg", "gif", "png", "heic"}
video_extensions = {"mp4", "mov", "avi", "3gp"}


def _rename_files_based_on_metadata(directory, recursive, debug_mode):
    files_scanned = 0
    files_renamed = 0
    for file_name in os.listdir(directory):
        full_path = os.path.join(directory, file_name)
        if os.path.isdir(full_path):
            if recursive:
                added_scanned, added_renamed = _rename_files_based_on_metadata(
                    full_path, recursive, debug_mode)
                files_scanned += added_scanned
                files_renamed += added_renamed
        else:
            metadata_extractor = None
            if _is_image(file_name):
                metadata_extractor = _extract_metadata_from_image_file
            if _is_video(file_name):
                metadata_extractor = _extract_metadata_from_video_file

            if metadata_extractor:
                files_scanned += 1
                if _rename_based_on_metadata(
                        directory, file_name, debug_mode, metadata_extractor):
                    files_renamed += 1

    return files_scanned, files_renamed


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

    if full_file_name.lower().endswith('.heic'):
        return _extract_heic_metadata(full_file_name)
    else:
        f = open(full_file_name, 'rb')
        try:
            tags = process_file(f)

            if tags.__contains__("EXIF DateTimeOriginal"):
                return tags["EXIF DateTimeOriginal"].printable
            elif tags.__contains__("Image DateTime"):
                return tags["Image DateTime"].printable
            else:
                return None
        except Exception as e:
            print("Error processing {}: {}".format(full_file_name, e))
            return None

def _extract_heic_metadata(heic_file_path):
    try:
        # Open the HEIC file with Pillow
        img = Image.open(heic_file_path)

        # Try to get the EXIF data
        exif_data = img.getexif()

        # EXIF tag for DateTime and DateTimeOriginal
        # 306 = DateTime
        # 36867 = DateTimeOriginal (when the photo was taken)
        # 36868 = DateTimeDigitized

        # First try DateTimeOriginal (most accurate for photos)
        creation_date = exif_data.get(36867)

        # If not found, try DateTime
        if not creation_date:
            creation_date = exif_data.get(306)

        # If still not found, try DateTimeDigitized
        if not creation_date:
            creation_date = exif_data.get(36868)

        return creation_date
    except Exception as e:
        print("Error processing {}: {}".format(heic_file_path, e))
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
            return False

        while os.path.exists(new_file_name):
            print("{} already exists, adding a suffix".format(new_file_name))
            file_time_stamp = file_time_stamp + "-1"
            new_file_name = _get_new_file_name(
                directory, file_time_stamp, extension)
            if new_file_name == original_file_name:
                print('{} already has the correct name, skipping'.format(
                    original_file_name))
                return False

        print("Renaming {} to be {}".format(
            original_file_name, new_file_name))
        if not debug_mode:
            os.rename(original_file_name, new_file_name)
        return True
    else:
        print("No date/time in tags for {}".format(original_file_name))
        return False


def _get_new_file_name(directory, file_timestamp, extension):
    new_file_name = '{}.{}'.format(file_timestamp, extension)
    return os.path.join(directory, new_file_name)


def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', dest="debug_mode",
                        action='store_true')
    parser.add_argument('-r', '--recursive', dest="recursive",
                        action='store_true')
    parser.add_argument(dest="path", type=str,
                        help='The path to scan for images')

    arguments = parser.parse_args(args)

    if arguments.debug_mode:
        print('Running in DEBUG mode')

    print('working on files in {}'.format(arguments.path))

    register_heif_opener()

    files_scanned, files_renamed = _rename_files_based_on_metadata(
        arguments.path, arguments.recursive, arguments.debug_mode)

    print(f"Scanned a total of {files_scanned}, renamed {files_renamed}")


if __name__ == '__main__':
    main(sys.argv[1:])
