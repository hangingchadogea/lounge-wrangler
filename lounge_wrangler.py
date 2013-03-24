import datetime
import logging
import urllib
import urllib2
import re
import time
import os
import sys

class lounge_wrangler:
  "Documentation is for sissies."
  def __init__(self,
               cookie=None,
               username=None,
               password=None,
               forum_id='79',
               cache_filename="cached_url.txt",
               cache_seconds=300,
               error_url=('http://www.downforeveryoneorjustme.com/'
                          'http://www.baseballthinkfactory.org/forums/')):
    self.main_url = ('http://www.baseballthinkfactory.org/forums/'
                     'viewforum/' + forum_id + '/')
    if cookie:
      self.cookie = cookie
    else:
      if not username or not password:
        sys.exit("Neither username nor password specified.")
      self.cookie = lounge_wrangler.get_cookie_via_post(username, password)
    self.cache_filename = cache_filename
    self.cache_seconds = cache_seconds
    self.error_url = error_url
#    bad_threads = "125|2(1(14|20|26|37|38)|482|505|6(05|50|88)|7(06|16|36|43|46))"
    bad_threads = "2961|3067|3078|3085|3089|3094|3102"
    self.last_url = re.compile(
        "(http://www.baseballthinkfactory.org/forums/viewthread/(?!("
        + bad_threads + "))\d+/P\d+/)'>\d+</a>\)</span>")
    self.thread_url = re.compile(
        "(http://www.baseballthinkfactory.org/forums/viewthread/(?!("
        + bad_threads + "))\d+/)")

  def retrieve_forum_page(self, deadline=5):
    # the deadline doesn't actually do anything here
    req = urllib2.Request(url=self.main_url)
    req.add_header('Cookie', self.cookie)
    req.add_header('User-Agent', 'Python-urllib/2.6')
    logging.info("Using cookie " + self.cookie)
    return urllib2.urlopen(req)

  def line_has_thread_url(self, line):
    return bool(self.thread_url.search(line))

  def line_has_last_forum_url(self, line):
    return bool(self.last_url.search(line))

  def topic_id_from_url(self, url):
    return re.search('viewthread/(\d+)/', url).groups()[0]

  def latest_topic_id_from_file(self, html_file):
    return self.topic_id_from_url(self.latest_url_from_file(html_file))

  def latest_url_from_file(self, html_file):
    current_thread = None
    line_count = 0
    for line in html_file:
      logging.info(line)
      line_count += 1
      m = self.last_url.search(line)
      if m:
        return m.groups(1)[0]
      m = self.thread_url.search(line)
      if m:
        if current_thread == None:
          current_thread = m.groups(1)[0]
        else:
          if current_thread != m.groups(1)[0]:
            # We had this thread URL, we never found a last page URL, and now
            # the site is showing us a new thread.  That means current_thread
            # points to the only page of the latest thread.
            logging.info('Returning after line ' + str(line_count))
            return current_thread
    #We've reached the end of the file.  current_thread is probably the one
    # we want to return.  If it's not set, it's None, which is also what we
    # want.
    logging.info('Returning after line ' + str(line_count))
    return current_thread

  def read_string_from_file(self, filename):
    f = open(filename)
    return f.read()

  def write_string_to_file(self, string, filename):
    f = open(filename, 'w')
    f.write(string)
    f.close()

  def file_age_seconds(self, filename):
    return time.time() - os.stat(filename).st_mtime

  def cache_expired(self, filename):
    try:
      file_age = self.file_age_seconds(filename)
      return file_age > self.cache_seconds
    except OSError:
      return 1

  def latest_lounge_url(self, deadline=5):
    url = self.latest_url_from_file(self.retrieve_forum_page(deadline=deadline))
    if url is None:
      logging.info("Using the error URL")
      url=self.error_url
    return url

  def latest_lounge_url_and_duration(self, deadline=5):
    request_start_time = datetime.datetime.now()
    url = self.latest_url_from_file(self.retrieve_forum_page(deadline=deadline))
    request_duration = (datetime.datetime.now() - request_start_time).seconds
    if url is None:
      logging.info('Using the error URL.')
      url=self.error_url
    return (url, request_duration)

  def latest_lounge_topic_id_caching(self):
    return self.topic_id_from_url(self.latest_lounge_url_caching())

  def latest_lounge_url_caching(self):
    if self.cache_expired(self.cache_filename):
      url = self.latest_lounge_url()
      self.write_string_to_file(url, self.cache_filename)
      return url
    else:
      return self.read_string_from_file(self.cache_filename)

  def post_to_forum(self, topic_id, forum_id, text):
    req = urllib2.Request(
        url="http://www.baseballthinkfactory.org/forums/newreply/%s/" %
        topic_id)
    req.add_header('Cookie', self.cookie)
    post_data = {'ACT': '19',
                 'FROM': 'forum',
                 'mbase':
                 'http://www.baseballthinkfactory.org/forums/member/',
                 'board_id': '1',
                 'RET':
                 'http://www.baseballthinkfactory.org/forums/viewthread/' + topic_id + '/',
                 'topic_id': topic_id,
                 'forum_id': forum_id,
                 'site_id': '1',
                 'smileys': 'y',
                 'body': text,
                 'submit': 'Submit Post'}
    encoded_data = urllib.urlencode(post_data)
    return urllib2.urlopen(req, encoded_data)

  @staticmethod
  def get_cookie_via_post(username, password):
    req = urllib2.Request(url="http://www.baseballthinkfactory.org/")
    post_data = {'ACT': '9',
                 'FROM': 'forum',
                 'mbase': 'http://www.baseballthinkfactory.org/forums/member/',
                 'RET': 'http://www.baseballthinkfactory.org/',
                 'site_id': '1',
                 'board_id': '1',
                 'username': username,
                 'password': password,
                 'submit': 'Login',
                 'auto_login': '1',
                 'anon': '1'}
    encoded_data = urllib.urlencode(post_data)
    login_response = urllib2.urlopen(req, encoded_data)
    final_cookie = ''
    for header in login_response.info().getheaders('Set-Cookie'):
      cookie = header.split()[0]
#      if 'exp_uniqueid=' in cookie or 'exp_userhash=' in cookie:
      final_cookie = final_cookie + cookie
    return final_cookie
