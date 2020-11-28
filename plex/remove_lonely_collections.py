#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from plexapi.server import PlexServer
import urllib3
import configparser

urllib3.disable_warnings()

config_parser = configparser.ConfigParser()
config_parser.read("/mnt/media/scripts/scripts.config")
PLEX_CONFIG = config_parser['PLEX']

LIBRARIES = ["Movies", "TV Shows"]

PLEX_URL = config_parser.get('PLEX', 'PLEX_URL')
PLEX_TOKEN = config_parser.get('PLEX', 'PLEX_TOKEN')
## CODE BELOW ##

print(PLEX_URL)
print(PLEX_TOKEN)

sess = requests.Session()
sess.verify = False
plex = PlexServer(PLEX_URL, PLEX_TOKEN, session=sess)

for library in LIBRARIES:
    for collection in plex.library.section(library).search(libtype="collection"):
        if collection.childCount < 2:
            collection.delete()
            # Other options
            # collection.modeUpdate("hideItems")
            #collection.modeUpdate("hide")
            print("{0} ({1} items)".format(collection, collection.childCount))
