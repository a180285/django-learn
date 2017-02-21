from django.contrib import admin

# Register your models here.
from .models import SecondHandHouse

from django.contrib import admin


class SecondHandHouseAdmin(admin.ModelAdmin):
  list_display = ('title', 'last_collect_time', 'like_rate')

admin.site.register(SecondHandHouse, SecondHandHouseAdmin)

