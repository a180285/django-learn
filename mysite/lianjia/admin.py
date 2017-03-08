#encoding:utf-8

from django.contrib import admin

# Register your models here.
from .models import SecondHandHouse, PresalePermit

from django.contrib import admin
from django.utils.safestring import mark_safe

def link_type(obj):
    return mark_safe(u'<a href="%s" target="_blank">%.2f万/平、%d万、%d平<br/>%s<br/>%s<br/>%s年建、%s</a>' % (
      obj.unique_link,
      obj.unit_price / 10000.0,
      obj.total_price,
      obj.area,
      obj.title,
      obj.sub_title,
      obj.building_year,
      obj.rooms_number,
      ))
link_type.short_description = 'Link'

class SecondHandHouseAdmin(admin.ModelAdmin):
  list_display = ('unit_price', 'like_rate', 'hidden', link_type, 'for_sell', 'area', 'remarks')
  list_editable = ('like_rate', 'hidden', 'for_sell', 'remarks')
  list_display_links = ('unit_price',)
  list_filter = ('hidden', 'has_pictures', 'for_sell', 'like_rate', 'building_year')
  search_fields = ['title']
  list_per_page = 10

def permit_link_type(obj):
    return mark_safe(u'<a href="%s" target="_blank">%s</a>' % (
      obj.detail_link,
      obj.title
      ))
permit_link_type.short_description = 'title'

class PresalePermitAdmin(admin.ModelAdmin):
  search_fields = ['title', 'company', 'location', 'permit_name']
  list_display = (permit_link_type, 'company', 'location', 'permit_name', 'permit_type', 'date')
  list_display_links = ('company',)
  list_per_page = 10

admin.site.register(SecondHandHouse, SecondHandHouseAdmin)
admin.site.register(PresalePermit, PresalePermitAdmin)

