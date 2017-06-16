#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

old_dir_name = '/Users/rkitay/Dropbox/Camera Uploads/'
new_root_dir = '/Users/rkitay/Pictures/Pictures_From_Home-Sorted'
num_of_files_moved = 0
for file_name in os.listdir(old_dir_name):
    if file_name.endswith(".jpg") or file_name.endswith(".mp4"):  # and not file_name.__contains__('-'):
        # if '2016-09' in file_name:
        print "working on file: %s" % file_name
        year = file_name[0:4]
        month = file_name[5:7]
        # print "year = %s" % (year)
        # print "month = %s" % (month)
        target_dir = new_root_dir + '/' + year + '/' + month
        # print "target dir = %s" % target_dir
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        num_of_files_moved += 1
        print ("Renaming {} to {}".format(old_dir_name + '/' + file_name, target_dir + '/' + file_name))
        os.rename(old_dir_name + '/' + file_name, target_dir + '/' + file_name)

        continue
    else:
        continue

print ("num_of_files_moved = {}".format(num_of_files_moved))




