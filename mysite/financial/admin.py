from django.contrib import admin

# Register your models here.

from .models import Account, AccountRecord, CashFlow

admin.site.register(Account)
admin.site.register(AccountRecord)
