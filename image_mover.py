#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

def is_image(file_name):
    file_name = file_name.lower()
    return file_name.endswith(".jpg") or file_name.endswith(".jpeg") or file_name.endswith(".gif")

old_dir_name = '/Users/rkitay/Pictures/Sorting/from_onedrive__likely_dups/DCIM/100MEDIA'
new_root_dir = '/Users/rkitay/Pictures/Sorting/from_onedrive__likely_dups/DCIM/100MEDIA/split'
num_of_files_moved = 0


def is_movie(file_name):
    file_name = file_name.lower()
    return file_name.endswith(".avi") or file_name.endswith(".mov") or file_name.endswith(".mp4") or file_name.endswith(".mpeg")

DEMO = True
DEMO = False


def get_year(file_name):
    return file_name[4:8] if file_name.startswith('IMG') else file_name[0:4]


def get_month(file_name):
    return file_name[8:10] if file_name.startswith('IMG') else file_name[4:6]


def validate_year_and_month(year, month):
    year_int = int(year)
    if year_int > 2017:
        raise ValueError("Year cannot be {}".format(year_int))
    if year_int < 2011:
        raise ValueError("Year cannot be {}".format(year_int))

    month_int = int(month)
    if month_int > 12:
        raise ValueError("Month cannot be {}".format(month_int))
    if month_int < 1:
        raise ValueError("Month cannot be {}".format(month_int))


for file_name in os.listdir(old_dir_name):
    if file_name.startswith('IMG') or file_name.startswith('201'):
        if is_image(file_name) or is_movie(file_name):  # and not file_name.__contains__('-'):
            # if '2016-09' in file_name:
            print "working on file: %s" % file_name
            year = get_year(file_name)
            month = get_month(file_name)

            validate_year_and_month(year, month)
            # print "year = %s" % (year)
            # print "month = %s" % (month)
            target_dir = new_root_dir + '/' + year + '/' + month
            print "target dir = %s" % target_dir
            if not DEMO:
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)
            num_of_files_moved += 1
            print ("Renaming {} to {}".format(old_dir_name + '/' + file_name, target_dir + '/' + file_name))
            if not DEMO:
                os.rename(old_dir_name + '/' + file_name, target_dir + '/' + file_name)

            continue
        else:
            continue

print ("num_of_files_moved = {}".format(num_of_files_moved))




