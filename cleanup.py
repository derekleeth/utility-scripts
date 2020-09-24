#!/usr/bin/env python3

import os
import logging
import logging.handlers

zero_file_cleanup_dirs = ["/mnt/storage/media/tv/", "/mnt/storage/media/movies/"]

def main():
    cleanup_zero_size_files()


def cleanup_zero_size_files():
    # Delete any 0 byte info files from the movie and tv folders.
    # find /mnt/storage/media/movies -size 0 -name "*.nfo" -exec rm {} \;
    # find /mnt/storage/media/tv -size 0 -name "*.nfo" -exec rm {} \;

    zero_size_cleanup_dirs = ["/mnt/storage/media/tv/", "/mnt/storage/media/movies/"]

    target_size=0
    for cleanup_dir in zero_file_cleanup_dirs:
        for dirpath, dirs, files in os.walk(cleanup_dir):
            for file in files: 
                path = os.path.join(dirpath, file)
                if os.stat(path).st_size <= target_size:
                    print(path)


if __name__ == '__main__':
    main()