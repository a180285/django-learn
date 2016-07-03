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
    url(r'^account/(?P<account_id>[0-9]+)/(?P<last_edit_date>[0-9\-]+)/$', views.EditRecord.as_view(),
      name='updated_record'),
    url(r'^account/(?P<account_id>[0-9]+)/delete_record/(?P<record_id>[0-9]+)/$', views.DeleteRecord.as_view(),
      name='delete_record'),
    url(r'^cash-flow/$', views.CashFlowView.as_view(), name='cash_flow_page'),
    url(r'^cash-flow-ng/$', views.CashFlowNgView.as_view(), name='cash_flow_page'),

    url(r'^accounts-json/$', views.GetAccountsView.as_view(), name = 'get_accounts'),
    url(r'^update-account-(?P<account_id>[0-9]+)/$', views.InsertOrUpdateAccountView.as_view(),
      name = 'update_account'),
    url(r'^insert-account/$', views.InsertOrUpdateAccountView.as_view(), name = 'insert_account'),
    url(r'^delete-account-(?P<account_id>[0-9]+)/$', views.DeleteAccountView.as_view(), name = 'delete_account_ng'),
]
