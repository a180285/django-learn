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


from django.core.management.base import BaseCommand, CommandError
from financial.models import AccountRecord

from ._private import *

import traceback

class Command(BaseCommand):
  help = 'Running for cron-job'

  def add_arguments(self, parser):
      parser.add_argument('--sleep', type=int, default=7)

  def handle(self, *args, **options):
    sleep = options['sleep']
    print 'sleep', sleep
    checker = CheckLianjia()
    checker.sleep = sleep
    try:
        checker.run()
    except Exception, e:
        print traceback.format_exc()
    # return

    self.stdout.write(self.style.SUCCESS('Successfully run the job '))

# 点融网：没有什么可投标
# 开鑫贷：利率低，标少
