from __future__ import unicode_literals

from django.db import models

from datetime import date

from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User

# Create your models here.

@python_2_unicode_compatible
class UserAccount(models.Model):
  user = models.ForeignKey(User, on_delete = models.CASCADE)
  name = models.CharField(max_length = 128, unique = True)
  interest_manage_rate = models.FloatField(default = 0.0)
  pick_up_rate = models.FloatField(default = 0.0)
  comment = models.TextField(blank = True, default = "")

  def __str__(self):
    return self.name

@python_2_unicode_compatible
class AccountRecord(models.Model):
  user = models.ForeignKey(User, on_delete = models.CASCADE)
  account = models.ForeignKey(UserAccount, on_delete = models.CASCADE)
  money = models.FloatField()
  date = models.DateField(default = date.today)
  apply_type = models.CharField(max_length = 128)
  year_rate = models.FloatField(default = 0)
  days = models.IntegerField(null = True)
  months = models.IntegerField(null = True)
  quarters = models.IntegerField(null = True)

  def __str__(self):
    return "%s (%s): %s" % (self.account, self.date, self.money)

@python_2_unicode_compatible
class CashFlow(models.Model):
  user = models.ForeignKey(User, on_delete = models.CASCADE)
  account_record = models.ForeignKey(AccountRecord, on_delete = models.CASCADE)
  money = models.FloatField()
  date = models.DateField()

  def __str__(self):
    return "%s: %s" % (self.date, self.money)
