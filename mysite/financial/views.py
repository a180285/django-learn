#encoding:utf-8

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.template import loader
from .models import Account
from django.db import IntegrityError

def index(request):
  return render(request, 'financial/index.html')

def account(request):
  accounts = Account.objects.order_by("name")
  context = {'account_list': accounts}
  return render(request, 'financial/account.html', context)

def add_account(request):
  new_account = Account(name = request.POST['name'],
    interest_manage_rate = request.POST['interest_manage_rate'],
    pick_up_rate = request.POST['pick_up_rate'],
    comment = request.POST['comment'])

  try:
    new_account.save()
  except IntegrityError, e:
    has_error = True
    accounts = Account.objects.order_by("name")
    context = {'has_error': has_error,
      'account_list': accounts}
    return render(request, 'financial/account.html', context)
  
  return HttpResponseRedirect(reverse('financial:account', args=()))
