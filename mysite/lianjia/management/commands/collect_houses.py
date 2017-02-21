#encoding:utf-8

from django.core.management.base import BaseCommand, CommandError
from financial.models import AccountRecord

from ._private import *

import traceback

class Command(BaseCommand):
  help = 'Running for cron-job'

  def handle(self, *args, **options):
    checker = CheckLianjia()
    try:
        checker.run()
    except Exception, e:
        print traceback.format_exc()
    # return

    self.stdout.write(self.style.SUCCESS('Successfully run the job '))

# 点融网：没有什么可投标
# 开鑫贷：利率低，标少
