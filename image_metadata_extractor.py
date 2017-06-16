#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import exifread


dir_name = '/Users/rkitay/Pictures/_Duplicates_To_Be_Deleted/zzzzzzzzzzzzzzzz/__________________Ron\'s Phone - probably duplicates (Old)'
for file_name in os.listdir(dir_name):
    if file_name.endswith(".jpg"):# and not file_name.__contains__('-'):
        old_file_name = dir_name + '/' + file_name
        print "Reading %s" % old_file_name
        f = open(old_file_name, 'rb')
        tags = exifread.process_file(f)
        # print tags
        if tags.__contains__("EXIF DateTimeOriginal"):
            raw_original_date_time = tags["EXIF DateTimeOriginal"].printable
        else:
            raw_original_date_time = tags["Image DateTime"].printable

        # print raw_original_date_time
        file_time_stamp = raw_original_date_time.replace(':', '').replace(' ', '_')
        # print file_time_stamp

        new_file_name = dir_name + '/' + file_time_stamp + '.jpg'
        print "Renaming %s to be %s" % (old_file_name, new_file_name)
        # os.rename(old_file_name, new_file_name)
