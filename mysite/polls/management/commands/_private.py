#encoding:utf-8

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from polls.models import Platform, Loan

import urllib2

class EDai365():
  def __init__(self):
    self.platform_name = "365易贷"
    self.platform = Platform.objects.get_or_create(name = self.platform_name)[0]

  def run(self):
    self.platform.loan_set.all().delete()
    index = 1
    while self._get(index):
      index += 1
    print("self.platform > " + str(self.platform))

  def _get(self, index):
    has_item = False
    print("Page : %d" % index)
    url = 'http://www.365edai.cn/Lend/Cloanlist.aspx?k=e&page=' + str(index)
    req = urllib2.Request(url)
    data = urllib2.urlopen(req).read()
    biaos = data.split("biaoname")[1:]
    for raw_biao in biaos:
      raw_datas = [raw_data.split('<')[0].strip() for raw_data in raw_biao.split('>')]

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

      available_money = float(available_money[3:].replace(',', ''))
      total_money = float(total_money.replace(',', ''))

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
