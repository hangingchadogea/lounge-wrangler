#!/usr/bin/python

from lounge_wrangler import lounge_wrangler

my_cookie =  "exp_userhash=madeline;exp_uniqueid=albright"

wrangler = lounge_wrangler(forum_id='90',
                           cookie=my_cookie,
                           cache_filename='/tmp/whatever.txt')
wrangler.post_to_forum(
    topic_id=wrangler.latest_lounge_topic_id_caching(),
    forum_id=90, text="Programmatic Lounge posting gets easier every day.")
