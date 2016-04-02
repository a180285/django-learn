#encoding:utf-8

from django.core.management.base import BaseCommand, CommandError
from financial.models import AccountRecord

from ._private import *

class Command(BaseCommand):
  help = 'Running for cron-job'

  def handle(self, *args, **options):
    # test = HeShiDai()
    # test.run()

    for t in [EDai365(), 
        GuoChengJinRong(), 
        XueShanDai(),
        HeShiDai()]:
      t.run()

    self.stdout.write(self.style.SUCCESS('Successfully run the job '))
