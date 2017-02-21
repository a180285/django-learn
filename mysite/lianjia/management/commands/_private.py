#encoding:utf-8

import urllib2
try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

from lianjia.models import SecondHandHouse
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from polls.models import Platform, Loan
import urllib2, urllib

import re

import simplejson
import subprocess


float_pattern = re.compile('[\d,.]+')
def get_float(raw_str):
  return float(float_pattern.search(str(raw_str)).group().replace(',', ''))

class CheckLianjia():
  def run(self):
    response = urllib2.urlopen('http://cq.lianjia.com/ershoufang/jiangbei/tf1de1y1sf1bp90ep170/')
    html = response.read()

    parsed_html = BeautifulSoup(html, 'lxml')
    ans = parsed_html.body.find('ul', attrs={
        'class' : 'sellListContent',
        'log-mod' : 'list'})
    for c in ans.children:
        title = c.find('div', attrs={'class' : 'title'})
        self.getDetail(title.a['href'])

  def getDetail(self, link):
    print('Try with link: %s' % (link))
    house = SecondHandHouse.objects.get_or_create(unique_link = link)[0]
    response = urllib2.urlopen(link)
    html = response.read()
    parsed_html = BeautifulSoup(html, 'lxml')
    price = parsed_html.body.find('div', attrs={'class':'price'})
    totalPrice = get_float(price.span.text)
    unitPriceValue = price.find('span', attrs={'class':'unitPriceValue'}).text.encode('utf-8')
    tax = price.find('div', attrs={'class':'tax'})
    firstPrice = tax.span.text.encode('utf-8')
    panelDetail = tax.find('span', attrs={'class':'panelDetail'}).text

    unitPriceValue = get_float(unitPriceValue)
    firstPrice = get_float(firstPrice)

    print 'totalPrice : ', totalPrice
    print 'unitPriceValue : ', unitPriceValue
    print 'firstPrice : ', firstPrice
    house.title = parsed_html.body.find('h1', attrs={'class':'main'}).text
    house.total_price = totalPrice
    house.unit_price = unitPriceValue
    house.first_price = firstPrice
    house.last_collect_time = timezone.now()
    print house
    house.save()
