#encoding:utf-8

#  ./manage.py check_shdc

import urllib2
from bs4 import BeautifulSoup

from lianjia.models import PresalePermit
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from polls.models import Platform, Loan
import urllib

import re

import simplejson
import subprocess
import time
from random import shuffle
import datetime


from django.core.management.base import BaseCommand, CommandError

import traceback



def get_float(raw_str):
  return float(float_pattern.search(str(raw_str)).group().replace(',', ''))

def get_float_utf8(raw_str):
  return get_float(raw_str.encode('utf-8'))

def buildRequest(url):
  values = {}
  data = urllib.urlencode(values)
  headers = {
    'Cookie': 'lianjia_uuid=fa0db3b9-4593-493d-9a18-e9e112359e7a; _jzqy=1.1485741142.1485741142.1.jzqsr=baidu.-; all-lj=59dc31ee6d382c2bb143f566d268070e; _jzqx=1.1487734083.1487743754.2.jzqsr=cq%2Elianjia%2Ecom|jzqct=/ershoufang/jiangbei/tf1de1y1sf1bp90ep170/.jzqsr=localhost:8000|jzqct=/admin/lianjia/secondhandhouse/; lianjia_token=2.0050c73748299b17e1416a1e793032bb8a; select_city=500000; _jzqckmp=1; arp_scroll_position=0; CNZZDATA1255849584=586247205-1485740443-null%7C1487766936; _smt_uid=588e9c55.2f888e1f; CNZZDATA1254525948=154430216-1485739885-null%7C1487767366; CNZZDATA1255633284=1494823037-1485739424-null%7C1487768572; CNZZDATA1255604082=1618755463-1485739141-null%7C1487763968; _qzja=1.27278110.1485741141839.1487743753627.1487766797665.1487769222428.1487769229342.0.0.0.86.5; _qzjb=1.1487766797664.48.0.0.0; _qzjc=1; _qzjto=76.3.0; _jzqa=1.3971729234422082000.1485741142.1487743754.1487766798.5; _jzqc=1; _jzqb=1.48.10.1487766798.1; _ga=GA1.2.1153156391.1485741149; lianjia_ssid=f2c0e1d3-9060-4147-8fb6-1f9aa6fc7c6b',
    'Accept': '*/*',
    'User-Agent': 'curl/7.51.0',
    'Host': 'cq.lianjia.com'
  }
  req = urllib2.Request(url, data, headers)
  req.add_header(
    'User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
  )
  req.get_method = lambda: 'GET'
  return req

def openUrl(link):
  useCurl = True
  if useCurl:
    p = subprocess.Popen(
        [
        'curl', link
        # , '--socks5', '127.0.0.1:3213'
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    out, err = p.communicate()
    return out
  else: # urllib
    response = urllib2.urlopen(buildRequest(link))
    return response.read()


def buildRequests():
  url = 'http://yuyue.shdc.org.cn/ajaxSearchOrderNumInfoAction.action'
  datas = [
    'platformHosId=30&platformDeptId=938&deptdesc=&docInfo.hisDoctId=270&visitLevelCode=1&nextNumInfo=0',
    # 'platformHosId=30&platformDeptId=936&deptdesc=&docInfo.hisDoctId=070&visitLevelCode=1&nextNumInfo=0'
  ]
  headers = {
    'Accept': '*/*',
    'User-Agent': 'curl/7.51.0',
  }

  reqs = []
  for data in datas:
    req = urllib2.Request(url, data, headers)
    req.add_header(
      'User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    )
    req.get_method = lambda: 'POST'
    reqs.append(req)
  return reqs


class Command(BaseCommand):
  help = 'Running for cron-job'

  def add_arguments(self, parser):
      parser.add_argument('--sleep', type=int, default=7)

  def handle(self, *args, **options):
    sleep = options['sleep']
    # PresalePermit.objects.all().delete()
    # return
    try:
        self.run()
    except Exception as e:
        print(traceback.format_exc())
    # return

    self.stdout.write(self.style.SUCCESS('Successfully run the job '))

  def send_notify(self, title, text):
    p = subprocess.Popen([
        'curl', '-s',
        '--form-string', "token=a7t9p2e7vffk1v2qah2td7ho4ekbo3",
        '--form-string', "user=uqbq8x24387odcnrwvpdxqgc9ey85u",
        '--form-string', "message=%s" % (text.encode('utf-8'), ),
        '--form-string', "title=%s" % (title.encode('utf-8'), ),
        'https://api.pushover.net/1/messages.json',

        # '--socks5', '127.0.0.1:3213'
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    out, err = p.communicate()
    print(out)

  def run(self):

    reqs = buildRequests()

    for req in reqs:
      response = urllib2.urlopen(req)
      html = response.read()
      # print(html)
      parsed_html = BeautifulSoup(html, 'lxml')
      time_biao = parsed_html.find('div', attrs={'class':'time_biao'})
      books = time_biao.find_all('li')
      for book in books:
        book_date = book.find('div', attrs={'class': ['huisyue', 'yue']}).text.strip()
        book_week_day = book.find('div', attrs={'class': ['huiszhou', 'zhou']}).text.strip()
        book_number = book.find('div', attrs={'class': 'renshu'}).text.strip()
        title = '%s %s %s' % (book_date, book_week_day, book_number)
        if book_date != '12-16':
          continue
        print(title.encode('utf-8'))
        if book_number != u'已满':
          self.send_notify(title, title)
