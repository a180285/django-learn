from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone

# Create your models here.

class Question(models.Model):
  question_text = models.CharField(max_length=200)
  pub_date = models.DateTimeField('date published')

  def __str__(self):
    return self.question_text

  def was_published_recently(self):
    now = timezone.now()
    return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  choice_text = models.CharField(max_length=200)
  votes = models.IntegerField(default=0)

  def __str__(self):
    return self.choice_text

@python_2_unicode_compatible
class Platform(models.Model):
  name = models.CharField(max_length = 128, unique = True)

  def __str__(self):
    return self.name

@python_2_unicode_compatible
class Loan(models.Model):
  platform = models.ForeignKey(Platform, on_delete = models.CASCADE)
  name = models.CharField(max_length = 128)
  duration = models.IntegerField(default = 0)
  year_rate = models.FloatField(default = 0)
  link = models.URLField(unique = True)
  total_money = models.FloatField(default = 0)
  available_money = models.FloatField(default = 0)

  def name_with_link(self):
    return u'<a href="%s" target="blank">%s</a>' % (self.link, self.name)

  def get_absolute_url(self):
    return self.link

  def __str__(self):
    return '%s > %s' % (self.platform.name, self.name)
