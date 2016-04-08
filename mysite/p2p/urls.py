from django.conf.urls import url

from . import views

app_name = 'p2p'

urlpatterns = [
  url(r'^$', views.IndexView.as_view(), name='index'),
]
