#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
script to collect artwork from wikiart.org
lives in utils
"""

import os
import urllib
import json
import time
import logging

DATA_ROOT = '/Volumes/data/art'

logging.basicConfig(filename='../logs/errors.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)


def fetch_artists(method='local'):
    if method == 'local':
        try:
            with open('AlphabetJson.json') as f:
                artists = json.load(f)
        except:
            print 'failed to fetch artists. Is path correct?'
    else:
        try:
            artist_url = 'http://www.wikiart.org/en/App/Artist/AlphabetJson'
            url = urllib.urlopen(artist_url)
            artists = json.load(url)
        except:
            'failed to fetch artists. Is path correct?'

    return artists


def fetch_img_urls(artist):
    # expects a json object with url attribute in form 'firstname-lastname'
    address = 'http://www.wikiart.org/en/App/Painting/' + \
              'PaintingsByArtist?artistUrl=' + \
               str(artist['url']) + '&json=2'
    json_data = json.load(urllib.urlopen(address))
    img_urls = {json_data[i]['title']: json_data[i]['image']
                for i in range(len(json_data))}

    return img_urls


if __name__ == "__main__":
    artists = fetch_artists()
    for artist in artists:
        if not os.path.exists(os.path.join(DATA_ROOT, artist['url'])):
            os.mkdir(os.path.join(DATA_ROOT, artist['url']))
        im_dict = fetch_img_urls(artist)
        for title, url in im_dict.items():
            print title, url
            try:
                file = os.path.join(DATA_ROOT, artist['url'], title + '.jpg')
                if not os.path.isfile(file):
                    with open(file, 'wb+') as f:
                        f.write(urllib.urlopen(url).read())
                        time.sleep(0.5)
            except Exception as e:
                logger.error(e)
