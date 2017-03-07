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
import time
from random import shuffle
import datetime

only_update = True
check_pictures = True

float_pattern = re.compile('[\d,.]+')
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

def openUrl(link, seconds):
  print('Now : %s , Sleep for %d s' % (datetime.datetime.now(), seconds))
  time.sleep(seconds)
  useCurl = False
  if useCurl:
    p = subprocess.Popen(
        ['curl', link, '--socks5', '127.0.0.1:3213'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    out, err = p.communicate()
    return out
  else: # urllib
    response = urllib2.urlopen(buildRequest(link))
    return response.read()

class CheckLianjia():
  def run(self):
    show_url_debug = False
    if show_url_debug:
      httpHandler = urllib2.HTTPHandler(debuglevel=1)
      httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
      opener = urllib2.build_opener(httpHandler, httpsHandler)
      urllib2.install_opener(opener)

    # SecondHandHouse.objects.all().delete()

    # for h in SecondHandHouse.objects.all():
    #   h.delete()
    # return

    urls = [
      # 江北
      'http://cq.lianjia.com/ershoufang/jiangbeizui/ie2y2sf1l2l3ba50ea120bp90ep150/',
      'http://cq.lianjia.com/ershoufang/wulidian1/ie2y2sf1l2l3ba50ea120bp90ep150/',
      'http://cq.lianjia.com/ershoufang/guanyinqiao/ie2y2sf1l2l3ba50ea120bp90ep150/',
      'http://cq.lianjia.com/ershoufang/huangnibang/ie2y2sf1l2l3ba50ea120bp90ep150/',
      'http://cq.lianjia.com/ershoufang/beibinlu/ie2y2sf1l2l3ba50ea120bp90ep150/',
      'http://cq.lianjia.com/ershoufang/longtousi/ie2y2sf1l2l3ba50ea120bp90ep150/',
      'http://cq.lianjia.com/ershoufang/huayuanxincun/ie2y2sf1l2l3ba50ea120bp90ep150/',
      'http://cq.lianjia.com/ershoufang/songshuqiao/ie2y2sf1l2l3ba50ea120bp90ep150/',
      'http://cq.lianjia.com/ershoufang/longxi/ie2y2sf1l2l3ba50ea120bp90ep150/',
      'http://cq.lianjia.com/ershoufang/jiazhou/ie2y2sf1l2l3ba50ea120bp90ep150/',
      'http://cq.lianjia.com/ershoufang/ranjiaba/ie2y2sf1l2l3ba50ea120bp90ep150/',
      'http://cq.lianjia.com/ershoufang/beihuan/ie2y2sf1l2l3ba50ea120bp90ep150/',
      'http://cq.lianjia.com/ershoufang/caifuzhongxin1/ie2y2sf1l2l3ba50ea120bp90ep150/',

      # 渝中
      'http://cq.lianjia.com/ershoufang/chaotianmen/ie2y2sf1l2l3ba50ea120bp90ep150/',
      'http://cq.lianjia.com/ershoufang/jiefangbei1/ie2y2sf1l2l3ba50ea120bp90ep150/',
      'http://cq.lianjia.com/ershoufang/shangqingsi/ie2y2sf1l2l3ba50ea120bp90ep150/',
      'http://cq.lianjia.com/ershoufang/lianglukou/ie2y2sf1l2l3ba50ea120bp90ep150/',
      'http://cq.lianjia.com/ershoufang/hualongqiao/ie2y2sf1l2l3ba50ea120bp90ep150/',
      'http://cq.lianjia.com/ershoufang/daping/ie2y2sf1l2l3ba50ea120bp90ep150/',

      # 南岸
      'http://cq.lianjia.com/ershoufang/rongqiaobandao/ie2y2sf1l2l3ba50ea120bp90ep150/',
      'http://cq.lianjia.com/ershoufang/nanping/ie2y2sf1l2l3ba50ea120bp90ep150/',
      'http://cq.lianjia.com/ershoufang/sigongli/ie2y2sf1l2l3ba50ea120bp90ep150/',
      'http://cq.lianjia.com/ershoufang/danlonglu/ie2y2sf1l2l3ba50ea120bp90ep150/',
    ]

    errorCount = 0

    shuffle(urls)
    for link in urls:
      linkParts = link.split('/')
      linkParts[-2] = 'pg%s' + linkParts[-2]
      errorCount += self.trySearchResultLink('/'.join(linkParts), 1)

    print('There are %d errors' % (errorCount,))

  def trySearchResultLink(self, linkPattern, pageId):
    errorCount = 0
    link = linkPattern % (pageId,)
    print ('Try search result page : %s' % (link,))
    print ('Page : %d' % (pageId,))
    html = ''
    try:
      html = openUrl(link, self.sleep)
    except Exception, e:
      print 'Search result page error occurs.'
      return 1000

    parsed_html = BeautifulSoup(html, 'lxml')
    houseList = parsed_html.body.find('ul', attrs={
        'class' : 'sellListContent',
        'log-mod' : 'list'})
    if houseList is None:
      print "No houses avaliable."
      return errorCount

    for c in houseList.children:
      try:
        title = c.find('div', attrs={'class' : 'title'})
        self.getDetail(title.a['href'])
      except Exception, e:
        print 'Error occurs.'
        errorCount += 1


    pageDiv = parsed_html.body.find('div', attrs={'comp-module':'page'})
    jsonData = simplejson.loads(pageDiv['page-data'])
    print ('%d / %d' % (pageId, int(jsonData['totalPage'])))
    if pageId < int(jsonData['totalPage']):
      errorCount += self.trySearchResultLink(linkPattern, pageId + 1)

    return errorCount

  def getDetail(self, link):
    if only_update and SecondHandHouse.objects.filter(unique_link = link).exists():
        house_tmp = SecondHandHouse.objects.get(unique_link = link)
        if (not check_pictures) or house_tmp.has_pictures:
          return

    print('Try with link: %s' % (link))
    # response = urllib2.urlopen(link)
    html = openUrl(link, self.sleep)
    parsed_html = BeautifulSoup(html, 'lxml')
    smallPics = parsed_html.body.find('ul', attrs={'class': 'smallpic'})
    pictures = len(smallPics.find_all('li'))

    titleTag = parsed_html.body.find('div', attrs={'class':'title'})
    title = titleTag.h1.text
    subTitle = titleTag.div.text

    price = parsed_html.body.find('div', attrs={'class':'price'})
    totalPrice = get_float_utf8(price.span.text)
    unitPriceValue = price.find('span', attrs={'class':'unitPriceValue'}).text
    tax = price.find('div', attrs={'class':'tax'})
    firstPrice = tax.span.text
    # panelDetail = tax.find('span', attrs={'class':'panelDetail'}).text

    unitPriceValue = get_float_utf8(unitPriceValue)
    firstPrice = get_float_utf8(firstPrice)

    areaInfo = parsed_html.body.find('div', attrs={'class':'area'})
    area = areaInfo.find('div', attrs={'class':'mainInfo'}).text
    area = get_float_utf8(area)
    buildingYear = areaInfo.find('div', attrs={'class':'subInfo'}).text

    listingTime = parsed_html.body \
      .find('div', attrs={'class':'transaction'}) \
      .find_all('li')[0] \
      .contents[1]

    try:
      buildingYear = get_float_utf8(buildingYear)
    except Exception, e:
      buildingYear = 0

    roomsNumber = parsed_html.body \
        .find('div', attrs={'class':'room'}) \
        .find('div', attrs={'class':'mainInfo'}).text

    print 'totalPrice : ', totalPrice
    print 'unitPriceValue : ', unitPriceValue
    print 'pictures : ', pictures
    print 'listingTime : ', listingTime

    house = SecondHandHouse.objects.get_or_create(unique_link = link)[0]
    house.title = title
    house.sub_title = subTitle
    house.total_price = totalPrice
    house.unit_price = unitPriceValue
    house.first_price = firstPrice
    house.last_collect_time = timezone.now()
    house.area = area
    house.building_year = buildingYear
    house.has_pictures = (pictures > 1)
    house.rooms_number = roomsNumber
    house.listing_time = listingTime
    if buildingYear < 2007:
      house.hidden = True
    print house
    house.save()


