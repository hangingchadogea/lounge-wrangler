#!/usr/bin/python

from getpass import getpass
import urllib
import urllib2
from lounge_wrangler import lounge_wrangler

username = raw_input('Enter BTF username: ')
password = getpass('Enter BTF password for ' + username + ': ')
final_cookie =  lounge_wrangler.get_cookie_via_post(username, password)

print final_cookie
