#encoding:utf-8

from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponseRedirect
from datetime import date
from django.utils import timezone

from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.template import loader
from .models import UserAccount, AccountRecord, CashFlow
from .forms import UserAccountForm, RecordForm
from django.db import IntegrityError

from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import View

from django.views.generic.dates import DateMixin

from django.core import serializers

class GenericDateView(DateMixin):
  date_field = '%m-%d'

  def _format_date(self, date):
    return date.strftime(self.get_date_field())

class OwnerRequiredView(UserPassesTestMixin, View):
  def test_func(self):

    if self.request.user.is_authenticated():
      self.login_url = reverse('financial:user_home_page', args=())
      self.redirect_field_name = None

    return (self.request.user.is_authenticated() and
      self._check_account_owner() and
      self._check_record_owner())

  def _check_account_owner(self):
    account_id = self.kwargs.get("account_id")
    if not account_id:
      return True

    any_accounts = UserAccount.objects.filter(pk = account_id)
    if not any_accounts:
      return False

    account = any_accounts[0]
    return account.user_id == self.request.user.id

  def _check_record_owner(self):
    record_id = self.kwargs.get("record_id")
    if not record_id:
      return True

    any_records = AccountRecord.objects.filter(pk = record_id)
    if not any_records:
      return False

    record = any_records[0]
    return record.user_id == self.request.user.id

class UserHomePage(OwnerRequiredView):
  def get(self, request, account_id = None):
    account = None
    if account_id:
      account = get_object_or_404(UserAccount, pk = account_id)
    form = UserAccountForm(instance = account)
    return self._response(form)

  def post(self, request, account_id = None):
    account = None
    if account_id:
      account = get_object_or_404(UserAccount, pk = account_id)
    form = UserAccountForm(request.POST, instance = account)
    if form.is_valid():
      account = form.save(commit = False)
      account.user_id = request.user.id
      account.save()

      return HttpResponseRedirect(reverse('financial:user_home_page', args = ()))

    return self._response(form)

  def _response(self, form):
    accounts = self.request.user.useraccount_set.all()
    context = {
      'account_list': accounts,
      'form': form}
    return render(self.request, 'financial/user-home-page.html', context)

class DeleteAccount(OwnerRequiredView):
  def get(self, request, account_id):
    UserAccount.objects.get(pk = account_id).delete()
    return HttpResponseRedirect(reverse('financial:user_home_page', args= ()))

class EditRecord(OwnerRequiredView):
  def get(self, request, account_id, last_edit_date = None):
    form = RecordForm
    if last_edit_date:
      form = RecordForm(initial = {'date': last_edit_date})
    return self._response(account_id, form)

  def post(self, request, account_id, last_edit_date = None):
    form = RecordForm(request.POST)
    if form.is_valid():
      record = form.save(commit = False)
      record.account_id = account_id
      record.user_id = request.user.id
      record.save()

      last_edit_date = form['date'].value()
      return HttpResponseRedirect(reverse('financial:updated_record', args = (account_id, last_edit_date)))

    return self._response(account_id, form)

  def _response(self, account_id, form):
    account = UserAccount.objects.get(pk = account_id)
    records = AccountRecord.objects.filter(account_id = account_id).order_by('date')
    context = {
      "account_name": account.name,
      'record_list': records,
      'form': form}
    return render(self.request, 'financial/edit-record.html', context)

class CashFlowView(OwnerRequiredView, GenericDateView):
  def get(self, request):
    user_id = request.user.id
    self._refresh_cash_flow(user_id)
    flows = CashFlow.objects.filter(user_id = user_id).order_by('date')

    cash_flows = []
    for flow in flows:
      cash_flows.append(flow)

    output_cash_flows = []

    cash_flow_daily = {}
    money_left = 0
    today = date.today()
    for i in xrange(-3,33):
      day = today + timezone.timedelta(days = i)
      while self._has_cash_flow_before(cash_flows, day):
        cash_flow = cash_flows.pop(0)
        money_left += cash_flow.money
        if cash_flow_daily:
          output_cash_flows.append(cash_flow)

      cash_flow_daily[self._format_date(day)] = money_left

    cash_flow_daily = cash_flow_daily.items()
    cash_flow_daily.sort()

    categories = []
    data = []

    for (day, money) in cash_flow_daily:
      categories.append(day)
      data.append(money)

    context = {
      'cash_flow_daily': cash_flow_daily,
      'categories': categories,
      'data': data,
      'user': request.user,
      'cash_flows': output_cash_flows}
    return render(self.request, 'financial/cash-flow.html', context)

  def _has_cash_flow_before(self, cash_flows, day):
    return cash_flows and cash_flows[0].date <= day

  def _refresh_cash_flow(self, user_id):
    records = AccountRecord.objects.filter(user_id = user_id)
    for record in records:
      if record.cashflow_set.all():
        continue

      CashFlow.objects.create(
        user_id = user_id,
        account_record_id = record.id,
        date = record.date,
        money = record.money)

class DeleteRecord(OwnerRequiredView):
  def get(self, request, account_id, record_id):
    AccountRecord.objects.get(pk = record_id).delete()

    return HttpResponseRedirect(reverse('financial:show_record', args = (account_id, )))

class CashFlowNgView(OwnerRequiredView, GenericDateView):
  def get(self, request):
    return render(self.request, 'financial/cash-flow-ng.html', {})

class GetAccountsView(OwnerRequiredView):
  def get(self, request):
    accounts = request.user.useraccount_set.all()
    return HttpResponse(serializers.serialize("json", accounts))

class InsertOrUpdateAccountView(OwnerRequiredView):
  def post(self, request, account_id = None):
    name = request.POST['name']
    account = None
    if account_id:
      account = UserAccount.objects.get(pk = account_id)
      account.name = name
      account.save()
    else:
      account = UserAccount.objects.create(
        user_id = request.user.id,
        name = name)

    return HttpResponse(serializers.serialize("json", [account]))

class DeleteAccountView(OwnerRequiredView):
  def post(self, request, account_id):
    print("account_id" + str(account_id))
    UserAccount.objects.get(pk = account_id).delete()
    return HttpResponse('')
