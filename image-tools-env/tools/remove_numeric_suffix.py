#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import sys
import argparse

image_extensions = {"jpg", "jpeg", "gif", "heic"}
video_extensions = {"mp4", "mov", "avi"}

pattern = re.compile(
    '([1-9][0-9]{3}\-[0-9]{2}\-[0-9]{2} [0-9]{2}\.[0-9]{2}\.[0-9]{2})(\-[0-9])\.([a-z0-9]+)')


def _remove_numeric_suffix_from_files(directory, recursive, debug_mode):
    files_scanned = 0
    files_renamed = 0
    for file_name in os.listdir(directory):
        full_path = os.path.join(directory, file_name)
        if os.path.isdir(full_path):
            if recursive:
                added_scanned, added_renamed = _remove_numeric_suffix_from_files(
                    full_path, recursive, debug_mode)
                files_scanned += added_scanned
                files_renamed += added_renamed
        else:
            if _is_image(file_name) or _is_video(file_name):
                match_result = _has_numeric_suffix(file_name)
                if match_result and len(match_result.groups()) == 3:
                    files_scanned += 1
                    if _try_remove_suffix(directory, match_result, debug_mode):
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


def _has_numeric_suffix(file_name):
    return pattern.match(file_name)


def _try_remove_suffix(directory, match_result, debug_mode):
    base_name = match_result.group(1)
    suffix = match_result.group(2)
    extension = match_result.group(3)

    target_file = os.path.join(directory, f"{base_name}.{extension}")

    if not os.path.exists(target_file):
        source_file = os.path.join(
            directory, f"{base_name}{suffix}.{extension}")
        print(f"Renaming {source_file} to {target_file}")
        if not debug_mode:
            os.rename(source_file, target_file)
        return 1
    else:
        print(f"{target_file} exists - cannot use it")
        return 0


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

    files_scanned, files_renamed = _remove_numeric_suffix_from_files(
        arguments.path, arguments.recursive, arguments.debug_mode)

    print(f"Scanned a total of {files_scanned}, renamed {files_renamed}")


if __name__ == '__main__':
    main(sys.argv[1:])
