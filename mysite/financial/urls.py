from django.conf.urls import url

from . import views

app_name = 'financial'

urlpatterns = [
    url(r'^$', views.UserHomePage.as_view(), name='user_home_page'),
    url(r'^edit-account/(?P<account_id>[0-9]+)/$', views.UserHomePage.as_view(), 
      name='edit_account'),
    url(r'^delete-account/(?P<account_id>[0-9]+)/$', views.DeleteAccount.as_view(), 
      name='delete_account'),
    url(r'^account/(?P<account_id>[0-9]+)/$', views.EditRecord.as_view(), 
      name='show_record'),
    url(r'^account/(?P<account_id>[0-9]+)/delete_record/(?P<record_id>[0-9]+)/$', views.DeleteRecord.as_view(), 
      name='delete_record'),
    url(r'^cash-flow/$', views.CashFlowView.as_view(), name='cash_flow_page'),
    url(r'^chart/$', views.weather_chart_view, name='chart'),
]
