#!/usr/bin/python

from lounge_wrangler import lounge_wrangler
from lounge_wrangler_secrets import username, password

wrangler = lounge_wrangler(forum_id='90',
                           username=username, password=password,
                           cache_seconds=300,
                           cache_filename="writable/cached_url.txt")
url = wrangler.latest_lounge_url_caching()

print "Location: " + url + "\n\n";
