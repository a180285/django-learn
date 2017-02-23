#encoding:utf-8

from django.contrib import admin

# Register your models here.
from .models import SecondHandHouse

from django.contrib import admin
from django.utils.safestring import mark_safe

def link_type(obj):
    return mark_safe(u'<a href="%s" target="_blank">%.2f万/平、%d万、%d平、%s<br/>%s<br/>%s</a>' % (
      obj.unique_link,
      obj.unit_price / 10000.0,
      obj.total_price,
      obj.area,
      obj.rooms_number,
      obj.title,
      obj.sub_title))
link_type.short_description = 'Link'

class SecondHandHouseAdmin(admin.ModelAdmin):
  list_display = ('last_collect_time', 'like_rate', 'hidden', link_type, 'for_sell')
  list_editable = ('like_rate', 'hidden', 'for_sell')
  list_display_links = ('last_collect_time',)
  list_filter = ('hidden', 'has_pictures', 'for_sell')
  list_per_page = 10

admin.site.register(SecondHandHouse, SecondHandHouseAdmin)

