#encoding:utf-8

import django_tables2 as tables
from .models import Loan

from django_tables2.utils import A  # alias for Accessor

class LoanTable(tables.Table):
  name = tables.LinkColumn(None, verbose_name="标名", attrs = {'a': {'target':"blank"}}, orderable = False)
  link = tables.Column(visible = False)
  id = tables.Column(visible = False)

  class Meta:
    model = Loan
    attrs = {"class": "paleblue"}
    sequence = ("name", "duration", 'available_money', 'year_rate', '...')
  # platform = models.ForeignKey(Platform, on_delete = models.CASCADE)
  # name = models.CharField(max_length = 128)
  # duration = models.IntegerField(default = 0)
  # year_rate = models.FloatField(default = 0)
  # link = models.URLField(unique = True)
  # total_money = models.FloatField(default = 0)
  # available_money = models.FloatField(default = 0)
