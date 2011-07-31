import datetime
import logging

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.api import taskqueue
from google.appengine.api import urlfetch
from google.appengine.api.urlfetch import DownloadError
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.runtime import DeadlineExceededError
from lounge_wrangler import lounge_wrangler
from lounge_wrangler_secrets import my_cookie

def seconds_from_now(time_s):
  return datetime.datetime.now() + datetime.timedelta(seconds=time_s)

class CachedURL(db.Model):
  url = db.LinkProperty()
  timestamp = db.DateTimeProperty(auto_now_add=True)
  expiration = db.DateTimeProperty()

class CacheInBackground(webapp.RequestHandler):
  def get(self):
    self.post()

  def post(self):
    wrangler = LoungeWranglerOnAppengine(forum_id='90', cookie=my_cookie,
                                         cache_seconds=600)
    try:
      logging.info('Trying to get the latest Lounge URL in the background.')
      (output_url, request_duration) = wrangler.latest_lounge_url_and_duration(
          deadline=300)
      # We will cache this for 60 * the number of seconds it took to get it.
      new_timeout = max(wrangler.cache_seconds, (request_duration + 1) * 60)
      logging.info('Got it. Now we will cache it for %d seconds.'
                   % new_timeout)
      new_expiration = seconds_from_now(new_timeout)
      new_cached_url = CachedURL(url=output_url, expiration=new_expiration)
      new_cached_url.put()
      taskqueue.Queue('default').purge()
    except (DeadlineExceededError, DownloadError):
      logging.info('Timed out. Oh well.')

class LoungeWranglerOnAppengine(lounge_wrangler):

  def retrieve_forum_page(self, deadline=10):
    return urlfetch.fetch(url=self.main_url, headers={'Cookie': self.cookie},
                          deadline=deadline).content.splitlines()


class LoungeRedirect(webapp.RequestHandler):
  def get(self):
    query = CachedURL.all()
    query.order('-expiration')
    logging.info('Checking the cache.')
    query_result = query.get()
    if (query_result is None or
        query_result.expiration < datetime.datetime.now()):
      wrangler = LoungeWranglerOnAppengine(forum_id='90', cookie=my_cookie)
      try:
        logging.info('Trying to get the latest Lounge URL.')
        (output_url,
         request_duration) = wrangler.latest_lounge_url_and_duration(
             deadline=10)
        # We will cache this for 60 * the number of seconds it took to get it.
        new_timeout = max(wrangler.cache_seconds, (request_duration + 1) * 60)
        logging.info('Got it. Now we will cache it for %d seconds.'
                     % new_timeout)
        new_expiration = seconds_from_now(new_timeout)
        new_cached_url = CachedURL(url=output_url, expiration=new_expiration)
        new_cached_url.put()
        print "Location: " + output_url + "\n\n";
      except (DeadlineExceededError, DownloadError):
        logging.info('Timed out. Will try queuing a background job.')
        taskqueue.add(url='/cache_in_background')
        self.response.out.write('<p>BTF took too long to respond. I have '
                                'better things to do than wait around all day '
                                'for that pile of MySQL.</p>')
        if query_result is not None:
          self.response.out.write(
              '<p><a href="%s">This</a> is the last good URL I know about. But '
              'it was %s when I retrieved it which is, like, an epoch ago '
              'in Internet time so I can\'t vouch for it.</p>' %
              (query_result.url,
               query_result.timestamp.strftime('%H:%M:%S UTC on %Y/%m/%d')))
        self.response.out.write('<p>Love,<br>HAL</p>')

    else:
      logging.info('We got a good result from the cache, so we will use that.')
      output_url = query_result.url
      print "Location: " + output_url + "\n\n";

application = webapp.WSGIApplication([
  ('/', LoungeRedirect),
  ('/cache_in_background', CacheInBackground),
], debug=True)



def main():
  run_wsgi_app(application)


if __name__ == '__main__':
  main()
