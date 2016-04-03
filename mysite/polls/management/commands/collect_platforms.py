#encoding:utf-8

from django.core.management.base import BaseCommand, CommandError
from financial.models import AccountRecord

from ._private import *

class Command(BaseCommand):
  help = 'Running for cron-job'

  def handle(self, *args, **options):
    platforms = [EDai365(), 
        GuoChengJinRong(), 
        XueShanDai(),
        YiQiHao(),
        HeShiDai()]

    # platforms = [YiQiHao()]

    for p in platforms:
      p.run()

    self.stdout.write(self.style.SUCCESS('Successfully run the job '))
