#!/usr/bin/env python3

import os
import logging
import logging.handlers
import syslog

logger = logging.getLogger('MyLogger')
logger.setLevel(logging.DEBUG)

handler = logging.handlers.SysLogHandler()

logger.addHandler(handler)

logger.debug('this is debug')
logger.info('this is debug')

syslog.syslog(syslog.LOG_INFO, "Test message")


zero_file_cleanup_dirs = ["/mnt/storage/media/tv/", "/mnt/storage/media/movies/"]
media_cleanup_dirs = ["/mnt/storage/media/deleted_files/TV/", "/mnt/storage/media/deleted_files/Movies"]

def main():
    cleanup_zero_size_files()


def cleanup_zero_size_files():
    # Delete any 0 byte info files from the movie and tv folders.
    # find /mnt/storage/media/movies -size 0 -name "*.nfo" -exec rm {} \;
    # find /mnt/storage/media/tv -size 0 -name "*.nfo" -exec rm {} \;

    target_size=0

    for cleanup_dir in zero_file_cleanup_dirs:
        for dirpath, dirs, files in os.walk(cleanup_dir):
            for file in files: 
                path = os.path.join(dirpath, file)
                if os.stat(path).st_size <= target_size:
                    print(path)
                    os.remove(path)

def cleanup_deleted_files():
    for cleanup_dir in zero_file_cleanup_dirs:
        for dirpath, dirs, files in os.walk(cleanup_dir):
            for file in files:  
                path = os.path.join(dirpath, file)
                print(path)
                

if __name__ == '__main__':
    main()