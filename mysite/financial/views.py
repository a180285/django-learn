#encoding:utf-8

from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.template import loader
from .models import UserAccount, AccountRecord
from .forms import UserAccountForm, RecordForm
from django.db import IntegrityError

from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import View

class OwnerRequiredView(UserPassesTestMixin, View):
  def test_func(self):

    if self.request.user.is_authenticated(): 
      self.login_url = reverse('financial:user_home_page', args=())
      self.redirect_field_name = None

    return self.request.user.is_authenticated() and self._check_account_owner()

  def _check_account_owner(self):
    account_id = self.kwargs.get("account_id")
    if not account_id:
      return True

    any_accounts = UserAccount.objects.filter(pk = account_id)
    if not any_accounts:
      return False

    account = any_accounts[0]
    return account.user_id == self.request.user.id

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

      form = UserAccountForm()

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
  def get(self, request, account_id):
    form = RecordForm
    return self._response(account_id, form)

  def post(self, request, account_id):
    form = RecordForm(request.POST)
    if form.is_valid():
      record = form.save(commit = False)
      record.account_id = account_id
      record.save()

      form = RecordForm()

    return self._response(account_id, form)

  def _response(self, account_id, form):
    records = AccountRecord.objects.filter(account_id = account_id)
    context = {
      'record_list': records,
      'form': form}
    return render(self.request, 'financial/edit-record.html', context)
