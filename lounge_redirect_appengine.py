import datetime
import logging

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from lounge_wrangler import lounge_wrangler
from lounge_wrangler_secrets import my_cookie

def seconds_ago(time_s):
  return datetime.datetime.now() - datetime.timedelta(seconds=time_s)

class CachedURL(db.Model):
  url = db.LinkProperty()
  timestamp = db.DateTimeProperty(auto_now_add=True)

class LoungeRedirect(webapp.RequestHandler):
  def get(self):

    query = CachedURL.all()
    query.filter('timestamp >', seconds_ago(120))
    query.order('-timestamp')
    query_result = query.get()
    if query_result is None:
      logging.info('We got a none from the query. Doing it the hard way.')
      wrangler = lounge_wrangler(forum_id='90',
                                 cookie=my_cookie)
      output_url = wrangler.latest_lounge_url()
      new_cached_url = CachedURL(url=output_url)
      new_cached_url.put()
    else:
      logging.info('We got a good result from the cache, so we will use that.')
      output_url = query_result.url

    print "Location: " + output_url + "\n\n";

application = webapp.WSGIApplication([
  ('/', LoungeRedirect),
], debug=True)


def main():
  run_wsgi_app(application)


if __name__ == '__main__':
  main()
