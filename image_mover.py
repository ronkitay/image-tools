#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys


def is_image(file_name):
    file_name = file_name.lower()
    return file_name.endswith(".jpg") or file_name.endswith(".jpeg") or file_name.endswith(".gif")

# old_dir_name = '/Users/ronk/OneDrive/Photos/_Exported From Google Photos/takout/2018/01'
# new_root_dir = '/Users/ronk/OneDrive/Photos/_Exported From Google Photos/takout/2018/01'
num_of_files_moved = 0


def is_movie(file_name):
    file_name = file_name.lower()
    return file_name.endswith(".avi") or file_name.endswith(".mov") or file_name.endswith(".mp4") or file_name.endswith(".mpeg")

DEMO = True
DEMO = False


def get_year(file_name):
    if file_name.startswith('IMG') or file_name.startswith('VID'):
        return file_name[4:8]
    if file_name.startswith('PANO'):
        return file_name[5:9]

    return file_name[0:4]


def get_month(file_name):
    if file_name.startswith('IMG') or file_name.startswith('VID'):
        return file_name[8:10]
    if file_name.startswith('PANO'):
        return file_name[9:11]

    return file_name[4:6]


def validate_year_and_month(year, month):
    year_int = int(year)
    if year_int > 2022:
        return False
        # raise ValueError("Year cannot be {}".format(year_int))
    if year_int < 2011:
        return False
        # raise ValueError("Year cannot be {}".format(year_int))

    month_int = int(month)
    if month_int > 12:
        return False
        # raise ValueError("Month cannot be {}".format(month_int))
    if month_int < 1:
        return False
        # raise ValueError("Month cannot be {}".format(month_int))

    return True


if __name__ == '__main__':

    old_dir_name = sys.argv[1]
    new_root_dir = old_dir_name

    for file_name in os.listdir(old_dir_name):
        if file_name.startswith('IMG') or file_name.startswith('VID') or  file_name.startswith('PANO') or file_name.startswith('201'):
            if is_image(file_name) or is_movie(file_name):  # and not file_name.__contains__('-'):
                # print("working on file: {}".format(file_name))
                year = get_year(file_name)
                month = get_month(file_name)

                if not validate_year_and_month(year, month):
                    print("Skipping {} as it does not have a valid timestamp".format(file_name))

                target_dir = new_root_dir + '/' + year + '/' + month
                # print("target dir = {}".format(target_dir))
                if not DEMO:
                    if not os.path.exists(target_dir):
                        os.makedirs(target_dir)
                num_of_files_moved += 1
                print("Renaming {} to {}".format(old_dir_name + '/' + file_name, target_dir + '/' + file_name))
                if not DEMO:
                    os.rename(old_dir_name + '/' + file_name, target_dir + '/' + file_name)

                continue
            else:
                print("SKIPPING {}".format(old_dir_name + '/' + file_name))
                continue

    print("num_of_files_moved = {}".format(num_of_files_moved))




