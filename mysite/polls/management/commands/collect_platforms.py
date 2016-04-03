#encoding:utf-8

from django.core.management.base import BaseCommand, CommandError
from financial.models import AccountRecord

from ._private import *

import traceback

class Command(BaseCommand):
  help = 'Running for cron-job'

  def handle(self, *args, **options):
    platforms = [EDai365(), 
        GuoChengJinRong(), 
        XueShanDai(),
        YiQiHao(),
        ShiTouJinRong(),
        ChengHuiTong(),
        NoNoBank(),
        HeShiDai()]

    platforms = [NoNoBank()]

    for p in platforms:
      try:
        p.run()
      except Exception, e:
        print traceback.format_exc()

    self.stdout.write(self.style.SUCCESS('Successfully run the job '))
