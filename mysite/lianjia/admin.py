from django.contrib import admin

# Register your models here.
from .models import SecondHandHouse

from django.contrib import admin
from django.utils.safestring import mark_safe

def link_type(obj):
    return mark_safe('<a href="%s">%s</a>' % (obj.unique_link, obj.title))
link_type.short_description = 'Link'

class SecondHandHouseAdmin(admin.ModelAdmin):
  list_display = ('last_collect_time', link_type, 'hidden', 'like_rate')
  list_editable = ('like_rate', 'hidden')
  list_display_links = ('last_collect_time',)

admin.site.register(SecondHandHouse, SecondHandHouseAdmin)

