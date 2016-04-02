#encoding:utf-8

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from polls.models import Platform, Loan

import urllib2, urllib

def split_by_tag(raw_data_str):
  return [raw_data.split('<')[0].strip() for raw_data in raw_data_str.split('>')]

class EDai365():
  def __init__(self):
    self.platform_name = "365易贷"
    self.platform = Platform.objects.get_or_create(name = self.platform_name)[0]

  def run(self):
    self.platform.loan_set.all().delete()
    index = 1
    while self._get(index):
      index += 1
    print("EDai365 Done ...")

  def _get(self, index):
    has_item = False
    print("Page : %d" % index)
    url = 'http://www.365edai.cn/Lend/Cloanlist.aspx?k=e&page=' + str(index)
    print("url -> " + url)

    req = urllib2.Request(url)
    data = urllib2.urlopen(req).read()
    biaos = data.split("biaoname")[1:]
    for raw_biao in biaos:
      if raw_biao.find('密码') != -1:
        continue

      raw_datas = split_by_tag(raw_biao)

      # self.debug(raw_datas)

      link = 'http://www.365edai.cn' + raw_datas[0].split('"')[2]
      biao_name = raw_datas[1]
      total_money = raw_datas[15]
      year_rate = raw_datas[19]
      duration = raw_datas[23]
      duration_type = raw_datas[24]
      if raw_datas[27]:
        additional_rate = raw_datas[27]
        return_method = raw_datas[30]
        available_money = raw_datas[36]
        prograss = raw_datas[43]
      else:
        additional_rate = '0'
        return_method = raw_datas[30 - 2]
        available_money = raw_datas[36 - 2]
        prograss = raw_datas[43 - 2]

      print('---------------------------------')
      print('link -> %s' % link)
      print('biao_name -> %s' % biao_name)
      print('total_money -> %s' % total_money)
      print('year_rate -> %s' % year_rate)
      print('duration -> %s' % duration)
      print('duration_type -> %s' % duration_type)
      print('additional_rate -> %s' % additional_rate)
      print('return_method -> %s' % return_method)
      print('available_money -> %s' % available_money)
      print('prograss -> %s' % prograss)

      available_money = float(available_money[3:].replace(',', ''))
      total_money = float(total_money.replace(',', ''))

      if duration_type == '天':
        duration_days = int(duration)
      elif duration_type == '月':
        duration_days = int(duration) * 30

      actaul_year_rate = float(year_rate) + float(additional_rate) * 360 / duration_days

      if available_money > 100:
        has_item = True
        self.platform.loan_set.create(name = biao_name,
          duration = duration_days,
          year_rate = actaul_year_rate,
          link = link,
          total_money = total_money,
          available_money = available_money)

    return has_item

  def debug(self, datas):
    for index in xrange(0, len(datas)):
      print("%s -> %s" % (index, datas[index][:100]))

class GuoChengJinRong():
  def __init__(self):
    self.platform_name = "国诚金融"
    self.platform = Platform.objects.get_or_create(name = self.platform_name)[0]
  
  def run(self):
    self.platform.loan_set.all().delete()
    index = 1
    while self._get(index):
      index += 1
    print("GuoChengJinRong Done ...")

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
      print '----------------'
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
