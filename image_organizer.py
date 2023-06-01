#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re
import sys


def organize_images(directory_to_scan):
    num_of_files_moved = 0

    for file_name in os.listdir(directory_to_scan):
        full_path = os.path.join(directory_to_scan, file_name)
        if os.path.isdir(full_path):
            organize_images(full_path)
        else:
            if is_candidate_file_name(file_name):
                if is_image(file_name) or is_movie(file_name):  # and not file_name.__contains__('-'):
                    print("working on file: {}".format(file_name))
                    date_part = get_date_part(file_name)
                    # print(date_part)
                    year = date_part[0:4]
                    month = date_part[4:6]
                    day = date_part[6:8]

                    time_part = get_time_part(file_name)
                    # print(time_part)

                    hour = time_part[0:2]
                    minute = time_part[2:4]
                    second = time_part[4:6]

                    extension = file_name.split('.')[1]
                    new_file_name = '{}-{}-{} {}.{}.{}.{}'.format(year, month, day, hour, minute, second, extension)
                    original_file_path = directory_to_scan + '/' + file_name
                    new_file_path = directory_to_scan + '/' + new_file_name
                    if os.path.exists(new_file_path):
                        index = 1
                        while os.path.exists(new_file_path):
                            newer_file_path = '{}/{}-{}-{} {}.{}.{}-{}.{}'.format(directory_to_scan, year, month, day, hour, minute, second, index, extension)
                            print('Detecting duplication with {} - renaming to {}'.format(new_file_path, newer_file_path))
                            new_file_path = newer_file_path
                            index += 1

                    print("Renaming {} to {}".format(original_file_path, new_file_path))
                    os.rename(original_file_path, new_file_path)
                    num_of_files_moved += 1

                    continue
                else:
                    continue


def is_candidate_file_name(file_name):
    match = re.match('((SAVE|VID|IMG|PANO)[-_]{1})?[0-9]{8}[-_][0-9]{6}', file_name)
    return match


def is_image(file_name):
    file_name = file_name.lower()
    return file_name.endswith(".jpg") or file_name.endswith(".jpeg") or file_name.endswith(".gif")


def is_movie(file_name):
    file_name = file_name.lower()
    return file_name.endswith(".avi") or file_name.endswith(".mov") or file_name.endswith(".mp4") or file_name.endswith(".mpeg")


def get_date_part(file_name):
    if file_name.startswith('IMG'):
        return file_name[4:12]
    if file_name.startswith('VID'):
        return file_name[4:12]
    if file_name.startswith('PANO'):
        return file_name[5:13]
    if file_name.startswith('SAVE'):
        return file_name[5:13]
    return file_name[0:8]


def get_time_part(file_name):
    if file_name.startswith('IMG'):
        return file_name[13:19]
    if file_name.startswith('VID'):
        return file_name[13:19]
    if file_name.startswith('PANO'):
        return file_name[14:20]
    if file_name.startswith('SAVE'):
        return file_name[14:20]
    return file_name[9:15]


if __name__ == '__main__':

    directory_to_scan = sys.argv[1]

    organize_images(directory_to_scan)