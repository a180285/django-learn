#encoding:utf-8

from django.core.management.base import BaseCommand, CommandError
from financial.models import AccountRecord

from ._private import EDai365

class Command(BaseCommand):
  help = 'Running for cron-job'

  def handle(self, *args, **options):
    for t in [EDai365()]:
      t.run()
    self.stdout.write(self.style.SUCCESS('Successfully run the job '))
