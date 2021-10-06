#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from exifread import process_file


# dir_name = '/Users/rkitay/Pictures/Sorting/Sort_From_Home_Most_should_be_duplicates/2011/07'
# dir_name = '/Users/rkitay/Pictures/Sorting/AAAA'
# dir_name = '/Users/rkitay/Pictures/Sorting/Sort_From_Home_Most_should_be_duplicates/___Much More to Sort'
dir_name = '/Users/rkitay/OneDrive/_CopyToHome/Pictures'


DEMO = True
# DEMO = False

def is_image(file_name):
    file_name = file_name.lower()
    return file_name.endswith(".jpg") or file_name.endswith(".jpeg") or file_name.endswith(".gif")


def is_video(file_name):
    file_name = file_name.lower()
    return file_name.endswith(".mp4")


# from mp4file.mp4file import Mp4File

def find_metadata_atom(file, name):
    atom = file.find('.//%s//data' % name)
    return atom.get_attribute('data')


if __name__ == '__main__':
    for file_name in os.listdir(dir_name):
        if is_image(file_name):# and not file_name.__contains__('-'):
            raw_original_date_time = None
            old_file_name = dir_name + '/' + file_name
            # print "Reading %s" % old_file_name
            f = open(old_file_name, 'rb')
            tags = process_file(f)
            # print tags
            if tags.__contains__("EXIF DateTimeOriginal"):
                raw_original_date_time = tags["EXIF DateTimeOriginal"].printable
                # print file_name
                # print raw_original_date_time
            elif tags.__contains__("Image DateTime"):
                raw_original_date_time = tags["Image DateTime"].printable
            else:
                print("No date/time in tags for {}".format(old_file_name))
                pass

            if raw_original_date_time:

                # print raw_original_date_time
                file_time_stamp = raw_original_date_time.replace(':', '').replace(' ', '_')
                # print file_time_stamp

                new_file_name = dir_name + '/IMG_' + file_time_stamp + '.jpg'
                print "Renaming %s to be %s" % (old_file_name, new_file_name)
                if not DEMO:
                    os.rename(old_file_name, new_file_name)
        # if is_video(file_name):
        #     print file_name
        #     file = Mp4File(dir_name + '/' + file_name)
        #     print find_metadata_atom(file, 'name')

