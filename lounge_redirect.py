#!/usr/bin/python

from lounge_wrangler import lounge_wrangler

my_cookie =  "exp_userhash=madeline;exp_uniqueid=albright;"

wrangler = lounge_wrangler(forum_id='90',
                           cookie=my_cookie,
                           cache_seconds=300,
                           cache_filename="writable/cached_url.txt")
url = wrangler.latest_lounge_url_caching()

print "Location: " + url + "\n\n";
