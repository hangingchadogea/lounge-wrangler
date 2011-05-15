#!/usr/bin/python

from lounge_wrangler import lounge_wrangler

my_cookie =  "exp_userhash=madeline;exp_uniqueid=albright"
my_cookie =  "exp_userhash=11615c74a29cc915c0802ae001d43b4cd96ced62;exp_uniqueid=9cc86a9bbfe20ac16a99c3ee6ce1f1f3c7ff19da" #DELETE THIS

wrangler = lounge_wrangler(forum_id='90',
                           cookie=my_cookie,
                           cache_filename='/tmp/whatever.txt')
wrangler.post_to_forum(
    topic_id=wrangler.latest_lounge_topic_id_caching(),
    forum_id=90, text="Programmatic Lounge posting gets easier every day.")
