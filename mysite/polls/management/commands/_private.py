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
    index = 1
    while self._get(index):
      index += 1
    print("self.platform > " + str(self.platform))

  def _get(self, index):
    has_item = False
    print("Page : %d" % index)
    url = 'http://www.365edai.cn/Lend/Cloanlist.aspx?k=e&sortby=1&sort=desc&page=' + str(index)
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

      available_money = available_money[3:].replace(',', '')
      total_money = total_money.replace(',', '')
      if duration_type == '天':
        duration_type = 'days'
      elif duration_type == '月':
        duration_type = 'months'

      print('link -> ' + link)
      print('biao_name -> ' + biao_name)
      print('total_money -> ' + total_money)
      print('year_rate -> ' + year_rate)
      print('duration -> ' + duration)
      print('duration_type -> ' + duration_type)
      print('additional_rate -> ' + additional_rate)
      print('return_method -> ' + return_method)
      print('available_money -> ' + available_money)
      print('prograss -> ' + prograss)

      has_item = has_item or (float(available_money) > 0)

    return has_item
