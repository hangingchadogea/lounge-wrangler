#!/usr/bin/python

from lounge_wrangler import lounge_wrangler
import unittest

class lounge_wrangler_test(unittest.TestCase):

  phillies_forum_id = '64'
  phillies_url = "http://www.baseballthinkfactory.org/files/forums/viewforum/64/"
  my_cookie = "exp_userhash=madeline;exp_uniqueid=albright"

  def test_constructor(self):

    wrangler = lounge_wrangler(forum_id=self.phillies_forum_id,
                               cookie=self.my_cookie)
    self.assertEqual(wrangler.main_url, self.phillies_url)
    self.assertEqual(wrangler.cookie, self.my_cookie)

    wrangler = lounge_wrangler(cookie=self.my_cookie)
    self.assertEqual(wrangler.cookie, self.my_cookie)
    self.assertEqual(wrangler.main_url,
                     "http://www.baseballthinkfactory.org/files/forums/viewforum/79/")

#  def test_retrieve_forum_page(self):
#    wrangler = lounge_wrangler(main_url=self.phillies_url,
#                               cookie=self.my_cookie)
#    try:
#      f = wrangler.retrieve_forum_page()
#      self.assert_(f.readline.find("DOCTYPE"))
#f.readline
#
#    for line in wrangler.retrieve_forum_page():
#      print line

  def test_line_has_last_forum_url(self):
    wrangler = lounge_wrangler(forum_id=self.phillies_forum_id,
                               cookie=self.my_cookie)
    self.assertEqual(wrangler.line_has_last_forum_url("href='http://www.baseballthinkfactory.org/files/forums/viewthread/2058/P1000/'>21</a>)</span>"), True)
    self.assertFalse(wrangler.line_has_last_forum_url("href='http://www.baseballthinkfactory.org/files/forums/viewthread/2114/P1000/'>21</a>)</span>"))
    self.assertFalse(wrangler.line_has_last_forum_url("href='http://www.baseballthinkfactory.org/files/forums/viewthread/2120/P1000/'>21</a>)</span>"))

  def test_latest_url_from_file(self):
    wrangler = lounge_wrangler(forum_id=self.phillies_forum_id,
                               cookie=self.my_cookie)
    self.assertEqual(
        wrangler.latest_url_from_file(open("testdata/phillies.html")),
        "http://www.baseballthinkfactory.org/files/forums/viewthread/1557/")
    self.assertEqual(
        wrangler.latest_url_from_file(open("testdata/lounge.html")),
        "http://www.baseballthinkfactory.org/files/forums/viewthread/2058/P1000/")

  def test_latest_topic_id_from_file(self):
    wrangler = lounge_wrangler(forum_id=self.phillies_forum_id,
                               cookie=self.my_cookie)
    self.assertEqual(
        wrangler.latest_topic_id_from_file(open("testdata/phillies.html")),
        '1557')
    self.assertEqual(
        wrangler.latest_topic_id_from_file(open("testdata/lounge.html")),
        '2058')



if __name__ == '__main__':
      unittest.main()
