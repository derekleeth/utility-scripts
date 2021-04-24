#!/usr/bin/env python3

import os
import logging
import logging.handlers
import syslog
import arrow

syslog.syslog(syslog.LOG_INFO, "Starting media cleanup script.")

zero_file_cleanup_dirs = ["/mnt/storage/media/tv/", "/mnt/storage/media/movies/"]
media_cleanup_dirs = ["/mnt/storage/media/deleted_files/TV/", "/mnt/storage/media/deleted_files/Movies"]

def main():
    cleanup_zero_size_files()
    cleanup_deleted_files()

def cleanup_zero_size_files():
    syslog.syslog(syslog.LOG_INFO, "Delete any 0 byte info files from the movie and tv folders.")

    target_size=0

    for cleanup_dir in zero_file_cleanup_dirs:
        for dirpath, dirs, files in os.walk(cleanup_dir):
            for file in files: 
                path = os.path.join(dirpath, file)
                if os.stat(path).st_size <= target_size:
                    syslog.syslog(syslog.LOG_INFO, "Deleting {0}".format(path))
                    os.remove(path)

def cleanup_deleted_files():
    delete_threshhold = arrow.now().shift(days=-7)

    for cleanup_dir in media_cleanup_dirs:
        for dirpath, dirs, files in os.walk(cleanup_dir):
            for file in files:  
                path = os.path.join(dirpath, file)
                mod_time = arrow.get(os.stat(path).st_mtime)
                print(mod_time)
                if mod_time < delete_threshhold:
                    syslog.syslog(syslog.LOG_INFO, "Deleting {0}".format(path))
                    print("Deleting {0}".format(path))
                

if __name__ == '__main__':
    main()