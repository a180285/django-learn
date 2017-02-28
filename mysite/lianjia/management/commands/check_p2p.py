#encoding:utf-8

from django.core.management.base import BaseCommand, CommandError

import traceback
import urllib2, urllib
try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

import re
import subprocess

float_pattern = re.compile('[\d,.]+')
def get_float(raw_str):
  return float(float_pattern.search(str(raw_str)).group().replace(',', ''))

def get_float_utf8(raw_str):
  return get_float(raw_str.encode('utf-8'))


class Command(BaseCommand):
  help = 'Running for cron-job'

  def handle(self, *args, **options):
    try:
      self.run()
    except Exception, e:
      print traceback.format_exc()
    # return

    self.stdout.write(self.style.SUCCESS('Successfully run the job '))

  def run(self):
    url = 'https://www.chenghuitong.net/borrow/1-1-0-0-0-1/'
    response = urllib2.urlopen(url)
    parsed_html = BeautifulSoup(response.read(), 'lxml')
    conList = parsed_html.find('div', attrs = {'class' : 'list-con'})
    items = conList.find_all('div', attrs = {'class' : ['list-item']})
    for item in items:
      iconNew = item.find('div', attrs = {'class' : 'icon-new'})
      duration = item.find('li', attrs = {'class' : 'borderless'})
      duration = get_float_utf8(duration.div.text)
      progress = item.find('i', attrs = {'class' : 'fr'}).text
      progress = get_float_utf8(progress)
      print '%3d month with progress : %3d%% %s' % (duration, progress, (iconNew and 'New' or ''))
      if iconNew is None and duration < 1.4 and progress < 100:
        self.send_notification(duration, progress)

  def send_notification(self, duration, progress):
    p = subprocess.Popen([
        'curl', '-s',
        '--form-string', "token=a7t9p2e7vffk1v2qah2td7ho4ekbo3",
        '--form-string', "user=uqbq8x24387odcnrwvpdxqgc9ey85u",
        '--form-string', "message=None",
        '--form-string', "title=%d month p2p %d%% progress" % (duration, progress),
        'https://api.pushover.net/1/messages.json',

        # '--socks5', '127.0.0.1:3213'
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    out, err = p.communicate()
    print out




