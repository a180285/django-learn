from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.template import loader
from .models import Account

def index(request):
  return HttpResponse("Hello, world. This is financial first page")

def account(request):
  accounts = Account.objects.order_by("name")
  context = {'account_list': accounts}
  return render(request, 'financial/account.html', context)
