#encoding:utf-8

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.utils import timezone

from polls.models import Platform, Loan
import urllib2, urllib

import re

import simplejson

def split_by_tag(raw_data_str):
  return [raw_data.split('<')[0].strip() for raw_data in raw_data_str.split('>')]

def debug_output(datas):
  for index in xrange(0, len(datas)):
    print("%s -> %s" % (index, datas[index][:100]))

def get_link(raw_txt, sep = '"', index = 1):
  return raw_txt.split('href=')[index].split(sep)[1]

float_pattern = re.compile('[\d,.]+')
def get_float(raw_str):
  return float(float_pattern.search(str(raw_str)).group().replace(',', ''))

def get_json(json_datas, key):
  key = key + '"'
  for data in json_datas:
    if data.startswith(key):
      return data.split(':', 1)[1].strip('"').strip()

def get_available_money(total_money, prograss):
  return get_float(total_money) * (100 - get_float(prograss)) / 100

def encode_json(json):
  for key in json:
    if json[key]:
      json[key] = json[key].encode('utf-8')

class BasePlatform():
  platform_name = None
  platform_link = None
  platform = None

  name = None
  total_money = None
  duration = None
  year_rate = None
  prograss = None
  available_money = None
  link = None
  for_new_member = False

  is_json_format = False

  def filter_func(self, raw_biao):
    return True

  def run(self):
    print("%s started ..." % self.platform_name)
    self.platform = Platform.objects.get_or_create(name = self.platform_name)[0]
    self.platform.link = self.platform_link
    self.platform.save()
    self.platform.loan_set.all().delete()

    index = 1
    while self.get(index):
      index += 1

    print("%s Done ..." % self.platform_name)
    self.platform.last_update_time = timezone.now()
    self.platform.save()

  def get(self, index):
    has_item = False
    req = self.get_request(index)
    print("Page : %s" % index)
    print("Url : %s" % req.get_full_url())
    print("Request data : %s" % req.get_data())

    data = urllib2.urlopen(req).read()
    biaos = self.get_biaos(data)
    biaos = filter(self.filter_func, biaos)
    for raw_biao in biaos:
      if not self.is_json_format:
        raw_datas = split_by_tag(raw_biao)
      else:
        raw_datas = raw_biao
      self.fill_fields(raw_biao, raw_datas)
      self.output_fields()

      if self.available_money > 100:
        if Loan.objects.filter(link = self.link):
          continue

        has_item = True
        self.platform.loan_set.create(name = self.name,
          duration = self.duration,
          year_rate = self.year_rate,
          link = self.link,
          total_money = self.total_money,
          available_money = self.available_money,
          for_new_member = self.for_new_member)

    return has_item

  def output_fields(self):
    print('----------------------------')
    print("name : %s" % self.name)
    print("total_money : %s" % self.total_money)
    print("duration : %s" % self.duration)
    print("year_rate : %s" % self.year_rate)
    print("prograss : %s" % self.prograss)
    print("available_money : %s" % self.available_money)
    print("for_new_member : %s" % self.for_new_member)
    print("link : %s" % self.link)

  def convert_data_by_detault(self):
    self.total_money = get_float(self.total_money)
    self.year_rate = get_float(self.year_rate)
    self.duration = int(get_float(self.duration)) * 30
    if self.available_money:
      self.available_money = get_float(self.available_money)
    else:
      self.prograss = get_float(self.prograss)
      self.available_money = get_available_money(self.total_money, self.prograss)

class HuRongBao(BasePlatform):
  platform_name = "互融宝"
  platform_link = 'http://www.hurbao.com/'

  def get_request(self, index):
    url = 'https://www.hurbao.com/invests?p=%s' % index
    values = {}
    data = urllib.urlencode(values)
    headers = {}
    return urllib2.Request(url, data, headers)

  def get_biaos(self, raw_data):
    return raw_data.split('class="content_list_product"')[1:]
 
  def fill_fields(self, raw_biao, raw_datas):
    # debug_output(raw_datas)
    # self.for_new_member = raw_biao.find('xinuser_ioc.png') != -1
    self.link = 'https://www.hurbao.com' + get_link(raw_biao)

    self.name = raw_datas[6]
    delta = 0
    if raw_datas[18]:
      delta = -3
    self.available_money = raw_datas[65 + delta]
    self.total_money = raw_datas[21 + delta]
    self.year_rate = raw_datas[32 + delta]
    self.duration = raw_datas[44 + delta]
    # self.prograss = raw_datas[52]

    self.output_fields()
    year_rate = 0
    for rate in self.year_rate.split('+'):
      year_rate += get_float(rate)
    self.year_rate = year_rate

    self.convert_data_by_detault()

class AnJieCaiFu(BasePlatform):
  platform_name = "安捷财富"
  platform_link = 'http://www.haoinvest.com/'

  def get_request(self, index):
    url = 'http://www.haoinvest.com/invest/hot/p/%s.html' % index
    values = {}
    data = urllib.urlencode(values)
    return urllib2.Request(url, data)

  def get_biaos(self, raw_data):
    return raw_data.split('class="tz_project_j_l"')[1:]
 
  def fill_fields(self, raw_biao, raw_datas):
    # debug_output(raw_datas)
    self.for_new_member = raw_biao.find('xinuser_ioc.png') != -1
    self.link = 'http://www.haoinvest.com' + get_link(raw_biao)

    delta = 0
    if self.for_new_member:
      delta = 3
    self.name = raw_datas[5 + delta]
    self.available_money = raw_datas[16 + delta]
    self.total_money = raw_datas[17 + delta]
    self.year_rate = raw_datas[23 + delta]
    self.duration = raw_datas[31 + delta]
    # self.prograss = raw_datas[52]

    self.output_fields()
    self.convert_data_by_detault()

class NoNoBank(BasePlatform):
  platform_name = "诺诺镑客"
  platform_link = 'http://www.nonobank.com/'
  is_json_format = True

  def get_request(self, index):
    index -= 1
    if index % 2 == 1:
      url = 'https://www.nonobank.com/Licai/GetLicaiList/8/'
    else:
      url = 'https://www.nonobank.com/Licai/IntimatePlanList/8/'
    url = url + str(index / 2)
    values = {}
    data = urllib.urlencode(values)
    return urllib2.Request(url, data)

  def get_biaos(self, raw_data):
    json = simplejson.loads(raw_data)

    return json['members']
 
  def fill_fields(self, json, raw_datas):
    # debug_output(raw_datas)

    encode_json(json)

    self.link = 'https://www.nonobank.com/Licai/FinancePlan/' + json['fp_id']
    self.name = json['fp_title']

    self.total_money = json['fp_price']
    self.year_rate = json['fp_rate_show']
    self.duration = json['fp_expect']
    self.prograss = json['fp_percent']
    self.available_money = None
    self.for_new_member = self.name.find('新客体验') != -1

    self.output_fields()

    self.convert_data_by_detault()

class ChengHuiTong(BasePlatform):
  platform_name = "诚汇通"
  platform_link = 'http://www.chenghuitong.net/'

  def get_request(self, index):
    url = 'https://www.chenghuitong.net/borrow/default-index.html?page=' + str(index)
    values = {}
    data = urllib.urlencode(values)
    return urllib2.Request(url, data)

  def get_biaos(self, raw_data):
    return raw_data.split('"invest-list-content-box"')[1:]
 
  def fill_fields(self, raw_biao, raw_datas):
    # debug_output(raw_datas)
    self.link = get_link(raw_biao)

    additional_rate = 0
    delta = 0
    for index in xrange(0,20):
      data = raw_datas[index]
      if data.endswith('%'):
        additional_rate = data
      elif raw_datas[index]:
        self.name = data
        delta = index
        break
    

    self.total_money = raw_datas[delta + 4]
    self.year_rate = raw_datas[delta + 6]
    self.duration = raw_datas[delta + 8]
    self.prograss = raw_datas[delta + 12]
    if not self.prograss:
      self.prograss = raw_datas[delta + 14]
    self.available_money = None

    self.output_fields()

    self.convert_data_by_detault()

class ShiTouJinRong(BasePlatform):
  platform_name = "石投金融"
  platform_link = 'http://www.shitou.com/'

  def get_request(self, index):
    url = 'http://www.shitou.com/website/loadLoanProList'
    values = {'page' : index,
        'timeLimit' : '-1',
        'repType' : '-1',
        'status' : '-1',
        'rows' : '5'}
    data = urllib.urlencode(values)
    return urllib2.Request(url, data)

  def get_biaos(self, raw_data):
    return raw_data.split('"loanListShow-li"')[1:]
 
  def fill_fields(self, raw_biao, raw_datas):
    # debug_output(raw_datas)
    self.link = 'http://www.shitou.com' + get_link(raw_biao, sep = "'")
    self.name = raw_datas[14]
    self.total_money = raw_datas[34]
    self.year_rate = raw_datas[26]
    self.duration = raw_datas[30]
    self.prograss = raw_datas[52]

    self.output_fields()

    self.total_money = get_float(self.total_money)
    self.duration = int(get_float(self.duration)) * 30
    self.year_rate = get_float(self.year_rate)
    self.prograss = get_float(self.prograss)
    self.for_new_member = self.name.find('新手') != -1
    self.available_money = get_available_money(self.total_money, self.prograss)

class EDai365(BasePlatform):
  platform_name = "365易贷"
  platform_link = 'http://www.365edai.cn/'

  def filter_func(self, raw_biao):
    return raw_biao.find('密码') == -1

  def get_request(self, index):
    url = 'http://www.365edai.cn/Lend/Cloanlist.aspx?k=e&page=' + str(index)
    return urllib2.Request(url)

  def get_biaos(self, raw_data):
    return raw_data.split("biaoname")[1:]
 
  def fill_fields(self, raw_biao, raw_datas):
    self.link = 'http://www.365edai.cn' + get_link(raw_biao)
    self.name = raw_datas[1]
    self.total_money = raw_datas[15]
    self.year_rate = raw_datas[19]
    self.duration = raw_datas[23]
    self.duration_type = raw_datas[24]
    self.additional_rate = raw_datas[27]
    delta = 0
    print("self.additional_rate : %s" % self.additional_rate)
    if not self.additional_rate:
      self.additional_rate = 0
      delta = -2

    return_method = raw_datas[30 + delta]
    self.available_money = raw_datas[36 + delta]
    self.prograss = raw_datas[43 + delta]

    self.output_fields()

    self.available_money = get_float(self.available_money)
    self.total_money = get_float(self.total_money)
    self.duration = int(self.duration)
    if self.duration_type == '月':
      self.duration = self.duration * 30

    self.year_rate = get_float(self.year_rate) + get_float(self.additional_rate) * 360 / self.duration

class YiQiHao(BasePlatform):
  platform_name = "一起好"
  platform_link = 'http://www.yiqihao.com/'

  def get_request(self, index):
    values = {'p' : index,
        'sort' : '',
        'format' : 'json'}
    data = urllib.urlencode(values)
    url = 'https://www.yiqihao.com/loan/list/all'
    return urllib2.Request(url, data)

  def get_biaos(self, raw_data):
    return raw_data.split('"lid"')[1:]
 
  def fill_fields(self, raw_biao, raw_datas):
    json_datas = raw_biao.split(',"')
    # debug_output(json_datas)

    self.link = 'https://www.yiqihao.com/#!detail&id=' + json_datas[0].split('"')[1]
    self.name = get_json(json_datas, 'title')
    self.total_money = get_json(json_datas, 'amount')
    self.year_rate = get_json(json_datas, 'apr')
    self.prograss = get_json(json_datas, 'progress')
    self.duration = get_json(json_datas, 'deadline')
    self.for_new_member = get_json(json_datas, 'is_newbie')

    self.available_money = get_available_money(self.total_money, self.prograss)
    self.for_new_member = self.for_new_member == '100'
    self.duration = get_float(self.duration) * 30

class GuoChengJinRong():
  def __init__(self):
    self.platform_name = "国诚金融"
    self.platform = Platform.objects.get_or_create(name = self.platform_name)[0]
    platform_link = 'http://www.gcjr.com/'
    self.platform.link = platform_link
    self.platform.save()
  
  def run(self):
    self.platform.loan_set.all().delete()
    index = 1
    while self._get(index):
      index += 1
    print("GuoChengJinRong Done ...")

    self.platform.last_update_time = timezone.now()
    self.platform.save()

  def _get(self, index):
    has_item = False
    print("Page : %d" % index)
    url = 'http://www.gcjr.com/dingqibao/queryFixBorrowList.html'
    values = {'pageNum' : index,
        'pageSize' : 10}
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    data = urllib2.urlopen(req).read()

    for raw_loan in data.split('<tr>')[1:]:
      raw_datas = raw_loan.split('</td>')

      for_new_member = raw_datas[0].find('<img src') != -1
      name = split_by_tag(raw_datas[0])[2]
      total_money = split_by_tag(raw_datas[1])[1]
      year_rate = split_by_tag(raw_datas[2])[1]
      duration = split_by_tag(raw_datas[3])[1]
      person_num = split_by_tag(raw_datas[4])[1]
      prograss = split_by_tag(raw_datas[5])[-3]
      is_active = raw_datas[6].find('立即加入') != -1

      link = raw_datas[0].split('(')[1].split(')')[0]
      link = 'http://www.gcjr.com/dingqibao/%s.html' % link

      total_money = float(total_money[:-3].replace(',', ''))
      year_rate = float(year_rate[:-1])
      duration = int(duration[:-6]) * 30
      prograss = float(prograss[:-1])
      available_money = total_money * (100 - prograss) / 100
      print '----------------------------'
      print 'for_new_member : %s' % for_new_member
      print 'name : %s' % name
      print 'total_money : %s' % total_money
      print 'year_rate : %s' % year_rate
      print 'duration : %s' % duration
      print 'person_num : %s' % person_num
      print 'prograss : %s' % prograss
      print 'available_money : %s' % available_money
      print 'link : %s' % link
      print 'is_active : %s' % is_active

      if is_active and available_money > 100:
        has_item = True
        self.platform.loan_set.create(name = name,
          duration = duration,
          year_rate = year_rate,
          link = link,
          total_money = total_money,
          available_money = available_money,
          for_new_member = for_new_member)

    return has_item

class XueShanDai(object):
  def __init__(self):
    self.platform_name = "雪山贷"
    self.platform = Platform.objects.get_or_create(name = self.platform_name)[0]
    platform_link = 'http://www.xueshandai.com/'
    self.platform.link = platform_link
    self.platform.save()

  def run(self):
    self.platform.loan_set.all().delete()
    index = 1
    while self._get(index):
      index += 1
    print("XueShanDai Done ...")

    self.platform.last_update_time = timezone.now()
    self.platform.save()

  def _get(self, index):
    has_item = False
    print("Page : %d" % index)
    url = 'http://www.xueshandai.com/invest/list?max=5&offset=%s&multiple=true&offest=0' % (index * 5 - 5)
    print("url -> " + url)

    req = urllib2.Request(url)
    data = urllib2.urlopen(req).read()
    biaos = data.split("listing list_inner")[1:]
    for raw_biao in biaos:
      datas = split_by_tag(raw_biao)

      # debug_output(datas)

      name = datas[8]
      total_money = datas[47]
      year_rate = datas[55]
      duration = datas[63]
      duration_type = datas[64]
      prograss = datas[74]
      link = 'http://www.xueshandai.com' + get_link(raw_biao)

      print '----------------------------'
      print('name : %s' % name)
      print('total_money : %s' % total_money)
      print('year_rate : %s' % year_rate)
      print('duration : %s' % duration)
      print('duration_type : %s' % duration_type)
      print('prograss : %s' % prograss)
      print('link : %s' % link)

      total_money = float(total_money.replace(',', ''))
      prograss = float(prograss[:-1])
      year_rate = float(year_rate)
      available_money = total_money * (100 - prograss) / 100
      duration = int(duration)
      if duration_type == '个月':
        duration = duration * 30

      if available_money > 100:
        has_item = True
        self.platform.loan_set.create(name = name,
          duration = duration,
          year_rate = year_rate,
          link = link,
          total_money = total_money,
          available_money = available_money)

    return has_item

class HeShiDai():
  def __init__(self):
    self.platform_name = "合时代"
    self.platform = Platform.objects.get_or_create(name = self.platform_name)[0]
    platform_link = 'http://www.heshidai.com/'
    self.platform.link = platform_link
    self.platform.save()

  def run(self):
    self.platform.loan_set.all().delete()
    index = 1
    while self._get(index):
      index += 1
    print("HeShiDai Done ...")

    self.platform.last_update_time = timezone.now()
    self.platform.save()

  def _get(self, index):
    has_item = False
    print("Page : %d" % index)
    url = 'https://www.heshidai.com/lctz/financeList.act'
    values = {'pageBean.pageNum' : index,
        'paramMap.sort' : 1,
        'paramMap.desc' : 'desc',
        'paramMap.isNewBorrow' : 1}
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    data = urllib2.urlopen(req).read()

    for raw_biao in data.split('</ul>')[1:-1]:
      datas = split_by_tag(raw_biao)
      # debug_output(datas)

      name = datas[6]
      delta = 0
      if datas[13]:
        delta = 2
      total_money = datas[11 + delta]
      duration = datas[14 + delta]
      year_rate = datas[18 + delta]
      prograss = datas[29 + delta]

      link = get_link(raw_biao)

      print '----------------------------'
      print('name : %s' % name)
      print('total_money : %s' % total_money)
      print('duration : %s' % duration)
      print('year_rate : %s' % year_rate)
      print('prograss : %s' % prograss)
      print('link : %s' % link)

      if total_money[-3:] == "万":
        total_money = float(total_money[:-3]) * 10000
      duration = int(duration) * 30
      prograss = float(prograss[:-1])
      available_money = total_money * (100 - prograss) / 100

      if available_money > 100:
        has_item = True
        self.platform.loan_set.create(name = name,
          duration = duration,
          year_rate = year_rate,
          link = link,
          total_money = total_money,
          available_money = available_money)

    return has_item
