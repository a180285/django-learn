from django.conf.urls import url

from . import views

app_name = 'polls'
urlpatterns = [
    # url(r'^$', views.IndexView.as_view(), name='index'),
    # url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    # url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^$', views.table, name = 'table'),
    url(r'^platform-(?P<platform_id>[0-9]+)/$', views.table, name = 'table'),
    url(r'^duration-(?P<min_duration>[0-9]+)-(?P<max_duration>[0-9]+)/$', views.table, name = 'table'),
    url(r'^loans-json/$', views.loans_json, name = 'loans-json'),
    url(r'^platforms-json/$', views.platforms_json, name = 'platforms-json'),
]
