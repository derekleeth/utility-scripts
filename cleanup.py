#!/usr/bin/env python3

import os
import logging
import logging.handlers
import syslog
import arrow
import shutil

syslog.syslog(syslog.LOG_INFO, "Starting media cleanup script.")

zero_file_cleanup_dirs = ["/mnt/storage/media/tv/", "/mnt/storage/media/movies/"]
media_cleanup_dirs = ["/mnt/storage/media/deleted_files/TV/", "/mnt/storage/media/deleted_files/Movies"]

def main():
    cleanup_zero_size_files()
    cleanup_deleted_files()

def cleanup_zero_size_files():
    counter = 0
    delete_threshhold = arrow.now().shift(days=-1)

    syslog.syslog(syslog.LOG_INFO, "Delete any 0 byte files from the movie and tv folders.")

    target_size=0

    for cleanup_dir in zero_file_cleanup_dirs:
        for dirpath, dirs, files in os.walk(cleanup_dir):
            for file in files: 
                path = os.path.join(dirpath, file)
                if os.stat(path).st_size <= target_size:
                    mod_time = arrow.get(os.stat(path).st_ctime)
                    if mod_time < delete_threshhold:
                        syslog.syslog(syslog.LOG_INFO, "Deleting {0}".format(path))
                        os.remove(path)
                        counter += 1

    syslog.syslog(syslog.LOG_INFO, "Deleted {0} empty files from the movie and tv folders.")

def cleanup_deleted_files():
    delete_threshhold = arrow.now().shift(days=-30)

    total, used, free = shutil.disk_usage("/mnt/storage")
    print(total, used, free)
    free_perc = free/total

    if (free_perc) < 0.05:
        delete_threshhold = arrow.now().shift(minutes=-30)
    elif (free_perc) < 0.10:
        delete_threshhold = arrow.now().shift(days=-2)
    elif (free_perc) < 0.20:
        delete_threshhold = arrow.now().shift(days=-7)

    for cleanup_dir in media_cleanup_dirs:
        for dirpath, dirs, files in os.walk(cleanup_dir):
            for file in files:  
                path = os.path.join(dirpath, file)
                mod_time = arrow.get(os.stat(path).st_ctime)
                
                if mod_time < delete_threshhold:
                    syslog.syslog(syslog.LOG_INFO, "Deleting {0}".format(path))
                    try:
                        os.remove(path)
                    except OSError as err:
                        syslog.syslog(syslog.LOG_ERR, "OS error: {0}".format(err))
                    except:
                        syslog.syslog(syslog.LOG_ERR, "Unexpected error: {0}".format(sys.exc_info()[0]))

                

if __name__ == '__main__':
    main()
    syslog.syslog(syslog.LOG_INFO, "Completed media cleanup script.")