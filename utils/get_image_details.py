#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
script to collect information on artworks
requires scrape script
lives in utils
"""

import urllib
import os
import json
import time
from datetime import datetime
import logging
import sys

import scrape

reload(sys)
sys.setdefaultencoding('utf8')

DATA_ROOT = '/Volumes/data/art'

logging.basicConfig(filename='../logs/style_error.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)


def fetch_img_details(artist, img):

    # artist is a json object with url attribute in form 'firstname-lastname'
    # img is a string corresponding to artwork title
    paintings_address = 'http://www.wikiart.org/en/App/Painting/' + \
                        'PaintingsByArtist?artistUrl=' + \
                         str(artist['url']) + '&json=2'
    json_data = json.load(urllib.urlopen(paintings_address))
    start = datetime.now()

    for result in json_data:
        if result['title'] == img:
            content_id = result['contentId']
            details_address = 'http://www.wikiart.org/' + \
                              'en/App/Painting/ImageJson/' + \
                               str(content_id)
            # make sure you're not exceeding rate limits on API
            if (datetime.now() - start).seconds < 0.5:
                time.sleep(0.5 - (datetime.now() - start).seconds)
            painting_details = json.load(urllib.urlopen(details_address))
            return painting_details
    return 'no info'


def write_label_file(fout, attr):
    # fout is path to label file
    # attr is attribute of interest
    with open(fout, 'wb+') as f:
        artists = scrape.fetch_artists()
        for artist in artists:
            print artist['url']
            img_urls = scrape.fetch_img_urls(artist)

            for title, _ in img_urls.items():
                path = os.path.join(DATA_ROOT, artist['url'], title + '.jpg')
                path = path.encode('utf-8')
                label = fetch_img_details(artist, title)[attr]
                if os.path.isfile(path):
                    if label is not None:
                        try:
                            print '{}\t{}'.format(path, label)
                            f.write('"' + path + '"' +
                                    '\t' + '"' + label + '"' + '\n')
                        except:
                            os.system('say "W T F"')
                            print 'wtf man'
                    else:
                        try:
                            print '{}\t{}'.format(path, 'None')
                            f.write('"' + path + '"' + '\t' + 'None' + '\n')
                        except:
                            os.system('say "W T F"')
                            print 'wtf man'
                else:
                    logger.error('path dne')
        os.system('say "Done"')


if __name__ == '__main__':
    # testing
    # print fetch_img_details({'url': 'pablo-picasso'}, 'Guernica')['style']
    write_label_file('../labels/style_labels.txt', 'style')

