from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone

# Create your models here.

@python_2_unicode_compatible
class SecondHandHouse(models.Model):
  unique_link = models.URLField(default = '', unique = True)
  title = models.CharField(max_length = 1024)
  sub_title = models.CharField(max_length = 1024)
  total_price = models.IntegerField(default = 0)
  unit_price = models.IntegerField(default = 0)
  first_price = models.IntegerField(default = 0)
  last_collect_time = models.DateTimeField(default = timezone.now)
  like_rate = models.IntegerField(default = 3)
  hidden = models.BooleanField(default = False)
  area = models.IntegerField(default = 0)
  building_year = models.IntegerField(default = 0)
  has_pictures = models.BooleanField(default = True)
  for_sell = models.BooleanField(default = True)
  rooms_number = models.CharField(max_length = 1024, default = '')
  remarks = models.CharField(max_length = 10000, null = True, blank = True)
  listing_time = models.CharField(max_length = 10000, null = True, blank = True)

  def __str__(self):
    return self.title

@python_2_unicode_compatible
class PresalePermit(models.Model):
  detail_link = models.URLField(default = '', unique = True)
  title = models.CharField(max_length = 1024)
  company = models.CharField(max_length = 1024)
  location = models.CharField(max_length = 1024)
  permit_name = models.CharField(max_length = 1024)
  permit_type = models.CharField(max_length = 1024)
  date = models.CharField(max_length = 1024)
