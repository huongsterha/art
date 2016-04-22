#!/usr/bin/env python

import re, urlparse


def urlEncodeNonAscii(b):
    return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)


def iriToUri(iri):
    parts = urlparse.urlparse(iri)
    return urlparse.urlunparse(
        part.encode('idna') if parti==1 else
        urlEncodeNonAscii(part.encode('utf-8'))
        for parti, part in enumerate(parts)
    )


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import urllib
    im = urllib.urlopen(iriToUri('http://uploads7.wikiart.org/images/ivan-aivazovsky/coffee-house-by-the-ortak/xf6y-mosque-in-constantinople-1846.jpg!Large.jpg')).read()
    img = plt.imread(im)
    plt.imshow(im)
    plt.show()
