#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import os
import re
import sys

image_extensions = {"jpg", "jpeg", "gif"}
video_extensions = {"mp4", "mov", "avi", "mpeg"}


def _rename_files_based_on_pattern(directory, debug_mode):
    num_of_files_moved = 0

    for file_name in os.listdir(directory):
        full_path = os.path.join(directory, file_name)
        if os.path.isdir(full_path):
            _rename_files_based_on_pattern(full_path, debug_mode)
        else:
            if _is_candidate_file_name(file_name):
                # and not file_name.__contains__('-'):
                if _is_image(file_name) or _is_video(file_name):
                    print("working on file: {}".format(file_name))
                    date_part = _get_date_part(file_name)
                    # print(date_part)
                    year = date_part[0:4]
                    month = date_part[4:6]
                    day = date_part[6:8]

                    time_part = _get_time_part(file_name)
                    # print(time_part)

                    hour = time_part[0:2]
                    minute = time_part[2:4]
                    second = time_part[4:6]

                    extension = file_name.split('.')[1]
                    new_file_name = '{}-{}-{} {}.{}.{}.{}'.format(
                        year, month, day, hour, minute, second, extension)
                    original_file_path = os.path.join(directory, file_name)
                    new_file_path = os.path.join(directory, new_file_name)
                    if os.path.exists(new_file_path):
                        index = 1
                        while os.path.exists(new_file_path):
                            newer_file_path = '{}/{}-{}-{} {}.{}.{}-{}.{}'.format(
                                directory, year, month, day, hour, minute, second, index, extension)
                            print(
                                'Detecting duplication with {} - renaming to {}'.format(new_file_path, newer_file_path))
                            new_file_path = newer_file_path
                            index += 1

                    print("Renaming {} to {}".format(
                        original_file_path, new_file_path))
                    if not debug_mode:
                        os.rename(original_file_path, new_file_path)
                    num_of_files_moved += 1

                    continue
                else:
                    continue
            else:
                print("{} is not a candidate file".format(file_name))


def _is_candidate_file_name(file_name):
    match = re.match(
        '((SAVE|VID|IMG|PANO)[-_]{1})?[0-9]{8}[-_][0-9]{6}', file_name)
    return match


def _is_image(file_name):
    return _matches_extension(file_name, image_extensions)


def _is_video(file_name):
    return _matches_extension(file_name, video_extensions)


def _matches_extension(file_name, extensions):
    return _get_extension(file_name) in extensions


def _get_extension(file_name):
    return file_name.split('.')[-1].lower()


def _get_date_part(file_name):
    if file_name.startswith('IMG'):
        return file_name[4:12]
    if file_name.startswith('VID'):
        return file_name[4:12]
    if file_name.startswith('PANO'):
        return file_name[5:13]
    if file_name.startswith('SAVE'):
        return file_name[5:13]
    return file_name[0:8]


def _get_time_part(file_name):
    if file_name.startswith('IMG'):
        return file_name[13:19]
    if file_name.startswith('VID'):
        return file_name[13:19]
    if file_name.startswith('PANO'):
        return file_name[14:20]
    if file_name.startswith('SAVE'):
        return file_name[14:20]
    return file_name[9:15]


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

    _rename_files_based_on_pattern(arguments.path, arguments.debug_mode)


if __name__ == '__main__':
    main(sys.argv[1:])
