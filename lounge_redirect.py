#!/usr/bin/python

from lounge_wrangler import lounge_wrangler

my_cookie =  "exp_userhash=11615c74a29cc915c0802ae001d43b4cd96ced62;exp_uniqueid=9cc86a9bbfe20ac16a99c3ee6ce1f1f3c7ff19da;"

wrangler = lounge_wrangler(forum_id='90',
                           cookie=my_cookie,
                           cache_seconds=300,
                           cache_filename="writable/cached_url.txt")
url = wrangler.latest_lounge_url_caching()

print "Location: " + url + "\n\n";
