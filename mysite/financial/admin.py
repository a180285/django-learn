from django.contrib import admin

# Register your models here.

from .models import UserAccount, AccountRecord, CashFlow

admin.site.register(UserAccount)
admin.site.register(AccountRecord)
