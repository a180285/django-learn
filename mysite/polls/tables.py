#encoding:utf-8

import django_tables2 as tables
from .models import Loan

from django_tables2.utils import A  # alias for Accessor

class LoanTable(tables.Table):
  name = tables.LinkColumn(None, verbose_name="标名", attrs = {'a': {'target':"blank"}}, orderable = False)
  link = tables.Column(visible = False)
  id = tables.Column(visible = False)
  total_money = tables.Column(visible = False)

  def render_year_rate(self, value):
    return '%.1f %%' % (value)

  def render_available_money(self, value):
    available_money = int(value)

    result = ''
    while available_money >= 1000:
      result = ',%03d%s' % (available_money % 1000, result)
      available_money /= 1000
    result = '%d%s' % (available_money, result)

    return result

  def render_duration(self, value):
    duration = int(value)
    days_in_month = 30
    duration_type = '天'
    if duration >= days_in_month:
      duration_type = '月'
      if duration % days_in_month == 0:
        duration /= days_in_month
      else:
        duration = duration * 1.0 / duration

    return '%s %s' % (duration, duration_type)

  class Meta:
    model = Loan
    attrs = {"class": "paleblue"}
    sequence = ("name", "duration", 'year_rate', 'available_money')
  # platform = models.ForeignKey(Platform, on_delete = models.CASCADE)
  # name = models.CharField(max_length = 128)
  # duration = models.IntegerField(default = 0)
  # year_rate = models.FloatField(default = 0)
  # link = models.URLField(unique = True)
  # total_money = models.FloatField(default = 0)
  # available_money = models.FloatField(default = 0)
