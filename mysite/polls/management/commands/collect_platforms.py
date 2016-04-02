#encoding:utf-8

from django.core.management.base import BaseCommand, CommandError
from financial.models import AccountRecord

from ._private import *

class Command(BaseCommand):
  help = 'Running for cron-job'

  def handle(self, *args, **options):
    # test = GuoChengJinRong()
    # test.run()

    for t in [EDai365(), GuoChengJinRong()]:
      t.run()

    self.stdout.write(self.style.SUCCESS('Successfully run the job '))
