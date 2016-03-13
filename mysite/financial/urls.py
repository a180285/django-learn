from django.conf.urls import url

from . import views

app_name = 'financial'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^account/$', views.account, name='account'),
]
